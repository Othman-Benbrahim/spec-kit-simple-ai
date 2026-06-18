# Spec Kit Simple AI

**Spec Kit Simple AI** est une application locale, autonome et accessible aux débutants, inspirée de la logique de Spec Kit.

L'objectif est simple : permettre à une personne qui n'est pas forcément développeuse de transformer une idée de projet en documents structurés grâce à une IA.

L'application aide à produire :

- un cahier des charges ;
- un plan d'action ;
- une liste de tâches ;
- une revue de cohérence ;
- un historique du projet ;
- une archive exportable contenant les documents générés.

L'application est conçue pour être lancée localement sur un ordinateur, puis empaquetée en `.exe` avec PyInstaller.

---

## Objectif du projet

Spec Kit officiel est puissant, mais il est plutôt pensé pour des développeurs habitués à Git, au terminal, aux agents IA et aux fichiers de configuration.

Ce projet cherche à proposer une version plus simple :

```text
J'ouvre l'application
↓
Je décris mon idée
↓
L'IA me pose des questions
↓
Je valide mes réponses
↓
L'IA génère les documents du projet
↓
J'exporte le résultat
```

L'utilisateur n'a pas besoin de comprendre Spec Kit, GitHub, React, Vite ou les commandes CLI.

---

## Fonctionnalités principales

### Assistant IA guidé

L'application accompagne l'utilisateur étape par étape :

1. clarification de l'idée ;
2. génération du cahier des charges ;
3. génération du plan d'action ;
4. génération des tâches ;
5. revue de cohérence du projet.

### Prise en compte des réponses à chaque étape

À chaque étape, l'utilisateur peut ajouter ses réponses, corrections ou précisions.

Les boutons de validation permettent d'ajouter explicitement les informations dans l'historique :

- valider les réponses aux questions de clarification ;
- valider les retours sur le cahier des charges ;
- valider les retours sur le plan ;
- valider les retours sur les tâches ;
- valider les retours sur la revue de cohérence.

Les générations suivantes utilisent cet historique complet afin que l'IA tienne compte des réponses précédentes.

### Historique du projet

Un onglet dédié affiche l'historique complet de la session.

L'historique permet de vérifier ce que l'utilisateur a déjà demandé, répondu ou corrigé.

Il est aussi exporté dans un fichier :

```text
historique.md
```

### Fournisseurs IA compatibles

L'application est pensée pour fonctionner avec plusieurs fournisseurs compatibles avec l'API OpenAI :

- Fantasy AI ;
- OpenRouter ;
- OpenAI ;
- fournisseur personnalisé compatible OpenAI.

L'utilisateur peut configurer :

- la clé API ;
- la base URL ;
- l'endpoint de chat ;
- l'endpoint des modèles ;
- le modèle IA à utiliser.

### Récupération dynamique des modèles

L'application peut appeler l'endpoint `/models` du fournisseur choisi afin de récupérer automatiquement la liste des modèles disponibles.

L'utilisateur peut ensuite choisir le modèle dans l'interface.

### Export des documents

L'application peut exporter :

- `cahier-des-charges.md` ;
- `plan-action.md` ;
- `taches.md` ;
- `revue-coherence.md` ;
- `historique.md` ;
- une archive `.zip` contenant les documents générés.

---

## Structure du projet

```text
spec-kit-simple-ai/
├── main.py
├── requirements.txt
├── build_windows.bat
├── build_linux_mac.sh
├── README.md
│
├── web/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── prompts/
│   ├── system_beginner.txt
│   ├── clarify.txt
│   ├── spec.txt
│   ├── plan.txt
│   ├── tasks.txt
│   └── review.txt
│
└── exports/
```

---

## Installation locale pour développement

### 1. Ouvrir un terminal dans le dossier du projet

Sous Windows, place-toi dans le dossier du projet :

```bat
cd chemin\vers\spec-kit-simple-ai
```

Exemple :

```bat
cd C:\Users\TonNom\Downloads\spec-kit-simple-ai
```

---

### 2. Créer un environnement virtuel

Cette étape est recommandée pour éviter les conflits entre plusieurs installations Python.

```bat
python -m venv .venv
```

Puis active l'environnement :

```bat
.venv\Scripts\activate
```

Si l'environnement est bien activé, tu devrais voir `(.venv)` au début de la ligne de commande.

---

### 3. Installer les dépendances

```bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller
```

---

### 4. Vérifier que pywebview est bien installé

Le paquet à installer s'appelle `pywebview`, mais dans le code il est importé avec `import webview`.

Teste avec :

```bat
python -c "import webview; print('OK webview trouve')"
```

Si le message `OK webview trouve` s'affiche, l'installation est correcte.

---

## Lancer le projet en local

Une fois les dépendances installées :

```bat
python main.py
```

Une fenêtre d'application doit s'ouvrir.

L'interface affichée est une interface HTML/CSS/JavaScript locale, pilotée par Python via pywebview.

---


## Export ZIP récupérable

Depuis l’onglet **Export**, l’utilisateur peut maintenant choisir explicitement où enregistrer le fichier `.zip`.

Fonctions disponibles :

- **Choisir l’emplacement** : ouvre une fenêtre système “Enregistrer sous” ;
- **Exporter en ZIP** : génère l’archive à l’emplacement choisi ;
- **Copier le chemin** : copie le chemin complet du fichier ZIP ;
- **Ouvrir le dossier** : ouvre directement le dossier contenant le ZIP.

Si aucun emplacement n’est choisi, l’application exporte dans son dossier local par défaut, puis affiche le chemin final dans l’interface.

## Compiler en `.exe` avec PyInstaller

### Méthode recommandée : script Windows

