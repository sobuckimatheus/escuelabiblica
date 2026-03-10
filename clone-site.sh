#!/bin/bash

# Script para clonar o site escuelabiblicakids.com

URL="https://escuelabiblicakids.com"
USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

echo "Baixando página principal..."
curl -A "$USER_AGENT" -L "$URL" -o index.html

echo "Extraindo URLs de CSS, JS e imagens..."
grep -oE 'href="[^"]+"' index.html | sed 's/href="//;s/"$//' > urls.txt
grep -oE 'src="[^"]+"' index.html | sed 's/src="//;s/"$//' >> urls.txt

echo "Total de recursos encontrados: $(wc -l < urls.txt)"
echo "URLs salvas em urls.txt"
