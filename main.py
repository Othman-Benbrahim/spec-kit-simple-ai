from __future__ import annotations

import json
import os
import re
import sys
import zipfile
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import webview


APP_NAME = "Spec Kit Simple AI"
APP_VERSION = "0.1.0"


PROVIDER_PRESETS = {
    "fantasy": {
        "label": "Fantasy AI Cloud",
        "base_url": "https://fantasyai.cloud/api/v1",
        "chat_endpoint": "/chat/completions",
        "models_endpoint": "/models",
        "auth_type": "bearer",
        "extra_headers": {},
        "default_model": "deepseek-v4",
    },
    "openrouter": {
        "label": "OpenRouter",
        "base_url": "https://openrouter.ai/api/v1",
        "chat_endpoint": "/chat/completions",
        "models_endpoint": "/models",
        "auth_type": "bearer",
        "extra_headers": {
            "HTTP-Referer": "https://local.spec-kit-simple-ai",
            "X-OpenRouter-Title": "Spec Kit Simple AI",
        },
        "default_model": "",
    },
    "openai": {
        "label": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "chat_endpoint": "/chat/completions",
        "models_endpoint": "/models",
        "auth_type": "bearer",
        "extra_headers": {},
        "default_model": "",
    },
    "custom": {
        "label": "Compatible OpenAI personnalisé",
        "base_url": "",
        "chat_endpoint": "/chat/completions",
        "models_endpoint": "/models",
        "auth_type": "bearer",
        "extra_headers": {},
        "default_model": "",
    },
}


def resource_path(relative: str) -> Path:
    """Return a path that works both in development and in a PyInstaller bundle."""
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return Path(base) / relative
    return Path(__file__).resolve().parent / relative


def app_data_dir() -> Path:
    if sys.platform.startswith("win"):
        root = os.getenv("APPDATA") or str(Path.home())
        path = Path(root) / "SpecKitSimpleAI"
    elif sys.platform == "darwin":
        path = Path.home() / "Library" / "Application Support" / "SpecKitSimpleAI"
    else:
        path = Path.home() / ".spec-kit-simple-ai"
    path.mkdir(parents=True, exist_ok=True)
    return path


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9àâäçéèêëîïôöùûüÿñæœ -]", "", text)
    text = text.replace(" ", "-")
    text = re.sub(r"-+", "-", text)
    return text[:60].strip("-") or "projet"


@dataclass
class ProviderConfig:
    provider: str = "fantasy"
    api_key: str = ""
    base_url: str = PROVIDER_PRESETS["fantasy"]["base_url"]
    chat_endpoint: str = PROVIDER_PRESETS["fantasy"]["chat_endpoint"]
    models_endpoint: str = PROVIDER_PRESETS["fantasy"]["models_endpoint"]
    selected_model: str = PROVIDER_PRESETS["fantasy"]["default_model"]
    temperature: float = 0.4
    extra_headers: Optional[Dict[str, str]] = None

    def normalized_extra_headers(self) -> Dict[str, str]:
        return self.extra_headers or {}


