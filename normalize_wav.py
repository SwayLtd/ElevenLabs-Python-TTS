from pydub import AudioSegment
import os

# Liste des fichiers à normaliser
files = [
    os.path.join("output", "fr-FR_C__B09RKQKM5P_excerpt2__KDPP_F.wav"),
    os.path.join("output", "fr-FR_C__B09SFHVNMS_excerpt1__KDPP_F.wav"),
    os.path.join("output", "fr-FR_C__B09SFHVNMS_excerpt2__KDPP_F.wav"),
]

for wav_path in files:
    if os.path.exists(wav_path):
        print(f"Normalisation : {wav_path}")
        sound = AudioSegment.from_wav(wav_path)
        sound = sound.apply_gain(-sound.max_dBFS)  # Normalise à 0 dBFS
        sound.export(wav_path, format="wav")
        print(f"  -> Fichier normalisé : {wav_path}")
    else:
        print(f"Fichier non trouvé : {wav_path}")
