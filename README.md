# Java Secure Properties App

Application desktop (PyQt6) pour chiffrer et déchiffrer des chaînes avec le **MuleSoft Secure Properties Tool**.

Le projet fournit:
- une interface graphique simple pour lancer les opérations;
- un exécutable Python pour lancer l'app localement;
- un script de build pour générer un `.exe` Windows avec PyInstaller.

## Fonctionnalités

- Sélection du JAR `secure-properties-tool-j17.jar`
- Chiffrement ou déchiffrement (`encrypt` / `decrypt`)
- Choix de l'algorithme: `AES`, `Blowfish`, `DES`, `DESede`
- Choix du mode: `CBC`, `CFB`, `ECB`, `OFB`
- Option `Use random IV`
- Prise en charge de l'entrée au format YAML
- Copie du résultat dans le presse-papiers

## Prérequis (pour le développement)

- Python 3.10+ recommandé
- Java (commande `java` disponible dans le `PATH`)
- Le JAR MuleSoft présent dans `ressources/secure-properties-tool-j17.jar`

## Installation

Depuis la racine du projet:

```bash
python -m venv .venv
```

### Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS / Linux

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Lancer l'application

```bash
python main.py
```

## Utilisation

1. Vérifier le chemin du JAR (pré-rempli si trouvé dans `ressources/`).
2. Renseigner la clé de chiffrement.
3. Choisir l'action (`Encrypt` ou `Decrypt`).
4. Choisir l'algorithme et le mode.
5. Saisir le texte d'entrée.
6. Cliquer sur `Execute`.
7. Copier le résultat avec `Copy result`.

## Générer un exécutable Windows

Le script de build utilise PyInstaller et produit `dist/secure-properties-app.exe`.

```bash
python build_exe.py
```

Points importants du build:
- mode `--onefile` + `--windowed`
- inclusion des fichiers `app-interface.py` et `secure-properties-executor.py`
- inclusion du dossier `ressources/`

## Structure du projet

```text
.
|- main.py                       # Point d'entrée
|- app-interface.py              # Interface PyQt6
|- secure-properties-executor.py # Exécution de la commande Java
|- build_exe.py                  # Build PyInstaller
|- requirements.txt              # Dépendances Python
|- ressources/
|  |- secure-properties-tool-j17.jar
```

## Dépannage

- `java` introuvable:
	installer Java et vérifier `java -version` dans le terminal.
- `JAR file not found`:
	vérifier le chemin du JAR dans l'application.
- Erreur d'exécution Java:
	le message de `stderr` est renvoyé dans la zone de résultat.
- Fenêtre qui ne s'ouvre pas après packaging:
	relancer le build puis tester l'exécutable depuis un terminal pour voir les erreurs éventuelles.

## Auteur

- David CHOCHO

## Source

- https://github.com/Davosthecool/java-secure-properties-app
