#!/usr/bin/env bash
# ─── DOM Incorporação · Publish Panorama ──────────────────────────────────
# 1. Limpa locks travados de runs anteriores (defesa contra index.lock órfão)
# 2. Regenera Planilha Mestre via gerar_planilha.py (source of truth)
# 3. Regenera index.html via build_panorama.py
# 4. Commit pacote completo + push
#
# Política v2.0 do PADRAO: tracking permissivo (.xlsx commitada, sem .gitignore
# restritivo). Uso:  ./publish.sh "Mensagem opcional do commit"
# ──────────────────────────────────────────────────────────────────────────
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

MSG="${1:-Atualização do Panorama $(date +%d/%m/%Y)}"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  DOM · Panorama de Lançamentos · Publish"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 0. Limpa locks travados (sandbox às vezes deixa órfãos quando crash)
if [ -f .git/index.lock ] || [ -f .git/HEAD.lock ]; then
    echo "▸ Limpando locks órfãos do git..."
    rm -f .git/index.lock .git/HEAD.lock
fi

# 1. Regenera Planilha Mestre a partir do source-of-truth (gerar_planilha.py)
echo "▸ Regenerando Planilha Mestre (gerar_planilha.py)..."
python3 _PADRAO_FASE_1/gerar_planilha.py

# 2. Regenera o HTML a partir da Planilha Mestre mais recente
echo ""
echo "▸ Regenerando index.html (build_panorama.py)..."
python3 build_panorama.py

# 3. Adiciona pacote completo ao git (tracking permissivo)
echo ""
echo "▸ Adicionando arquivos ao git..."
git add _PADRAO_FASE_1/PADRAO.md
git add _PADRAO_FASE_1/gerar_planilha.py
git add _PADRAO_FASE_1/assets/ 2>/dev/null || true  # v6.5: logos locais (auto-suficiência)
git add build_panorama.py
git add publish.sh
git add .gitignore
git add ESTADO_ATUAL.md 2>/dev/null || true        # v6.5: declarativo de bootstrap (PADRAO §0.4)
git add "Planilha_Mestre_Panorama_v"*.xlsx 2>/dev/null || true
git add index.html
git add dom_logo.png 2>/dev/null || true  # logo embutido no HTML como data URI

# 4. Verifica se há algo realmente novo
if git diff --cached --quiet; then
    echo ""
    echo "✓ Nada a publicar (sem mudanças)."
    exit 0
fi

echo ""
echo "▸ Commit: \"$MSG\""
git commit -m "$MSG"

echo ""
echo "▸ Enviando para GitHub..."
git push

echo ""
echo "✓ Publicado. GitHub Pages atualiza em 1-2 minutos."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
