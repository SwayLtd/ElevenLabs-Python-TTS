# Utilisation d'un environnement virtuel Python avec ElevenLabs

## 1. Créer un environnement virtuel

Ouvre un terminal dans le dossier du projet et exécute :

```bash
python -m venv venv
```

## 2. Activer l'environnement virtuel

- **Sous Windows** :
  
```bash
venv\Scripts\activate
```

- **Sous macOS/Linux** :
  
```bash
source venv/bin/activate
```

## 3. Installer la bibliothèque elevenlabs

Une fois l'environnement activé, installe la bibliothèque :

```bash
pip install elevenlabs
```

## 4. Lancer le script de génération TTS

Place tes fichiers `.txt` dans le dossier `input`, puis lance :

```bash
python generate_tts.py
```

---

**Rappel** :

- Pour désactiver l'environnement virtuel, tape simplement :
  
```bash
deactivate
```
