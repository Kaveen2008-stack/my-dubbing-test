import asyncio, os, pathlib, requests, edge_tts

OUT = pathlib.Path("output")
OUT.mkdir(exist_ok=True)

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

def eleven():
    key = os.environ.get("ELEVEN_API_KEY")
    if not key:
        print("ELEVEN skipped (no key)")
        return
    voice = "21m00Tcm4TlvDq8ikWAM"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
    for i, t in enumerate(TEXTS):
        for lang in ("si", None):
            body = {"text": t, "model_id": "eleven_v3"}
            if lang:
                body["language_code"] = lang
            r = requests.post(url, headers={"xi-api-key": key}, json=body)
            tag = f"lang={lang}"
            if r.status_code == 200:
                (OUT / f"eleven_{tag}_{i}.mp3").write_bytes(r.content)
                print(f"ELEVEN OK   #{i} {tag}")
            else:
                print(f"ELEVEN FAIL #{i} {tag}: {r.status_code} {r.text[:200]}")

asyncio.run(azure())
eleven()
