import asyncio, pathlib
import edge_tts

OUT = pathlib.Path("output"); OUT.mkdir(exist_ok=True)
TEXTS = [
    "ඔයා කොහොමද? අද නම් හරි ලස්සන දවසක්නේ!",
    "මම ඒක කලිනුත් කිව්වානේ, ඇයි තාම තේරුණේ නැද්ද?",
    "අද උෂ්ණත්වය අංශක 32ක් විතර වෙනවා, ඒ නිසා පරිස්සමෙන් යන්න.",
    "ඔන්න හරි, දැන් අපි පටන් ගමු.",
]

async def azure():
    for v in ["si-LK-SameeraNeural", "si-LK-ThiliniNeural"]:
        for i, t in enumerate(TEXTS):
            try:
                await edge_tts.Communicate(t, v).save(str(OUT / f"azure_{v}_{i}.mp3"))
                print(f"AZURE OK   {v} #{i}")
            except Exception as e:
                print(f"AZURE FAIL {v} #{i}: {e}")

def mms():
    try:
        import torch, scipy.io.wavfile as wav
        from transformers import VitsModel, AutoTokenizer
        tok = AutoTokenizer.from_pretrained("facebook/mms-tts-sin")
        model = VitsModel.from_pretrained("facebook/mms-tts-sin")
        for i, t in enumerate(TEXTS):
            inputs = tok(t, return_tensors="pt")
            with torch.no_grad():
                audio = model(**inputs).waveform[0].numpy()
            wav.write(OUT / f"mms_{i}.wav", model.config.sampling_rate, audio)
            print(f"MMS OK     #{i}")
    except Exception as e:
        print(f"MMS FAIL: {e}")

asyncio.run(azure())
mms()
