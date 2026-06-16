import json
import os
import re

# Carrega os dois arquivos de posts
todos_posts = []

for arquivo in ["posts.json", "posts_1.json"]:
    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)
        todos_posts.extend(dados)

print(f"Total de posts carregados: {len(todos_posts)}")

# Dicionário para armazenar: { "a": ["url1", "url2"], "b": ["url3"] }
letras = {}

for post in todos_posts:
    # Pega as hashtags do post
    hashtags_encontradas = []
    
    for item in post.get("label_values", []):
        if item.get("title") == "Hashtags":
            for tag in item.get("dict", []):
                nome = tag.get("dict", [{}])[0].get("value", "")
                hashtags_encontradas.append(nome.lower())
    
    # Procura hashtags que são exatamente 1 letra ou 1 número
    letras_do_post = []
    for tag in hashtags_encontradas:
        match = re.match(r"^[a-z0-9]$", tag)
        if match:
            letras_do_post.append(tag)
    
    # Se encontrou letras, pega a URL da imagem
    if letras_do_post:
        # Extrai a URI da imagem
        uri_imagem = None
        for item in post.get("label_values", []):
            if item.get("label") == "Mídia":
                for media in item.get("media", []):
                    uri_imagem = media.get("uri", "")
                    break
        
        if uri_imagem:
            # Converte o caminho local para URL pública
            # Ex: media/posts/18106407103759145.heic → public/imagens/18106407103759145.heic
            nome_arquivo = os.path.basename(uri_imagem)
            url_publica = f"public/imagens/{nome_arquivo}"
            
            # Adiciona para cada letra encontrada
            for letra in letras_do_post:
                if letra not in letras:
                    letras[letra] = []
                if url_publica not in letras[letra]:
                    letras[letra].append(url_publica)
                    print(f"  ✓ #{letra.upper()} → {nome_arquivo}")

# Salva o letras.json
with open("letras.json", "w", encoding="utf-8") as f:
    json.dump(letras, f, indent=2, ensure_ascii=False)

print(f"\n✅ letras.json gerado com sucesso!")
print(f"Letras encontradas: {sorted(letras.keys())}")
for letra, imagens in sorted(letras.items()):
    print(f"  {letra.upper()}: {len(imagens)} imagem(ns)")
