import urllib.request
import urllib.error
import json
import base64
import os

API_KEY = "AIzaSyAywdmRrSro0oVhASG_6ra-c7tl-OPzNys"
MODEL = "gemini-3.1-flash-image-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
OUT = "C:/Resource/greatest-version-0.1/animated-website-super-skilled/images"

prompts = [
    ("hero", "16:9", "Aerial cinematic view of a vibrant amusement park on a sunny day. Blue sky with soft clouds, roller coasters, a large ferris wheel, colorful rides and attractions, happy crowds below, motion blur on moving rides, golden-hour cinematic lighting, photorealistic 3D render style, bright saturated colors, wide panoramic shot"),
    ("skybreaker", "16:9", "Orange and white steel roller coaster mid-loop at full speed, dramatic low-angle shot looking up, motion blur on the coaster cars, passengers with arms raised, bright blue sky background, cinematic lighting, photorealistic, amusement park setting"),
    ("cloud-swing", "4:3", "Aerial view of a rotating swing ride at the top of its arc, passengers on swings high above an amusement park, blue sky with white clouds, golden sunlight, birds-eye perspective, photorealistic, vibrant colors, sense of freedom and height"),
    ("lightning-drop", "3:4", "Vertical drop tower ride, dramatic upward angle shot, bright yellow ride car in mid-freefall, motion blur, passengers screaming with excitement, deep blue sky, cinematic dramatic lighting, photorealistic, amusement park at daytime"),
    ("neon-midway", "16:9", "Carnival midway at night, colorful neon-lit game booths, giant plush prize animals hanging from booths, crowds of people walking, bright magenta and cyan neon lights reflecting on the ground, festive atmosphere, photorealistic, vibrant and energetic"),
    ("sunset-gardens", "16:9", "Outdoor amusement park food area at golden hour sunset, string lights overhead, people seated at outdoor tables eating classic fair food, cotton candy, hot dogs, lemonade stands, warm amber glow, relaxed and joyful atmosphere, photorealistic"),
]

def generate(name, aspect, prompt):
    print(f"Generating {name}...")
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]}
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
        for part in data["candidates"][0]["content"]["parts"]:
            if "inlineData" in part:
                img_bytes = base64.b64decode(part["inlineData"]["data"])
                mime = part["inlineData"].get("mimeType", "image/png")
                ext = "jpg" if "jpeg" in mime else "png"
                path = f"{OUT}/{name}.{ext}"
                with open(path, "wb") as f:
                    f.write(img_bytes)
                print(f"  Saved {path} ({len(img_bytes)//1024}KB)")
                return path
        print(f"  No image in response for {name}")
        print(f"  Response keys: {list(data.keys())}")
    except Exception as e:
        print(f"  Error for {name}: {e}")
    return None

results = {}
for name, aspect, prompt in prompts:
    path = generate(name, aspect, prompt)
    if path:
        results[name] = path

print("\nDone:", results)
