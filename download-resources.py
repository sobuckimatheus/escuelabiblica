#!/usr/bin/env python3
import re
import os
import urllib.request
import urllib.parse
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
        print(f"✓ {url} -> {local_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao baixar {url}: {e}")
        return False

def extract_urls_from_html(html_content, base_url):
    """Extrai todas as URLs de recursos do HTML"""
    urls = set()

    # Padrões para encontrar recursos
    patterns = [
        r'href=["\']([^"\']+)["\']',
        r'src=["\']([^"\']+)["\']',
        r'url\(["\']?([^"\')\s]+)["\']?\)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, html_content)
        for match in matches:
            # Ignorar URLs especiais
            if match.startswith(('data:', 'javascript:', 'mailto:', '#', '//')):
                continue

            # Converter URL relativa para absoluta
            full_url = urllib.parse.urljoin(base_url, match)

            # Apenas URLs do mesmo domínio
            if base_url in full_url:
                urls.add(full_url)

    return urls

def url_to_local_path(url, base_url):
    """Converte URL para caminho local"""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path

    # Remover barra inicial
    if path.startswith('/'):
        path = path[1:]

    # Se termina com /, adicionar index.html
    if path.endswith('/') or not path:
        path += 'index.html'

    return path

# Ler o HTML
print("Lendo index.html...")
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

base_url = 'https://escuelabiblicakids.com/'

print("Extraindo URLs de recursos...")
urls = extract_urls_from_html(html_content, base_url)

print(f"\nEncontrados {len(urls)} recursos para baixar\n")

# Baixar recursos
downloaded = 0
failed = 0

for i, url in enumerate(urls, 1):
    print(f"[{i}/{len(urls)}] ", end='')
    local_path = url_to_local_path(url, base_url)

    if download_file(url, local_path):
        downloaded += 1
    else:
        failed += 1

    # Pausa pequena para não sobrecarregar o servidor
    time.sleep(0.2)

print(f"\n✅ Download concluído!")
print(f"   Sucesso: {downloaded}")
print(f"   Falhas: {failed}")
