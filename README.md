# Spec Kit Simple AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Standalone](https://img.shields.io/badge/App-Standalone-green.svg)](#compiler-en-exe-windows)

**Spec Kit Simple AI** est une application locale, autonome et pensée pour les débutants. Elle permet de transformer une idée de projet en documents structurés grâce à une IA, sans devoir utiliser Git, le terminal de façon avancée, React, Vite ou le workflow complet de Spec Kit officiel.

L'application s'inspire de la logique du **Spec-Driven Development** : avant de coder, on clarifie l'idée, on rédige un cahier des charges, on prépare un plan, puis on découpe le projet en tâches.

```text
Idée floue
  ↓
Questions de clarification
  ↓
Cahier des charges
  ↓
Plan d'action
  ↓
Liste de tâches
  ↓
Export simple ou compatible Spec Kit officiel
```

---

## Sommaire

- [Objectif](#objectif)
- [Public visé](#public-visé)
- [Fonctionnalités](#fonctionnalités)
- [Captures d'usage attendues](#captures-dusage-attendues)
- [Structure du projet](#structure-du-projet)
- [Prérequis](#prérequis)
- [Lancer le projet en local avec CMD](#lancer-le-projet-en-local-avec-cmd)
- [Compiler en exe Windows](#compiler-en-exe-windows)
- [Configuration IA](#configuration-ia)
- [Fournisseurs IA compatibles](#fournisseurs-ia-compatibles)
- [Utilisation de l'application](#utilisation-de-lapplication)
- [Exports disponibles](#exports-disponibles)
- [Sécurité des clés API](#sécurité-des-clés-api)
- [Dépannage](#dépannage)
- [Créer une release GitHub](#créer-une-release-github)
- [Roadmap](#roadmap)
- [Licence](#licence)

---

## Objectif

Spec Kit officiel est puissant, mais il s'adresse surtout à des développeurs habitués aux outils suivants :

- Git ;
- lignes de commande ;
- agents IA de développement ;
- fichiers Markdown structurés ;
- workflows de type `spec`, `plan`, `tasks`, `implement`.

**Spec Kit Simple AI** propose une porte d'entrée plus accessible :

```text
J'ouvre l'application
Je configure ma clé API
Je choisis mon modèle IA
Je décris mon idée
L'IA me pose des questions
Je valide mes réponses
L'IA génère les documents
J'exporte le résultat
```

Le but n'est pas de remplacer Spec Kit officiel, mais de rendre sa logique compréhensible et utilisable par des non-initiés.

---

## Public visé

Ce projet est pensé pour :

- les débutants en programmation ;
- les étudiants ;
- les porteurs de projets ;
- les personnes qui veulent structurer une idée avant de demander à une IA ou à un développeur de coder ;
- les développeurs qui veulent générer rapidement une base de spécification exploitable.

L'utilisateur final n'a pas besoin d'installer Node.js, React, Vite ou Git pour utiliser l'application compilée.

---

## Fonctionnalités

### Application locale standalone

L'application est développée en Python et peut être compilée en `.exe` avec PyInstaller.

Une fois compilée, elle peut être lancée par double-clic.

### Interface simple en HTML/CSS/JavaScript

L'interface est locale et affichée dans une fenêtre grâce à `pywebview`.

Cela permet d'avoir une interface proche d'une application web, sans imposer une stack web complexe.

### IA centrale

L'IA n'est pas optionnelle : elle est au centre du parcours.

Elle sert à :

- poser des questions de clarification ;
- reformuler l'idée ;
- générer un cahier des charges ;
- générer un plan d'action ;
- générer une liste de tâches ;
- faire une revue de cohérence ;
- prendre en compte l'historique des réponses.

### Prise en compte des réponses à chaque étape

À chaque étape, l'utilisateur peut ajouter des réponses, remarques ou corrections.

Les boutons de validation permettent d'ajouter explicitement ces informations dans l'historique :

- réponses aux questions de clarification ;
- retours sur le cahier des charges ;
- retours sur le plan d'action ;
- retours sur les tâches ;
- retours sur la revue de cohérence.

Les générations suivantes utilisent cet historique afin que l'IA ne reparte pas de zéro.

### Historique du projet

Un onglet dédié affiche l'historique complet de la session.

Cet historique permet de vérifier ce qui a été dit, validé ou corrigé.

Il est aussi exporté dans :

```text
historique.md
```

### Choix dynamique du modèle IA

L'application peut récupérer la liste des modèles disponibles via l'endpoint `/models` du fournisseur choisi.

L'utilisateur peut ensuite choisir le modèle dans une liste déroulante.

### Fournisseur IA configurable

L'application fonctionne avec des fournisseurs compatibles avec l'API OpenAI :

- Fantasy AI ;
- OpenRouter ;
- OpenAI ;
- fournisseur personnalisé compatible OpenAI.

L'utilisateur peut configurer :

- la clé API ;
- la base URL ;
- l'endpoint de chat ;
- l'endpoint des modèles ;
- le modèle à utiliser.

### Export simple

L'application peut exporter les documents suivants :

- `cahier-des-charges.md` ;
- `plan-action.md` ;
- `taches.md` ;
- `revue-coherence.md` ;
- `historique.md`.

### Export ZIP récupérable

L'utilisateur peut choisir où enregistrer son archive ZIP.

Fonctions prévues :

- choisir l'emplacement de sauvegarde ;
- exporter en ZIP ;
- copier le chemin du ZIP ;
- ouvrir le dossier contenant le ZIP.

### Export compatible Spec Kit officiel

L'application peut générer une structure proche de celle attendue par un projet Spec Kit officiel.

Structure générée :

```text
.specify/
└── memory/
    └── constitution.md

specs/
└── 001-nom-du-projet/
    ├── spec.md
    ├── plan.md
    ├── tasks.md
    ├── research.md
    ├── quickstart.md
    ├── data-model.md
    ├── contracts/
    │   └── README.md
    └── checklists/
        └── requirements.md

README_SPEC_KIT_EXPORT.md
```

Cela permet à un développeur ou à un agent IA de reprendre le travail dans un workflow plus avancé.

---

## Captures d'usage attendues

Flux utilisateur typique :

```text
1. Configurer le fournisseur IA
2. Coller sa clé API
3. Récupérer les modèles disponibles
4. Choisir un modèle
5. Décrire son idée
6. Générer les questions de clarification
7. Répondre et valider les réponses
8. Générer le cahier des charges
9. Ajouter des corrections si nécessaire
10. Générer le plan
11. Générer les tâches
12. Lancer la revue de cohérence
13. Exporter en ZIP simple ou Spec Kit officiel
```

---

## Structure du projet

```text
spec-kit-simple-ai/
├── main.py
├── requirements.txt
├── build_windows.bat
├── build_linux_mac.sh
├── README.md
├── LICENSE
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

## Prérequis

Pour lancer le projet depuis le code source :

- Windows, Linux ou macOS ;
- Python 3.10 ou plus récent ;
- une connexion internet pour appeler le fournisseur IA ;
- une clé API Fantasy, OpenRouter, OpenAI ou compatible OpenAI.

Pour l'utilisateur final d'une release `.exe`, Python n'est pas censé être nécessaire.

---

## Lancer le projet en local avec CMD

Les commandes suivantes sont prévues pour Windows avec **cmd**, sans environnement virtuel.

### 1. Ouvrir cmd dans le dossier du projet

Exemple :

```bat
cd C:\Users\TonNom\Downloads\spec-kit-simple-ai
```

### 2. Installer les dépendances

```bat
python -m pip install --upgrade pip
python -m pip install pywebview requests pyinstaller
```

### 3. Vérifier que pywebview est bien installé

Le paquet s'appelle `pywebview`, mais dans le code il est importé avec `import webview`.

```bat
python -c "import webview; print('OK webview trouve')"
```

Si le message s'affiche, l'installation est correcte.

### 4. Lancer l'application

```bat
python main.py
```

Une fenêtre doit s'ouvrir.

---

## Compiler en exe Windows

### Méthode recommandée : utiliser le script

```bat
build_windows.bat
```

L'exécutable sera généré dans :

```text
dist\SpecKitSimpleAI.exe
```

### Méthode manuelle avec cmd

Nettoyer les anciens builds :

```bat
rmdir /s /q build
rmdir /s /q dist
del SpecKitSimpleAI.spec
```

Compiler :

```bat
python -m PyInstaller --clean --noconsole --onefile --name "SpecKitSimpleAI" --collect-all webview --hidden-import=webview --add-data "web;web" --add-data "prompts;prompts" main.py
```

Important : sous Windows, `--add-data` utilise un point-virgule `;`.

---

## Compiler sous Linux ou macOS

Installer les dépendances :

```bash
python3 -m pip install --upgrade pip
python3 -m pip install pywebview requests pyinstaller
```

Compiler :

```bash
python3 -m PyInstaller --clean --onefile --name "SpecKitSimpleAI" \
  --collect-all webview \
  --hidden-import=webview \
  --add-data "web:web" \
  --add-data "prompts:prompts" \
  main.py
```

Important : sous Linux/macOS, `--add-data` utilise deux-points `:`.

---

## Configuration IA

L'application utilise des APIs de type OpenAI-compatible.

Dans l'interface, l'utilisateur doit renseigner ou sélectionner :

- le fournisseur IA ;
- la clé API ;
- la base URL ;
- l'endpoint de chat ;
- l'endpoint des modèles ;
- le modèle IA.

---

## Fournisseurs IA compatibles

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

Pour un fournisseur compatible OpenAI :

```text
Base URL : https://mon-fournisseur.com/v1
Endpoint chat : /chat/completions
Endpoint modèles : /models
Authentification : Bearer token
```

---

## Utilisation de l'application

1. Ouvrir l'application.
2. Aller dans la section de configuration IA.
3. Choisir Fantasy, OpenRouter, OpenAI ou Custom.
4. Coller sa clé API.
5. Cliquer sur le bouton de récupération des modèles.
6. Choisir un modèle.
7. Décrire son idée de projet.
8. Générer les questions de clarification.
9. Répondre aux questions.
10. Valider les réponses pour les ajouter à l'historique.
11. Générer le cahier des charges.
12. Ajouter éventuellement des corrections.
13. Générer le plan d'action.
14. Générer les tâches.
15. Lancer la revue de cohérence.
16. Choisir l'emplacement d'export.
17. Exporter en ZIP simple ou compatible Spec Kit officiel.

---

## Exports disponibles

### Export simple

Contenu typique :

```text
cahier-des-charges.md
plan-action.md
taches.md
revue-coherence.md
historique.md
```

### Export ZIP complet

Contient les documents simples ainsi que les éléments utiles pour reprendre le projet.

### Export compatible Spec Kit officiel

Contient :

```text
.specify/memory/constitution.md
specs/001-nom-du-projet/spec.md
specs/001-nom-du-projet/plan.md
specs/001-nom-du-projet/tasks.md
specs/001-nom-du-projet/research.md
specs/001-nom-du-projet/quickstart.md
specs/001-nom-du-projet/data-model.md
specs/001-nom-du-projet/contracts/README.md
specs/001-nom-du-projet/checklists/requirements.md
README_SPEC_KIT_EXPORT.md
```

---

## Sécurité des clés API

La clé API doit rester privée.

Recommandations :

- ne jamais publier une clé API sur GitHub ;
- ne jamais l'écrire directement dans le code ;
- ne pas partager de capture d'écran où elle apparaît ;
- utiliser une clé avec limite de consommation si le fournisseur le permet ;
- révoquer la clé si elle a été exposée.

Dans une future version, le stockage sécurisé pourrait être amélioré avec `keyring`.

---

## Dépannage

### Erreur : `ModuleNotFoundError: No module named 'webview'`

Cela signifie que `pywebview` n'est pas installé dans le Python utilisé.

Solution :

```bat
python -m pip install pywebview
python -c "import webview; print('OK webview trouve')"
```

Pour compiler, utiliser :

```bat
python -m PyInstaller ...
```

et non simplement :

```bat
pyinstaller ...
```

Cela évite de lancer PyInstaller depuis un autre environnement Python.

### L'exe ne se met pas à jour

Supprimer les anciens fichiers :

```bat
rmdir /s /q build
rmdir /s /q dist
del SpecKitSimpleAI.spec
```

Puis recompiler.

### Les modèles ne se chargent pas

Vérifier :

- la validité de la clé API ;
- la base URL ;
- l'endpoint `/models` ;
- les droits du compte API ;
- la connexion internet.

### L'IA ne prend pas mes réponses en compte

Vérifier que les réponses ont bien été validées avec le bouton correspondant.

Les réponses validées doivent apparaître dans l'historique.

### Le ZIP est introuvable

Utiliser les boutons de l'onglet Export :

- choisir l'emplacement ;
- copier le chemin ;
- ouvrir le dossier.

---

## Créer une release GitHub

Pour publier une version utilisable par tous :

1. Compiler l'application avec PyInstaller.
2. Récupérer :

```text
dist\SpecKitSimpleAI.exe
```

3. Créer une release GitHub.
4. Ajouter l'exécutable à la release.
5. Ajouter aussi :

```text
README.md
LICENSE
```

6. Indiquer dans la description de release :

```text
Téléchargez SpecKitSimpleAI.exe, puis lancez-le par double-clic.
Configurez ensuite votre clé API depuis l'application.
```

---

## Roadmap

Améliorations possibles :

- stockage sécurisé avec `keyring` ;
- meilleure gestion des erreurs API ;
- streaming des réponses IA ;
- sauvegarde et rechargement de plusieurs projets ;
- templates de projets ;
- mode sombre ;
- mode IA locale avec Ollama ;
- installeur Windows ;
- signature de l'exécutable ;
- export GitHub automatique ;
- amélioration de la compatibilité avec le workflow Spec Kit officiel.

---

## Licence

Ce projet est distribué sous licence **MIT**.

Cela signifie que le code peut être utilisé, copié, modifié, fusionné, publié et distribué librement, y compris dans des projets privés ou commerciaux, à condition de conserver la notice de licence.

Voir le fichier [`LICENSE`](LICENSE).

---

## Auteur

Projet conçu pour rendre les workflows de spécification IA plus accessibles aux débutants et aux non-développeurs.