class OpenAICompatibleProvider:
    def __init__(self, config: ProviderConfig):
        self.config = config

    def _join_url(self, endpoint: str) -> str:
        endpoint = endpoint.strip()
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        base = self.config.base_url.strip().rstrip("/")
        if not base:
            raise ValueError("Base URL vide. Renseigne une base URL ou un endpoint complet.")
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        return base + endpoint

    def _headers(self) -> Dict[str, str]:
        if not self.config.api_key.strip():
            raise ValueError("Clé API manquante.")
        headers = {
            "Authorization": f"Bearer {self.config.api_key.strip()}",
            "Content-Type": "application/json",
        }
        headers.update(self.config.normalized_extra_headers())
        return headers

    def list_models(self) -> List[Dict[str, Any]]:
        url = self._join_url(self.config.models_endpoint)
        response = requests.get(url, headers=self._headers(), timeout=45)
        self._raise_for_status(response)
        data = response.json()
        return self._normalize_models(data)

    def chat(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> str:
        selected_model = (model or self.config.selected_model or "").strip()
        if not selected_model:
            raise ValueError("Aucun modèle sélectionné.")
        url = self._join_url(self.config.chat_endpoint)
        payload = {
            "model": selected_model,
            "messages": messages,
            "temperature": float(self.config.temperature),
            "stream": False,
        }
        response = requests.post(url, headers=self._headers(), json=payload, timeout=120)
        self._raise_for_status(response)
        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except Exception as exc:
            raise ValueError(f"Format de réponse inattendu: {json.dumps(data, ensure_ascii=False)[:800]}") from exc

    @staticmethod
    def _normalize_models(data: Any) -> List[Dict[str, Any]]:
        # Formats fréquents : {"data": [{"id": ...}]} ou [{"id": ...}]
        raw_models = data.get("data", data) if isinstance(data, dict) else data
        if not isinstance(raw_models, list):
            return []

        models: List[Dict[str, Any]] = []
        for item in raw_models:
            if not isinstance(item, dict):
                continue
            model_id = item.get("id") or item.get("name") or item.get("model")
            if not model_id:
                continue
            label = item.get("name") or item.get("display_name") or model_id
            models.append({
                "id": str(model_id),
                "label": str(label),
                "raw": item,
            })
        models.sort(key=lambda m: m["id"].lower())
        return models

    @staticmethod
    def _raise_for_status(response: requests.Response) -> None:
        if response.ok:
            return
        text = response.text[:1200] if response.text else ""
        raise requests.HTTPError(
            f"Erreur HTTP {response.status_code}: {text}",
            response=response,
        )


class AppAPI:
    def __init__(self):
        self.data_dir = app_data_dir()
        self.config_path = self.data_dir / "config.json"
        self.export_dir = self.data_dir / "exports"
        self.export_dir.mkdir(exist_ok=True)

    # ---------- Config ----------
    def get_app_info(self) -> Dict[str, Any]:
        return {
            "name": APP_NAME,
            "version": APP_VERSION,
            "data_dir": str(self.data_dir),
            "presets": PROVIDER_PRESETS,
        }

    def load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            cfg = asdict(ProviderConfig(extra_headers={}))
            self.save_config(cfg)
            return cfg
        try:
            cfg = json.loads(self.config_path.read_text(encoding="utf-8"))
        except Exception:
            cfg = asdict(ProviderConfig(extra_headers={}))
        cfg.setdefault("provider", "fantasy")
        cfg.setdefault("api_key", "")
        cfg.setdefault("base_url", PROVIDER_PRESETS["fantasy"]["base_url"])
        cfg.setdefault("chat_endpoint", "/chat/completions")
        cfg.setdefault("models_endpoint", "/models")
        cfg.setdefault("selected_model", PROVIDER_PRESETS["fantasy"]["default_model"])
        cfg.setdefault("temperature", 0.4)
        cfg.setdefault("extra_headers", {})
        return cfg

    def save_config(self, cfg: Dict[str, Any]) -> Dict[str, Any]:
        # Ne jamais afficher la clé dans les logs. Stockage local simple pour MVP.
        self.config_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
        return {"ok": True, "path": str(self.config_path)}

    def apply_preset(self, provider: str, current_api_key: str = "") -> Dict[str, Any]:
        preset = PROVIDER_PRESETS.get(provider, PROVIDER_PRESETS["custom"])
        cfg = {
            "provider": provider,
            "api_key": current_api_key,
            "base_url": preset.get("base_url", ""),
            "chat_endpoint": preset.get("chat_endpoint", "/chat/completions"),
            "models_endpoint": preset.get("models_endpoint", "/models"),
            "selected_model": preset.get("default_model", ""),
            "temperature": 0.4,
            "extra_headers": preset.get("extra_headers", {}),
        }
        self.save_config(cfg)
        return cfg

    def _provider_from_cfg(self, cfg: Optional[Dict[str, Any]] = None) -> OpenAICompatibleProvider:
        cfg = cfg or self.load_config()
        config = ProviderConfig(
            provider=cfg.get("provider", "fantasy"),
            api_key=cfg.get("api_key", ""),
            base_url=cfg.get("base_url", ""),
            chat_endpoint=cfg.get("chat_endpoint", "/chat/completions"),
            models_endpoint=cfg.get("models_endpoint", "/models"),
            selected_model=cfg.get("selected_model", ""),
            temperature=float(cfg.get("temperature", 0.4)),
            extra_headers=cfg.get("extra_headers", {}),
        )
        return OpenAICompatibleProvider(config)

    # ---------- IA ----------
    def list_models(self, cfg: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            provider = self._provider_from_cfg(cfg)
            models = provider.list_models()
            return {"ok": True, "models": models}
        except Exception as exc:
            return {"ok": False, "error": str(exc), "models": []}

    def test_connection(self, cfg: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            provider = self._provider_from_cfg(cfg)
            models = provider.list_models()
            return {"ok": True, "message": f"Connexion OK. {len(models)} modèle(s) récupéré(s).", "models": models[:30]}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def ask_ai(self, user_message: str, cfg: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            provider = self._provider_from_cfg(cfg)
            system = self._read_prompt("system_beginner.txt")
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": user_message},
            ]
            answer = provider.chat(messages)
            return {"ok": True, "answer": answer}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def clarify(self, idea: str, context: str = "", cfg: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = self._read_prompt("clarify.txt").format(idea=idea, context=context or "Aucune réponse encore.")
        return self.ask_ai(prompt, cfg)

    def generate_spec(self, project_text: str, cfg: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = self._read_prompt("spec.txt").format(project_text=project_text)
        return self.ask_ai(prompt, cfg)

    def generate_plan(self, spec_text: str, cfg: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = self._read_prompt("plan.txt").format(spec_text=spec_text)
        return self.ask_ai(prompt, cfg)

    def generate_tasks(self, spec_text: str, plan_text: str, cfg: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = self._read_prompt("tasks.txt").format(spec_text=spec_text, plan_text=plan_text)
        return self.ask_ai(prompt, cfg)

    def review_project(self, spec_text: str, plan_text: str, tasks_text: str, cfg: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = self._read_prompt("review.txt").format(
            spec_text=spec_text,
            plan_text=plan_text,
            tasks_text=tasks_text,
        )
        return self.ask_ai(prompt, cfg)

    def _read_prompt(self, name: str) -> str:
        return resource_path(f"prompts/{name}").read_text(encoding="utf-8")

    # ---------- Export ----------
    def default_zip_filename(self, project_name: str = "projet") -> str:
        clean_name = slugify(project_name or "projet")
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"{clean_name}-{stamp}.zip"

    def choose_zip_path(self, project_name: str = "projet") -> Dict[str, Any]:
        """Open a native save dialog and return the selected ZIP path.

        This makes the export location explicit and avoids forcing users to copy a
        hidden application-data path. If the user cancels, the method returns a
        cancelled response instead of raising.
        """
        try:
            default_name = self.default_zip_filename(project_name)
            downloads = Path.home() / "Downloads"
            directory = downloads if downloads.exists() else Path.home()

            selected = None
            if webview.windows:
                selected = webview.windows[0].create_file_dialog(
                    webview.SAVE_DIALOG,
                    directory=str(directory),
                    save_filename=default_name,
                    file_types=("Archive ZIP (*.zip)", "Tous les fichiers (*.*)"),
                )

            if not selected:
                return {"ok": False, "cancelled": True, "error": "Choix annulé."}

            # pywebview may return a string or a list/tuple depending on platform.
            if isinstance(selected, (list, tuple)):
                selected = selected[0] if selected else ""

            path = Path(str(selected)).expanduser()
            if path.suffix.lower() != ".zip":
                path = path.with_suffix(".zip")
            return {"ok": True, "path": str(path)}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def open_export_location(self, path: str) -> Dict[str, Any]:
        """Open the folder containing an exported ZIP file."""
        try:
            p = Path(path).expanduser()
            target = p.parent if p.suffix else p
            if not target.exists():
                return {"ok": False, "error": f"Dossier introuvable : {target}"}

            if sys.platform.startswith("win"):
                os.startfile(str(target))  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(target)])
            else:
                subprocess.Popen(["xdg-open", str(target)])
            return {"ok": True}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def copy_text_to_clipboard(self, text: str) -> Dict[str, Any]:
        """Copy text to the system clipboard without adding a dependency."""
        try:
            if sys.platform.startswith("win"):
                subprocess.run("clip", input=text, text=True, shell=True, check=True)
            elif sys.platform == "darwin":
                subprocess.run(["pbcopy"], input=text, text=True, check=True)
            else:
                # Common Linux clipboard tools. Try several and report a clear error if absent.
                for command in (["wl-copy"], ["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]):
                    try:
                        subprocess.run(command, input=text, text=True, check=True)
                        return {"ok": True}
                    except Exception:
                        continue
                return {"ok": False, "error": "Aucun outil presse-papiers trouvé (wl-copy, xclip ou xsel)."}
            return {"ok": True}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def export_project(self, project_name: str, spec: str, plan: str, tasks: str, review: str = "", history: str = "", zip_path: str = "") -> Dict[str, Any]:
        try:
            clean_name = slugify(project_name or "projet")
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            folder = self.export_dir / f"{clean_name}-{stamp}"
            folder.mkdir(parents=True, exist_ok=True)

            files = {
                "cahier-des-charges.md": spec or "# Cahier des charges\n\nNon généré.\n",
                "plan-action.md": plan or "# Plan d'action\n\nNon généré.\n",
                "taches.md": tasks or "# Liste des tâches\n\nNon générée.\n",
            }
            if review.strip():
                files["revue-coherence.md"] = review
            if history.strip():
                files["historique.md"] = "# Historique du projet\n\n" + history

            # Export simple
            for filename, content in files.items():
                (folder / filename).write_text(content, encoding="utf-8")

            # Export compatible logique Spec Kit
            spec_folder = folder / "specs" / f"001-{clean_name}"
            memory_folder = folder / ".specify" / "memory"
            spec_folder.mkdir(parents=True, exist_ok=True)
            memory_folder.mkdir(parents=True, exist_ok=True)
            (spec_folder / "spec.md").write_text(spec or "", encoding="utf-8")
            (spec_folder / "plan.md").write_text(plan or "", encoding="utf-8")
            (spec_folder / "tasks.md").write_text(tasks or "", encoding="utf-8")
            (memory_folder / "constitution.md").write_text(
                "# Constitution du projet\n\n"
                "- Priorité à la simplicité.\n"
                "- Les documents doivent rester compréhensibles par un novice.\n"
                "- Chaque fonctionnalité doit correspondre à un besoin clair.\n"
                "- La première version doit rester minimale et testable.\n",
                encoding="utf-8",
            )

            if zip_path.strip():
                final_zip_path = Path(zip_path.strip()).expanduser()
                if final_zip_path.suffix.lower() != ".zip":
                    final_zip_path = final_zip_path.with_suffix(".zip")
                final_zip_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                final_zip_path = self.export_dir / f"{clean_name}-{stamp}.zip"

            with zipfile.ZipFile(final_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                for path in folder.rglob("*"):
                    if path.is_file():
                        zf.write(path, path.relative_to(folder))

            return {"ok": True, "folder": str(folder), "zip": str(final_zip_path)}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}


def main() -> None:
    api = AppAPI()
    index = resource_path("web/index.html")
    webview.create_window(
        APP_NAME,
        str(index),
        js_api=api,
        width=1180,
        height=800,
        min_size=(980, 680),
    )
    webview.start(debug=False)


if __name__ == "__main__":
    main()
