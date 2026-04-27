#!/usr/bin/env bash
# ─── DOM Incorporação · Publish Panorama ──────────────────────────────────
# 1. Regenera Planilha Mestre via gerar_planilha.py (source of truth)
# 2. Regenera index.html via build_panorama.py
# 3. Commit gerar_planilha.py + build_panorama.py + index.html + push
#    (planilhas .xlsx ficam LOCAIS — gitignored por política, são output)
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

# 1. Regenera Planilha Mestre a partir do source-of-truth (gerar_planilha.py)
echo "▸ Regenerando Planilha Mestre (gerar_planilha.py)..."
python3 _PADRAO_FASE_1/gerar_planilha.py

# 2. Regenera o HTML a partir da Planilha Mestre mais recente
echo ""
echo "▸ Regenerando index.html (build_panorama.py)..."
python3 build_panorama.py

# 3. Verifica se há mudanças em SOURCE ou no HTML
HAS_CHANGES=0
if ! git diff --quiet _PADRAO_FASE_1/gerar_planilha.py 2>/dev/null; then HAS_CHANGES=1; fi
if ! git diff --quiet build_panorama.py 2>/dev/null; then HAS_CHANGES=1; fi
if ! git diff --quiet index.html 2>/dev/null; then HAS_CHANGES=1; fi
if ! git ls-files --error-unmatch index.html > /dev/null 2>&1; then HAS_CHANGES=1; fi

if [ "$HAS_CHANGES" -eq 0 ]; then
    echo ""
    echo "✓ Nada a publicar (sem mudanças em source nem em HTML)."
    exit 0
fi

# 4. Commit (script-fonte + html) e push
echo ""
echo "▸ Adicionando arquivos:"
echo "    • _PADRAO_FASE_1/gerar_planilha.py (source-of-truth)"
echo "    • build_panorama.py (gerador de HTML)"
echo "    • index.html (output publicado)"
git add _PADRAO_FASE_1/gerar_planilha.py
git add build_panorama.py
git add index.html

echo ""
echo "▸ Commit: \"$MSG\""
git commit -m "$MSG"

echo ""
echo "▸ Enviando para GitHub..."
git push

echo ""
echo "✓ Publicado. GitHub Pages atualiza em 1-2 minutos."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
