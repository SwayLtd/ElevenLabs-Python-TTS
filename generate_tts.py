from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import os
from pydub import AudioSegment
import wave
import struct
import tempfile

load_dotenv()
API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
if not API_KEY or not VOICE_ID:
    raise ValueError(
        "ELEVENLABS_API_KEY et ELEVENLABS_VOICE_ID doivent être définis dans le fichier .env"
    )
client = ElevenLabs(api_key=API_KEY)

INPUT_DIR = "input"
OUTPUT_DIR = "output"
MODEL_ID = "eleven_multilingual_v2"
PCM_DIR = "pcm"
TEMP_WAV_DIR = tempfile.mkdtemp(prefix="wavtmp_")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PCM_DIR, exist_ok=True)

for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".txt"):
        input_path = os.path.join(INPUT_DIR, filename)
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
        print(f"Génération audio pour : {filename}")

        # Découpage du texte en morceaux de 5000 caractères max, en essayant de couper à la fin d'une phrase
        max_len = 5000
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + max_len, len(text))
            if end < len(text):
                # Cherche le dernier point avant la limite
                last_dot = text.rfind(".", start, end)
                if last_dot != -1 and last_dot > start:
                    end = last_dot + 1
            chunks.append(text[start:end].strip())
            start = end

        wav_parts = []
        for i, chunk in enumerate(chunks):
            print(f"  Traitement du chunk {i+1}/{len(chunks)}")
            audio = client.text_to_speech.convert(
                text=chunk,
                voice_id=VOICE_ID,
                model_id=MODEL_ID,
                output_format="pcm_48000",
                voice_settings={
                    "stability": 0.7,
                    "similarity_boost": 1.0,
                },
            )
            pcm_part_path = os.path.join(
                PCM_DIR, filename.replace(".txt", f"_part{i+1}.pcm")
            )
            with open(pcm_part_path, "wb") as f:
                for chunk_bytes in audio:
                    f.write(chunk_bytes)
            print(f"  Fichier PCM brut généré : {pcm_part_path}")

            # Ajout d'un en-tête WAV pour obtenir un vrai fichier WAV (dans TEMP_WAV_DIR)
            wav_part_path = os.path.join(
                TEMP_WAV_DIR, filename.replace(".txt", f"_part{i+1}.wav")
            )
            sample_rate = 48000
            num_channels = 1
            sample_width = 2  # 16 bits = 2 bytes
            with open(pcm_part_path, "rb") as pcmfile:
                pcm_data = pcmfile.read()
            with wave.open(wav_part_path, "wb") as wavfile:
                wavfile.setnchannels(num_channels)
                wavfile.setsampwidth(sample_width)
                wavfile.setframerate(sample_rate)
                wavfile.writeframes(pcm_data)
            print(f"  Fichier WAV généré (16 bits) : {wav_part_path}")

            # Conversion en 24 bits si besoin + normalisation du volume
            sound = AudioSegment.from_wav(wav_part_path)
            sound = sound.set_sample_width(3)  # 24 bits = 3 bytes
            sound = sound.apply_gain(-sound.max_dBFS)  # Normalise à 0 dBFS
            sound.export(wav_part_path, format="wav")
            print(f"  Fichier WAV finalisé en 24 bits et normalisé : {wav_part_path}")
            wav_parts.append(wav_part_path)

        # Fusion des fichiers WAV en un seul
        if len(wav_parts) > 1:
            print(f"Fusion des {len(wav_parts)} parties en un seul fichier WAV...")
            combined = AudioSegment.empty()
            for part in wav_parts:
                combined += AudioSegment.from_wav(part)
            final_wav_path = os.path.join(OUTPUT_DIR, filename.replace(".txt", ".wav"))
            combined.export(final_wav_path, format="wav")
            print(f"Fichier WAV fusionné : {final_wav_path}")
        elif len(wav_parts) == 1:
            # Renomme le seul fichier généré
            final_wav_path = os.path.join(OUTPUT_DIR, filename.replace(".txt", ".wav"))
            os.replace(wav_parts[0], final_wav_path)
            print(f"Fichier WAV final : {final_wav_path}")
