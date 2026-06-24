import json
import os
import re
import instaloader

USER = os.environ["INSTAGRAM_USER"]
PASS = os.environ["INSTAGRAM_PASS"]

L = instaloader.Instaloader()
L.login(USER, PASS)

perfil = "vernaculando"

if not os.path.exists("temp"):
    os.makedirs("temp")

with open("letras.json", "r") as f:
    letras = json.load(f)

posts = instaloader.Profile.from_username(L.context, perfil).get_posts()
novos = 0

for post in posts:
    legenda = (post.caption or "").upper()
    hashtags = re.findall(r'#([A-Z0-9])\b', legenda)
    
    if not hashtags:
        continue
    
    for letra in hashtags:
        chave = letra.lower()
        if chave not in letras:
            letras[chave] = []
        
        L.download_post(post, target="temp")
        
        for arquivo in os.listdir("temp"):
            if arquivo.endswith((".jpg", ".png", ".webp")):
                nome_final = f"{chave}-{len(letras[chave])+1}.jpg"
                os.rename(f"temp/{arquivo}", f"public/imagens/{nome_final}")
                letras[chave].append(f"public/imagens/{nome_final}")
                novos += 1
                print(f"  ✓ #{letra} → {nome_final}")
        
        for f in os.listdir("temp"):
            os.remove(f"temp/{f}")

with open("letras.json", "w") as f:
    json.dump(letras, f, indent=2)

print(f"\n✅ {novos} novas imagens adicionadas!")
