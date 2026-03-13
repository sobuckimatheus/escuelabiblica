#!/usr/bin/env python3
import re
import os
import urllib.request
from pathlib import Path
import time

def download_file(url, local_path):
    """Baixa um arquivo da URL e salva no caminho local"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)

        # Criar diretório se não existir
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        with urllib.request.urlopen(req, timeout=30) as response:
            with open(local_path, 'wb') as out_file:
                out_file.write(response.read())
        print(f"✓ {local_path}")
        return True
    except Exception as e:
        print(f"✗ {local_path}: {e}")
        return False

# Ler o HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

base_url = 'https://escuelabiblicakids.com/'

# Encontrar todos os caminhos de imagem
image_patterns = [
    r'src="([^"]*wp-content/[^"]+)"',
    r'srcset="([^"]*wp-content/[^"]+)"',
    r'href="([^"]*wp-content/[^"]+)"',
]

image_paths = set()
for pattern in image_patterns:
    matches = re.findall(pattern, html)
    for match in matches:
        # Separar srcset que pode ter múltiplas URLs
        for path in match.split(','):
            path = path.strip().split()[0]  # Remove "300w", "600w" etc
            if 'wp-content/' in path:
                image_paths.add(path)

print(f"Encontrados {len(image_paths)} caminhos de imagens no HTML\n")

# Verificar quais estão faltando
missing = []
for path in image_paths:
    if not os.path.exists(path):
        missing.append(path)

print(f"Faltando {len(missing)} imagens:\n")

# Baixar as que faltam
downloaded = 0
failed = 0

for i, path in enumerate(missing, 1):
    print(f"[{i}/{len(missing)}] ", end='')
    url = base_url + path

    if download_file(url, path):
        downloaded += 1
    else:
        failed += 1

    time.sleep(0.2)

print(f"\n✅ Download concluído!")
print(f"   Sucesso: {downloaded}")
print(f"   Falhas: {failed}")