Dans le dossier du projet :

```bat
build_windows.bat
```

L'exécutable sera généré ici :

```text
dist\SpecKitSimpleAI.exe
```

---

### Méthode manuelle Windows

Si tu veux lancer la commande toi-même :

```bat
python -m PyInstaller --clean --noconsole --onefile --name "SpecKitSimpleAI" ^
  --collect-all webview ^
  --hidden-import=webview ^
  --add-data "web;web" ^
  --add-data "prompts;prompts" ^
  main.py
```

Important : sous Windows, `--add-data` utilise un point-virgule `;`.

---

### Méthode Linux / macOS

Sous Linux ou macOS, la syntaxe change légèrement :

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller
```

Puis :

```bash
python -m PyInstaller --clean --onefile --name "SpecKitSimpleAI" \
  --collect-all webview \
  --hidden-import=webview \
  --add-data "web:web" \
  --add-data "prompts:prompts" \
  main.py
```

Important : sous Linux/macOS, `--add-data` utilise deux-points `:`.

---

## Configuration IA

Dans l'application, va dans les paramètres IA.

Tu peux choisir un fournisseur prédéfini ou personnalisé.

### Fantasy AI

Configuration recommandée :

```text
Base URL : https://fantasyai.cloud/api/v1
Endpoint chat : /chat/completions
Endpoint modèles : /models
Authentification : Bearer token
```

### OpenRouter

Configuration recommandée :

```text
Base URL : https://openrouter.ai/api/v1
Endpoint chat : /chat/completions
Endpoint modèles : /models
Authentification : Bearer token
```

### OpenAI

Configuration recommandée :

```text
Base URL : https://api.openai.com/v1
Endpoint chat : /chat/completions
Endpoint modèles : /models
Authentification : Bearer token
```

### Fournisseur personnalisé

Pour un fournisseur compatible OpenAI, il faut renseigner :

```text
Base URL
Endpoint chat
Endpoint modèles
Clé API
Modèle
```

Exemple :

```text
Base URL : https://mon-fournisseur.com/v1
Endpoint chat : /chat/completions
Endpoint modèles : /models
```

---

## Utilisation de l'application

1. Ouvre l'application.
2. Configure ton fournisseur IA.
3. Ajoute ta clé API.
4. Clique sur le bouton permettant de récupérer les modèles disponibles.
5. Choisis un modèle.
6. Décris ton idée de projet.
7. Demande les questions de clarification.
8. Réponds aux questions.
9. Clique sur le bouton de validation des réponses.
10. Génère le cahier des charges.
11. Ajoute éventuellement des corrections.
12. Génère le plan d'action.
13. Génère les tâches.
14. Lance la revue de cohérence.
15. Exporte les documents.

---

## Sécurité des clés API

Pour la V1, la clé API est gérée localement par l'application.

Recommandations :

- ne jamais publier ta clé API sur GitHub ;
- ne jamais la mettre en dur dans le code ;
- éviter de partager une capture d'écran montrant la clé ;
- utiliser une clé avec des limites de consommation si le fournisseur le permet.

Une amélioration future pourrait utiliser `keyring` pour stocker la clé dans le gestionnaire sécurisé du système.

---

## Dépannage

### Erreur : `ModuleNotFoundError: No module named 'webview'`

Cela veut dire que `pywebview` n'est pas installé dans le Python utilisé pour lancer ou compiler l'application.

Solution recommandée :

```bat
python -m pip install pywebview
python -c "import webview; print('OK webview trouve')"
```

Puis compile avec :

```bat
python -m PyInstaller ...
```

et non simplement :

```bat
pyinstaller ...
```

Cela évite d'utiliser un autre environnement Python par erreur.

---

### L'exe généré ne se lance pas correctement

Nettoie les anciens fichiers :

```bat
rmdir /s /q build
rmdir /s /q dist
del SpecKitSimpleAI.spec
```

Puis relance :

```bat
build_windows.bat
```

---

### Les modèles ne se chargent pas

Vérifie :

- que ta clé API est valide ;
- que le fournisseur choisi est correct ;
- que la base URL est correcte ;
- que l'endpoint modèles est bien `/models` ;
- que ton compte API permet bien l'accès aux modèles.

---

### L'IA ne semble pas prendre mes réponses en compte

Vérifie que tu as bien cliqué sur le bouton de validation après avoir écrit tes réponses.

Les réponses validées sont ajoutées dans l'onglet historique.

Les générations suivantes utilisent cet historique.

---

## Build de release GitHub

Pour publier une version Windows :

1. Génère l'exe avec `build_windows.bat`.
2. Récupère le fichier :

```text
dist\SpecKitSimpleAI.exe
```

3. Crée une release GitHub.
4. Ajoute l'exe comme fichier de release.
5. Ajoute éventuellement une archive `.zip` contenant :

```text
SpecKitSimpleAI.exe
README.md
LICENSE
```

---

## Roadmap possible

Améliorations futures possibles :

- stockage sécurisé des clés avec `keyring` ;
- mode sombre ;
- meilleure gestion des erreurs API ;
- streaming des réponses IA ;
- génération d'un export compatible Spec Kit officiel ;
- sauvegarde/rechargement de plusieurs projets ;
- templates de projets ;
- mode totalement local avec Ollama ;
- signature de l'exécutable Windows ;
- installeur Windows `.msi` ou `.exe`.

---

## Licence


MIT.

---

## Résumé

Spec Kit Simple AI est une application locale qui rend la logique du développement piloté par les spécifications plus accessible.

Au lieu de demander à un novice d'utiliser un terminal ou un outil professionnel complexe, l'application propose une interface guidée par IA pour transformer une idée en documents structurés.

