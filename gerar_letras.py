import json
import os
import re

todos_posts = []

for arquivo in ["posts.json", "posts_1.json"]:
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
            todos_posts.extend(dados)
        print(f"✓ {arquivo} carregado ({len(dados)} posts)")
    except FileNotFoundError:
        print(f"⚠ {arquivo} não encontrado, pulando...")

print(f"Total de posts carregados: {len(todos_posts)}")

letras = {}

for i, post in enumerate(todos_posts):
    # Extrai hashtags
    hashtags_encontradas = []
    for item in post.get("label_values", []):
        if item.get("title") == "Hashtags":
            for tag in item.get("dict", []):
                nome = tag.get("dict", [{}])[0].get("value", "")
                if nome:
                    hashtags_encontradas.append(nome.strip().lower())
    
    # Filtra hashtags com EXATAMENTE 1 caractere
    letras_do_post = []
    for tag in hashtags_encontradas:
        if re.match(r"^[a-z0-9]$", tag):
            letras_do_post.append(tag)
    
    # Se encontrou, pega a imagem
    if letras_do_post:
        uri_imagem = None
        for item in post.get("label_values", []):
            # Procura qualquer label que contenha "dia" (Mídia)
            label = item.get("label", "")
            if "dia" in label and "media" in item:
                for media in item.get("media", []):
                    uri_imagem = media.get("uri", "")
        
        if uri_imagem:
            nome_arquivo = os.path.basename(uri_imagem)
            url_publica = f"public/imagens/{nome_arquivo}"
            
            for letra in letras_do_post:
                if letra not in letras:
                    letras[letra] = []
                if url_publica not in letras[letra]:
                    letras[letra].append(url_publica)
                    print(f"  ✓ #{letra.upper()} → {nome_arquivo}")

with open("letras.json", "w", encoding="utf-8") as f:
    json.dump(letras, f, indent=2, ensure_ascii=False)

print(f"\n✅ letras.json gerado com sucesso!")
print(f"Letras encontradas: {sorted(letras.keys())}")
for letra, imagens in sorted(letras.items()):
    print(f"  {letra.upper()}: {len(imagens)} imagem(ns)")
