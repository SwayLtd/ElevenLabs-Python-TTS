from pydub import AudioSegment
import os
import subprocess

INPUT_DIR = os.path.join("output", "former")
OUTPUT_DIR = os.path.join(INPUT_DIR, "new")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Liste tous les fichiers audio (wav ou mp3) dans output/former
for filename in os.listdir(INPUT_DIR):
    if filename.lower().endswith((".wav", ".mp3")):
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)
        print(f"Normalisation avancée (ffmpeg) : {input_path}")
        # Commande ffmpeg équivalente à celle donnée
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-af",
            "dynaudnorm=f=150:g=15,loudnorm=I=-16:LRA=7:TP=-2",
            output_path,
        ]
        subprocess.run(cmd, check=True)
        print(f"  -> Fichier normalisé : {output_path}")
