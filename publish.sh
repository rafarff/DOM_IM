#!/usr/bin/env bash
# ─── DOM Incorporação · Publish Panorama ──────────────────────────────────
# Regenera o index.html a partir da Planilha Mestre e publica no GitHub.
# Uso:  ./publish.sh "Mensagem opcional do commit"
# ──────────────────────────────────────────────────────────────────────────
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

MSG="${1:-Atualização do Panorama $(date +%d/%m/%Y)}"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  DOM · Panorama de Lançamentos · Publish"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. Regenera o HTML a partir da Planilha Mestre
echo "▸ Regenerando index.html..."
python3 build_panorama.py

# 2. Verifica se há mudanças
if git diff --quiet index.html 2>/dev/null && git diff --cached --quiet index.html 2>/dev/null; then
  # Verifica se index.html é novo (não rastreado)
  if ! git ls-files --error-unmatch index.html > /dev/null 2>&1; then
    echo "  (index.html é novo — será adicionado)"
  else
    echo ""
    echo "✓ Nenhuma mudança no index.html. Nada a publicar."
    exit 0
  fi
fi

# 3. Commit e push
echo ""
echo "▸ Fazendo commit: \"$MSG\""
git add index.html
git commit -m "$MSG"

echo ""
echo "▸ Enviando para GitHub..."
git push

echo ""
echo "✓ Publicado. GitHub Pages atualiza em 1-2 minutos."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
