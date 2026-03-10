#!/usr/bin/env python3
import re

# Ler o HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Substituir URLs absolutas por caminhos relativos
html = re.sub(r'https://escuelabiblicakids\.com/', '', html)

# Salvar o HTML atualizado
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ URLs atualizadas para caminhos locais!")
