#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_panorama.py
─────────────────────────────────────────────────────────────────────────────
Gera o dashboard HTML "Panorama de Lançamentos — Grande São Luís" a partir
da Planilha Mestre de Inteligência de Mercado da DOM Incorporação.

Fluxo:
  1. Localiza a versão mais recente de `Planilha_Mestre_Panorama_v*.xlsx`
  2. Lê a aba "Empreendimentos"
  3. Filtra lançamentos 2025/2026 (ou em comercialização nesse ciclo)
  4. Geocodifica cada empreendimento por bairro (coordenadas aproximadas)
  5. Gera o arquivo `Panorama_Lancamentos_2025_2026.html` na pasta raiz

Uso:
    python3 build_panorama.py
    python3 build_panorama.py --all   # Inclui todos (não filtra por ciclo)

Autor: DOM Incorporação · Inteligência de Mercado
─────────────────────────────────────────────────────────────────────────────
"""
from __future__ import annotations
import argparse
import json
import math
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl não instalado. Rode: pip install openpyxl --break-system-packages")


# ─── Caminhos ────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_HTML = SCRIPT_DIR / "index.html"  # nome padrão do GitHub Pages

def discover_search_dirs() -> list[Path]:
    """
    Descobre dinamicamente as pastas candidatas onde a Planilha Mestre pode estar.
    Resolve problema de normalização Unicode (NFD vs NFC) no macOS procurando
    irmãos da pasta do script pelo padrão "01.*" + subpasta "00_ESTUDO_CONSOLIDADO".
    """
    dirs: list[Path] = []
    parent = SCRIPT_DIR.parent
    # 1. Procura pasta irmã "01.*" (Inteligência Mercado numerada)
    for sibling in parent.iterdir():
        if sibling.is_dir() and sibling.name.startswith("01."):
            estudo = sibling / "00_ESTUDO_CONSOLIDADO"
            if estudo.exists():
                dirs.append(estudo)
            dirs.append(sibling)
    # 2. Subpasta no próprio diretório do script
    local_estudo = SCRIPT_DIR / "00_ESTUDO_CONSOLIDADO"
    if local_estudo.exists():
        dirs.append(local_estudo)
    # 3. Diretório do script como último recurso
    dirs.append(SCRIPT_DIR)
    return dirs


# ─── Coordenadas aproximadas de bairros de São Luís/MA ───────────────────────
COORDS_BAIRRO = {
    # São Luís / MA — coordenadas no CENTRO geográfico de cada bairro (em terra firme).
    # Metodologia: afastado no mínimo ~400m da linha de costa ou rio,
    # priorizando áreas densamente urbanizadas.
    "Calhau":            (-2.5030, -44.2740),
    "Renascença":        (-2.5085, -44.2945),
    "Renascença II":     (-2.5110, -44.2965),
    "Jardim Renascença": (-2.5090, -44.2830),
    "Ponta d'Areia":     (-2.4985, -44.3000),
    "Ponta D'Areia":     (-2.4985, -44.3000),
    "Ponta do Farol":    (-2.4925, -44.2960),
    "São Marcos":        (-2.5030, -44.2855),
    "Cohama":            (-2.5330, -44.2760),
    "Cohab Anil IV":     (-2.5535, -44.2655),
    "Anil":              (-2.5485, -44.2645),
    "Cohab Anil":        (-2.5535, -44.2655),
    "Jardim Eldorado":   (-2.5590, -44.2485),
    "Turú":              (-2.5620, -44.2515),
    "Cantinho do Céu":   (-2.5650, -44.2660),
    "Araçagi":           (-2.4920, -44.2200),
    "Araçagy":           (-2.4920, -44.2200),
    "São Francisco":     (-2.5285, -44.3000),
    "Maranhão Novo":     (-2.5585, -44.2810),
    "Santo Amaro":       (-2.5635, -44.2685),
    "Cohatrac":          (-2.5685, -44.2280),
    "Iguaíba":           (-2.5730, -44.3580),
    "São Luís":          (-2.5310, -44.3068),
}

# Overrides de endereço-específico quando temos endereço preciso
COORDS_ENDERECO = {
    "Dom Lucas":            (-2.5665, -44.2675),
    "Dom José":             (-2.5594, -44.2492),
    "Edifício Bossa":       (-2.5002, -44.2788),
    "Al Mare Tirreno":      (-2.5018, -44.2870),
    "Le Noir":              (-2.5115, -44.2960),
    "Entre Rios":           (-2.5090, -44.2940),
    "Residencial Novo Anil":(-2.5540, -44.2660),
    "Edifício Sanpaolo":    (-2.5335, -44.2755),
}


# ─── Paleta DOM (cores por incorporadora no mapa) ────────────────────────────
INC_COLORS = {
    "Mota Machado":   "#B87333",  # bronze
    "Treviso":        "#8B2E2E",
    "Delman":         "#1B4584",
    "Canopus":        "#5D6E3C",
    "Berg Engenharia":"#6A4C93",
    "Niágara":        "#0F7B6C",
    "Castelucci":     "#A0522D",
    "Alfa Engenharia":"#2F4858",
    "Monteplan":      "#D17A22",
    "Sá Cavalcante":  "#7A2E7C",
    "Ergus":          "#3E6B93",
    "Lua Nova":       "#BA5A31",
    "Franere":        "#4D4D4D",
    "MB Engenharia":  "#8C8C8C",
    "DOM Incorporação":"#C9A84C",  # DOURADO DOM (marca da casa — destaque)
    "Hiali":          "#8C3B4A",  # vinho/bordô
}


# ─── Utilidades ──────────────────────────────────────────────────────────────
def find_latest_planilha() -> Path:
    """Busca a Planilha_Mestre_Panorama_v*.xlsx mais recente."""
    search_dirs = discover_search_dirs()
    candidates: list[Path] = []
    for d in search_dirs:
        if d.exists():
            for p in d.glob("Planilha_Mestre_Panorama_v*.xlsx"):
                candidates.append(p)
    if not candidates:
        sys.exit(
            "❌ Não encontrei nenhuma Planilha_Mestre_Panorama_v*.xlsx\n"
            f"   Busquei em: {[str(d) for d in search_dirs]}"
        )
    # Ordena por versão (extraindo X.Y.Z do nome)
    def version_key(p: Path) -> tuple:
        m = re.search(r"v(\d+)(?:\.(\d+))?(?:\.(\d+))?", p.stem)
        if not m:
            return (0, 0, 0, p.stat().st_mtime)
        parts = tuple(int(g) if g else 0 for g in m.groups())
        return parts + (p.stat().st_mtime,)
    candidates.sort(key=version_key, reverse=True)
    return candidates[0]


def parse_lancamento_sort(lancamento: str) -> int:
    """
    Converte string de lançamento em inteiro AAAAMM para ordenação cronológica.
    PADRAO v2.0 §1: formato esperado é SEMPRE MM/AAAA (com flag opcional ⚠ T-36).
    Exemplos:
        '04/2026'            → 202604
        '04/2025 ⚠ T-36'     → 202504
        '10/2025'            → 202510
        '—' / vazio          → 0 (faltam dados — vai para o fim da lista)
        'AAAA' puro          → 0 (formato inválido — força correção, vai pro fim)
    """
    if not lancamento or lancamento == "—":
        return 0
    s = str(lancamento).strip()
    # Aceita SOMENTE MM/AAAA (com ou sem ⚠ T-36)
    m = re.match(r"^(\d{1,2})/(\d{4})( ⚠ T-36)?$", s)
    if m:
        month, year = int(m.group(1)), int(m.group(2))
        return year * 100 + max(1, min(12, month))
    # Formato inválido (AAAA puro, ~AAAA, etc.) → empurrar pro fim
    # Sinaliza visualmente que falta dado preciso
    return 0


def geocode_bairro(bairro: str) -> tuple[float, float] | None:
    """
    Retorna (lat, lng) aproximados para o bairro, ou None se o bairro
    não puder ser identificado.

    Regras:
      - "São Luís" (placeholder genérico de bairro desconhecido) → None
      - Bairros vazios/nulos → None
      - Bairros mapeados → coordenadas conhecidas
      - Bairros não mapeados → tenta match parcial; se falhar → None
    """
    if not bairro:
        return None
    b = bairro.strip()
    # "São Luís" genérico = bairro não identificado
    if b.lower() in ("são luís", "sao luis", "são luís - ma", "—", "-"):
        return None
    # Busca exata
    if b in COORDS_BAIRRO:
        c = COORDS_BAIRRO[b]
        # Ignora se o match for o default "São Luís"
        return c if b != "São Luís" else None
    # Busca case-insensitive / aproximada
    for key, coord in COORDS_BAIRRO.items():
        if key == "São Luís":
            continue  # nunca usar como match aproximado
        if key.lower() == b.lower():
            return coord
        if key.lower() in b.lower() or b.lower() in key.lower():
            return coord
    return None


# ─── Parse de data de lançamento ─────────────────────────────────────────────
def parse_lancamento(raw: str, orig_col: str = "") -> tuple[str, str]:
    """
    Normaliza a string de "Mês lançamento" e deriva a Origem da informação.

    Retorna (data_formatada, origem):
      - '04/2026'           → ('04/2026', 'Tabela')
      - '10/2025'           → ('10/2025', 'Tabela')
      - '2026'              → ('2026',    'Book')
      - '~2026'             → ('2026',    'Estimado')
      - '~2025'             → ('2025',    'Estimado')
      - '04/2025 ⚠ T-36'    → ('04/2025', 'T-36')
      - '—' ou vazio        → ('—',      '—')

    `orig_col` = valor da coluna "Orig. lançamento" (imprensa/book/tabela),
    usado como fonte primária quando disponível.
    """
    if not raw or str(raw).strip() in ("—", "-", ""):
        # Data vazia — respeita origem informada (ex: 'pendente', 'estimado-fraco')
        if orig_col and str(orig_col).strip() not in ("", "—", "N/A"):
            origem = str(orig_col).strip().title()
            return ("—", origem)
        return ("—", "—")
    s = str(raw).strip()

    # Identificar origem a partir de marcadores no texto
    is_approx = "~" in s
    is_t36 = "T-36" in s or "t-36" in s

    # Extrair data normalizada
    m_full = re.search(r"(\d{1,2})/(\d{4})", s)
    if m_full:
        mo, yr = int(m_full.group(1)), int(m_full.group(2))
        data_fmt = f"{mo:02d}/{yr}"
    else:
        m_year = re.search(r"(\d{4})", s)
        data_fmt = m_year.group(1) if m_year else s

    # Definir origem com a seguinte prioridade:
    # 1. T-36 (marcador explícito no texto — forma mais crua)
    # 2. Estimado (marcador ~)
    # 3. Valor da coluna "Orig. lançamento" da planilha
    # 4. Fallback: "Book" (se só tem ano) ou "Tabela" (se tem MM/AAAA)
    if is_t36:
        origem = "T-36"
    elif is_approx:
        origem = "Estimado"
    elif orig_col and str(orig_col).strip() not in ("", "—", "N/A"):
        oc = str(orig_col).strip().lower()
        mapping = {
            "tabela": "Tabela",
            "book": "Book",
            "imprensa": "Imprensa",
            "site": "Site",
        }
        origem = mapping.get(oc, str(orig_col).strip().title())
    elif m_full:
        origem = "Tabela"
    else:
        origem = "Book"
    return (data_fmt, origem)


def should_include(row: dict, include_all: bool = False) -> bool:
    """
    Filtro: empreendimentos ATIVOS no mercado (ciclo 2025/2026).
    Inclui qualquer empreendimento:
      - lançado em 2025 ou 2026, OU
      - com status que indique venda ativa (Lançamento, Pré-lançamento,
        Em comercialização, Últimas unidades), independente do ano de lançamento.
    Exclui: Entregue/esgotado e explicitamente inativos.
    """
    if include_all:
        return True
    launch = str(row.get("Mês lançamento") or "")
    status = str(row.get("Status") or "").lower().strip()
    # Status que indicam comercialização ativa no ciclo atual
    active_statuses = {
        "lançamento", "pré-lançamento", "pre-lançamento",
        "em comercialização", "em comercializacao",
        "últimas unidades", "ultimas unidades",
    }
    if status in active_statuses:
        return True
    # Fallback: lançamento no ciclo 2025/2026
    if "2025" in launch or "2026" in launch:
        return True
    return False


# ─── Leitura da planilha ─────────────────────────────────────────────────────
def read_planilha(path: Path) -> list[dict]:
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Empreendimentos"]
    # Cabeçalho está na linha 5
    headers = [c.value for c in ws[5]]
    rows: list[dict] = []
    for r in range(6, ws.max_row + 1):
        row = {headers[i]: c.value for i, c in enumerate(ws[r])}
        if row.get("Incorporadora") and row.get("Empreendimento"):
            rows.append(row)
    return rows


def enrich(rows: list[dict], include_all: bool = False) -> list[dict]:
    """
    Retorna TODAS as linhas enriquecidas, com flag `is_active` indicando
    quais são ativas no ciclo atual (atendem a `should_include`).
    A UI usa `is_active` para filtrar a aba Panorama, mas a aba Dados
    Completos mostra todos.
    """
    bairro_count: dict = defaultdict(int)
    enriched: list[dict] = []
    for r in rows:
        is_active = should_include(r, include_all)
        bairro_raw = r.get("Bairro")
        bairro = str(bairro_raw).strip() if bairro_raw else ""
        emp_name = str(r.get("Empreendimento") or "").strip()
        # Prioriza coordenada por endereço (quando conhecida) sobre bairro
        if emp_name in COORDS_ENDERECO:
            coord = COORDS_ENDERECO[emp_name]
        else:
            coord = geocode_bairro(bairro)

        # Se o bairro não foi identificado, não coloca no mapa (lat/lng = None)
        lat_j: float | None = None
        lng_j: float | None = None
        on_map = False
        if coord is not None:
            lat, lng = coord
            # Jitter em espiral para não sobrepor markers do mesmo bairro
            idx = bairro_count[bairro]
            r_off = 0.0008 * idx   # reduzido: 220m → 88m (evita pin fora do bairro)
            theta = idx * 2.4
            lat_j = round(lat + r_off * math.cos(theta), 5)
            lng_j = round(lng + r_off * math.sin(theta), 5)
            bairro_count[bairro] += 1
            on_map = True

        lancamento_raw = str(r.get("Mês lançamento") or "—")
        orig_col = r.get("Orig. lançamento") or ""
        data_fmt, origem = parse_lancamento(lancamento_raw, orig_col)

        # Label do bairro para a UI: se não for identificado, explicitamos
        bairro_label = bairro if on_map else (bairro if bairro and bairro.lower() not in ("são luís", "sao luis") else "Não identificado")

        enriched.append({
            "incorporadora":  r.get("Incorporadora"),
            "empreendimento": r.get("Empreendimento"),
            "endereco":       r.get("Endereço") or "",
            "bairro":         bairro_label,
            "tipo":           r.get("Tipo") or "—",
            "segmento":       r.get("Segmento") or "—",
            "status":         r.get("Status") or "—",
            "unidades":       r.get("Nº unid."),
            "lancamento":     data_fmt,
            "lancamento_origem": origem,
            "lancamento_raw": lancamento_raw,
            "lancamento_sort": parse_lancamento_sort(lancamento_raw),
            "entrega":        str(r.get("Mês entrega") or "—"),
            "area_min":       r.get("Área mín (m²)"),
            "area_max":       r.get("Área máx (m²)"),
            "area_med":       r.get("Tipologia média (m²)"),
            "dorms":          r.get("Tipologia (dorms)") or "—",
            "ticket_min":     r.get("Ticket mín (R$)"),
            "ticket_max":     r.get("Ticket máx (R$)"),
            "rsm2":           r.get("R$/m²"),
            "vgv":            r.get("VGV (R$)"),
            "vendido":        r.get("% Vendido"),
            "orig_precos":    r.get("Orig. preços") or "—",
            "orig_estoque":   r.get("Orig. estoque") or "—",
            "orig_lancamento": r.get("Orig. lançamento") or "—",
            "link":           r.get("Link fonte principal") or "",
            "data_verif":     str(r.get("Data verif.") or "—"),
            "obs":            r.get("Observações") or "",
            "lat":            lat_j,
            "lng":            lng_j,
            "on_map":         on_map,
            "is_active":      is_active,
        })
    # Ordena cronologicamente (mais recente primeiro)
    enriched.sort(key=lambda e: e["lancamento_sort"], reverse=True)
    return enriched


# ─── Template HTML (mantém identidade visual DOM) ────────────────────────────
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<title>DOM Incorporação — Panorama de Lançamentos Grande São Luís</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  :root {
    --dom-black: #000000; --dom-gray-dark: #4D4D4D; --dom-gray-mid: #8C8C8C;
    --dom-gray-light: #F2F2F2; --dom-white: #FFFFFF;
    --dom-gold: #C9A84C; --dom-gold-light: #E8D5A3; --dom-gold-dark: #8B6914;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Calibri', 'Arial', sans-serif; background: var(--dom-gray-light); color: var(--dom-gray-dark); line-height: 1.5; }
  .hero { background: var(--dom-black); color: var(--dom-white); padding: 32px 40px 28px; border-bottom: 4px solid var(--dom-gold); }
  .hero-inner { max-width: 1400px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; }
  .hero-brand { display: flex; align-items: center; gap: 20px; }
  .hero-logo { height: 60px; width: auto; }
  .hero h1 { font-size: 24px; font-weight: 700; letter-spacing: 2px; color: var(--dom-white); }
  .hero h1 .gold { color: var(--dom-gold); }
  .hero .subtitle { font-size: 13px; color: var(--dom-gold); margin-top: 4px; letter-spacing: 1px; text-transform: uppercase; }
  .hero .meta { font-size: 12px; color: var(--dom-gray-mid); text-align: right; }
  .container { max-width: 1400px; margin: 0 auto; padding: 24px 40px; }
  .kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }
  .kpi { background: var(--dom-white); border-left: 4px solid var(--dom-gold); padding: 18px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
  .kpi .label { font-size: 11px; color: var(--dom-gray-mid); text-transform: uppercase; letter-spacing: 1.2px; }
  .kpi .value { font-size: 26px; font-weight: 700; color: var(--dom-black); margin-top: 6px; }
  .kpi .unit { font-size: 13px; color: var(--dom-gray-dark); margin-left: 4px; font-weight: 400; }
  .kpi.highlight { background: var(--dom-black); color: var(--dom-white); border-left-color: var(--dom-gold); }
  .kpi.highlight .value { color: var(--dom-gold); } .kpi.highlight .label { color: var(--dom-gold-light); } .kpi.highlight .unit { color: var(--dom-white); }
  .filters { background: var(--dom-white); padding: 16px 20px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); display: flex; flex-wrap: wrap; gap: 14px; align-items: center; }
  .filters label { font-size: 11px; color: var(--dom-gray-mid); text-transform: uppercase; letter-spacing: 0.8px; display: block; margin-bottom: 4px; }
  .filters select, .filters input { padding: 8px 12px; border: 1px solid var(--dom-gray-mid); font-family: inherit; font-size: 13px; color: var(--dom-gray-dark); background: var(--dom-white); min-width: 160px; }
  .filters select:focus, .filters input:focus { outline: 2px solid var(--dom-gold); border-color: var(--dom-gold); }
  .filter-group { display: flex; flex-direction: column; }
  .reset-btn { padding: 10px 18px; background: var(--dom-black); color: var(--dom-gold); border: none; cursor: pointer; font-family: inherit; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; font-weight: 700; margin-top: 15px; transition: all 0.2s; }
  .reset-btn:hover { background: var(--dom-gold); color: var(--dom-black); }
  .results-count { margin-left: auto; font-size: 12px; color: var(--dom-gray-dark); margin-top: 15px; }
  .results-count strong { color: var(--dom-gold-dark); font-size: 14px; }
  #map { height: 480px; margin-bottom: 24px; border: 2px solid var(--dom-black); box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
  .leaflet-popup-content-wrapper { border-radius: 0; border-left: 3px solid var(--dom-gold); }
  .leaflet-popup-content { margin: 12px 14px; font-family: 'Calibri', Arial, sans-serif; font-size: 13px; color: var(--dom-gray-dark); min-width: 200px; }
  .leaflet-popup-content .pop-title { font-weight: 700; color: var(--dom-black); font-size: 14px; margin-bottom: 4px; }
  .leaflet-popup-content .pop-inc { color: var(--dom-gold-dark); font-size: 11px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
  .leaflet-popup-content .pop-field { font-size: 12px; margin-top: 2px; }
  .leaflet-popup-content .pop-field strong { color: var(--dom-gray-dark); }
  .table-wrap { background: var(--dom-white); box-shadow: 0 1px 3px rgba(0,0,0,0.08); overflow-x: auto; }
  .table-header { background: var(--dom-black); color: var(--dom-white); padding: 14px 20px; font-weight: 700; font-size: 14px; letter-spacing: 1.5px; text-transform: uppercase; border-bottom: 3px solid var(--dom-gold); }
  table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
  thead tr { background: var(--dom-gray-dark); color: var(--dom-white); }
  thead th { padding: 12px 10px; text-align: left; font-weight: 700; font-size: 11px; letter-spacing: 0.8px; text-transform: uppercase; border-bottom: 2px solid var(--dom-gold); cursor: pointer; user-select: none; position: sticky; top: 0; }
  thead th:hover { background: var(--dom-black); }
  thead th.sorted::after { content: ' ▼'; color: var(--dom-gold); font-size: 9px; }
  thead th.sorted.asc::after { content: ' ▲'; }
  tbody tr { border-bottom: 1px solid var(--dom-gray-light); transition: background 0.15s; }
  tbody tr:nth-child(even) { background: var(--dom-gray-light); }
  tbody tr:hover { background: var(--dom-gold-light); cursor: pointer; }
  tbody td { padding: 10px; vertical-align: middle; }
  .chip { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 10.5px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
  .chip.seg-luxo { background: var(--dom-black); color: var(--dom-gold); }
  .chip.seg-alto { background: var(--dom-gold); color: var(--dom-black); }
  .chip.seg-medioalto { background: var(--dom-gold-light); color: var(--dom-gold-dark); }
  .chip.seg-medio { background: var(--dom-gray-mid); color: var(--dom-white); }
  .chip.seg-popular { background: #B8DBC5; color: #1F5138; }
  .chip.seg-other { background: var(--dom-gray-light); color: var(--dom-gray-dark); }
  .chip.st-lancamento { background: #FFE4A8; color: #7A5500; }
  .chip.st-pre { background: #E8D5A3; color: var(--dom-gold-dark); }
  .chip.st-comerc { background: #C3DAF9; color: #1B4584; }
  .chip.st-ultimas { background: #F7C8C8; color: #8C2525; }
  /* Origem da data — formatação minimalista com graduação de confiança */
  .origem { display: inline-block; font-size: 10.5px; padding: 1px 7px 1px 8px; border-radius: 3px; color: var(--dom-gray-dark); border-left: 3px solid var(--dom-gray-mid); background: #FAFAF5; font-variant: small-caps; letter-spacing: 0.3px; }
  .origem.strong { border-left-color: var(--dom-black); color: var(--dom-black); font-weight: 600; }
  .origem.medium { border-left-color: var(--dom-gold); color: var(--dom-gold-dark); }
  .origem.weak   { border-left-color: var(--dom-gray-mid); color: var(--dom-gray-mid); font-style: italic; }
  .origem.pending{ border-left-color: #B54B3A; color: #B54B3A; font-weight: 600; }
  .origem-legend { display: flex; flex-wrap: wrap; gap: 10px 18px; padding: 10px 14px; background: #FAFAF5; border-left: 3px solid var(--dom-gold); margin-top: 8px; font-size: 11px; color: var(--dom-gray-dark); }
  .origem-legend strong { color: var(--dom-black); font-size: 11px; letter-spacing: 0.5px; margin-right: 4px; }
  .origem-legend .item { display: inline-flex; align-items: center; gap: 6px; }
  .chip.tp-vertical   { background: #3B4371; color: #FFFFFF; }
  .chip.tp-horizontal { background: #5D7A3C; color: #FFFFFF; }
  .chip.tp-other      { background: var(--dom-gray-light); color: var(--dom-gray-dark); }
  .table-intro { background: var(--dom-white); padding: 14px 20px; font-size: 12px; color: var(--dom-gray-dark); border-left: 3px solid var(--dom-gold); margin-top: 18px; margin-bottom: 0; }
  .table-intro strong { color: var(--dom-gold-dark); }
  .table-intro.incomplete { border-left-color: #B54B3A; }
  .table-intro.incomplete strong { color: #B54B3A; }
  .nomap-badge { font-size: 9.5px; color: var(--dom-gray-mid); font-style: italic; margin-left: 6px; letter-spacing: 0.5px; }
  .nomap-note { display: none; background: var(--dom-white); padding: 10px 16px; margin-bottom: 12px; font-size: 11.5px; color: var(--dom-gray-dark); border-left: 3px solid var(--dom-gray-mid); }
  .nomap-note.show { display: block; }
  .nomap-note strong { color: var(--dom-gray-dark); }
  .inc-name { font-weight: 700; color: var(--dom-black); }
  .emp-name { font-weight: 700; color: var(--dom-gold-dark); }
  .price { font-variant-numeric: tabular-nums; color: var(--dom-black); font-weight: 600; }
  .dim { color: var(--dom-gray-mid); font-size: 11.5px; }
  .legend { display: flex; gap: 20px; flex-wrap: wrap; background: var(--dom-white); padding: 12px 20px; margin-bottom: 12px; font-size: 11.5px; border-left: 3px solid var(--dom-gold); }
  .legend-item { display: flex; align-items: center; gap: 6px; }
  .legend-dot { width: 12px; height: 12px; border-radius: 50%; border: 2px solid var(--dom-white); box-shadow: 0 0 0 1px var(--dom-gray-mid); }
  .footer { text-align: center; padding: 20px; font-size: 11px; color: var(--dom-gray-mid); border-top: 1px solid var(--dom-gray-mid); margin-top: 32px; }
  .footer strong { color: var(--dom-gold-dark); }
  /* Tab navigation */
  .tabs { background: var(--dom-black); border-bottom: 3px solid var(--dom-gold); }
  .tabs-inner { max-width: 1400px; margin: 0 auto; padding: 0 40px; display: flex; gap: 2px; }
  .tab-btn { background: transparent; color: var(--dom-gray-mid); border: none; padding: 16px 28px; font-family: inherit; font-size: 12px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; cursor: pointer; border-bottom: 3px solid transparent; margin-bottom: -3px; transition: all 0.2s; }
  .tab-btn:hover { color: var(--dom-gold-light); }
  .tab-btn.active { color: var(--dom-gold); border-bottom-color: var(--dom-gold); }
  .tab-btn .count { font-size: 10px; opacity: 0.7; margin-left: 6px; font-weight: 400; }
  .tab-panel { display: none; }
  .tab-panel.active { display: block; }
  /* Compact table for Dados Completos */
  .tbl-compact table { font-size: 11.5px; }
  .tbl-compact thead th { padding: 10px 8px; font-size: 10px; white-space: nowrap; }
  .tbl-compact tbody td { padding: 8px; white-space: nowrap; }
  .tbl-compact tbody td.wrap { white-space: normal; min-width: 180px; }
  .tbl-compact { overflow-x: auto; max-height: 75vh; }
  @media (max-width: 768px) {
    .hero { padding: 20px; } .hero h1 { font-size: 20px; } .container { padding: 16px; }
    #map { height: 350px; } table { font-size: 11px; } thead th, tbody td { padding: 8px 6px; }
    .tabs-inner { padding: 0 16px; } .tab-btn { padding: 12px 16px; font-size: 11px; }
  }
</style>
</head>
<body>
<header class="hero">
  <div class="hero-inner">
    <div class="hero-brand">
      <img class="hero-logo" src="__LOGO_B64__" alt="DOM Incorporação" />
      <div>
        <h1>INTELIGÊNCIA DE MERCADO</h1>
        <div class="subtitle">Panorama de Lançamentos — Grande São Luís · __CICLO__</div>
      </div>
    </div>
    <div class="meta">
      Atualizado em __DATA_UPDATE__<br>
      <span style="color: var(--dom-gold);">__VERSAO__ · Fase 2 — Dashboard Interativo</span>
    </div>
  </div>
</header>
<nav class="tabs">
  <div class="tabs-inner">
    <button class="tab-btn active" data-tab="panorama">Panorama <span class="count" id="tab-count-panorama">—</span></button>
    <button class="tab-btn" data-tab="dados">Dados Completos <span class="count" id="tab-count-dados">—</span></button>
  </div>
</nav>
<main class="container">
  <!-- TAB: PANORAMA -->
  <div class="tab-panel active" id="tab-panorama">
  <section class="kpis" id="kpis">
    <div class="kpi highlight"><div class="label">Empreendimentos</div><div class="value" id="kpi-count">—</div></div>
    <div class="kpi"><div class="label">Incorporadoras</div><div class="value" id="kpi-inc">—</div></div>
    <div class="kpi"><div class="label">Ticket médio</div><div class="value" id="kpi-ticket">—<span class="unit">R$</span></div></div>
    <div class="kpi"><div class="label">R$/m² médio</div><div class="value" id="kpi-rsm2">—<span class="unit">R$</span></div></div>
    <div class="kpi"><div class="label">VGV somado</div><div class="value" id="kpi-vgv">—<span class="unit">R$</span></div></div>
  </section>
  <section class="filters">
    <div class="filter-group"><label>Incorporadora</label><select id="f-inc"><option value="">Todas</option></select></div>
    <div class="filter-group"><label>Bairro</label><select id="f-bairro"><option value="">Todos</option></select></div>
    <div class="filter-group"><label>Segmento</label><select id="f-seg"><option value="">Todos</option></select></div>
    <div class="filter-group"><label>Ano lançamento</label><select id="f-ano"><option value="">Todos</option></select></div>
    <div class="filter-group"><label>Busca</label><input type="text" id="f-search" placeholder="Nome do empreendimento..." /></div>
    <button class="reset-btn" onclick="resetFilters()">Limpar Filtros</button>
    <div class="results-count"><strong id="res-count">0</strong> de <span id="res-total">0</span> empreendimentos</div>
  </section>
  <section class="legend" id="legend"></section>
  <section class="nomap-note" id="nomap-note"></section>
  <section id="map"></section>
  <div class="origem-legend">
    <strong>Origem da data:</strong>
    <span class="item"><span class="origem strong">memorial</span> registro em cartório (prova legal)</span>
    <span class="item"><span class="origem strong">interno</span> confirmado pela incorporadora (DOM)</span>
    <span class="item"><span class="origem medium">T-36</span> estimativa: entrega menos 36 meses</span>
    <span class="item"><span class="origem medium">book</span> data do book de vendas</span>
    <span class="item"><span class="origem medium">informado</span> fonte externa confiável, sem arquivo documental</span>
    <span class="item"><span class="origem weak">imprensa/site</span> menção pública, estimativa fraca</span>
    <span class="item"><span class="origem weak">estimado-fraco</span> data histórica preservada, sem evidência forte</span>
    <span class="item"><span class="origem pending">pendente</span> sem evidência — buscar tabela</span>
  </div>
  <div class="table-intro">
    <strong>📊 Tabela A — Empreendimentos com dados completos</strong> · com área, ticket e R$/m² confirmados (<strong id="cnt-complete">—</strong>)
  </div>
  <section class="table-wrap">
    <table id="tbl">
      <thead><tr>
        <th data-col="incorporadora">Incorporadora</th>
        <th data-col="empreendimento">Empreendimento</th>
        <th data-col="bairro">Bairro</th>
        <th data-col="tipo">Tipo</th>
        <th data-col="segmento">Segmento</th>
        <th data-col="lancamento_sort">Lançamento</th>
        <th data-col="lancamento_origem">Origem data</th>
        <th data-col="area_med">Área méd (m²)</th>
        <th data-col="ticket_med">Ticket (R$)</th>
        <th data-col="rsm2">R$/m²</th>
      </tr></thead>
      <tbody id="tbody"></tbody>
    </table>
  </section>

  <div class="table-intro incomplete">
    <strong>🔎 Tabela B — Faltam dados (área / ticket / R$/m²)</strong> · <strong id="cnt-incomplete">—</strong> empreendimento(s) — <em>priorizar buscar tabela com corretor/site</em>
  </div>
  <section class="table-wrap">
    <table id="tbl-b">
      <thead><tr>
        <th data-col="incorporadora">Incorporadora</th>
        <th data-col="empreendimento">Empreendimento</th>
        <th data-col="bairro">Bairro</th>
        <th data-col="tipo">Tipo</th>
        <th data-col="segmento">Segmento</th>
        <th data-col="lancamento_sort">Lançamento</th>
        <th data-col="lancamento_origem">Origem data</th>
        <th data-col="pendencias">O que falta</th>
      </tr></thead>
      <tbody id="tbody-b"></tbody>
    </table>
  </section>
  </div><!-- /tab-panorama -->

  <!-- TAB: DADOS COMPLETOS -->
  <div class="tab-panel" id="tab-dados">
    <section class="filters" style="margin-top:8px;">
      <div class="filter-group"><label>Busca</label><input type="text" id="fd-search" placeholder="Buscar em qualquer coluna..." style="min-width:280px"/></div>
      <div class="filter-group"><label>Incorporadora</label><select id="fd-inc"><option value="">Todas</option></select></div>
      <div class="filter-group"><label>Status</label><select id="fd-status"><option value="">Todos</option></select></div>
      <div class="results-count"><strong id="fd-res-count">0</strong> de <span id="fd-res-total">0</span> linhas</div>
    </section>
    <section class="table-wrap tbl-compact">
      <div class="table-header">Dados Completos · Reflete todas as colunas da Planilha Mestre</div>
      <table id="tbl-full">
        <thead><tr>
          <th data-col="incorporadora">Incorporadora</th>
          <th data-col="empreendimento">Empreendimento</th>
          <th data-col="endereco">Endereço</th>
          <th data-col="bairro">Bairro</th>
          <th data-col="tipo">Tipo</th>
          <th data-col="segmento">Segmento</th>
          <th data-col="status">Status</th>
          <th data-col="unidades">Nº unid.</th>
          <th data-col="lancamento_sort">Lançamento</th>
          <th data-col="entrega">Entrega</th>
          <th data-col="area_min">Área mín</th>
          <th data-col="area_max">Área máx</th>
          <th data-col="area_med">Área méd</th>
          <th data-col="dorms">Dorms</th>
          <th data-col="ticket_min">Ticket mín</th>
          <th data-col="ticket_max">Ticket máx</th>
          <th data-col="rsm2">R$/m²</th>
          <th data-col="vgv">VGV</th>
          <th data-col="vendido">% Vendido</th>
          <th data-col="orig_precos">Orig. preços</th>
          <th data-col="orig_estoque">Orig. estoque</th>
          <th data-col="orig_lancamento">Orig. lançamento</th>
          <th data-col="data_verif">Data verif.</th>
          <th data-col="obs">Observações</th>
        </tr></thead>
        <tbody id="tbody-full"></tbody>
      </table>
    </section>
  </div><!-- /tab-dados -->

  <div class="footer">
    <strong>DOM Incorporação</strong> · Inteligência de Mercado · São Luís/MA<br>
    Fonte: books e tabelas oficiais das incorporadoras · Gerado de __PLANILHA_NAME__
  </div>
</main>
<script>
const ALL_DATA = __DATA_PLACEHOLDER__;
const DATA = ALL_DATA.filter(e => e.is_active);  // Panorama = apenas ativos no ciclo
const INC_COLORS = __INC_COLORS_PLACEHOLDER__;
function getColor(inc) { return INC_COLORS[inc] || "#8C8C8C"; }
function formatBRL(v, compact=false) {
  if (v == null || v === '' || isNaN(v)) return '—';
  v = Number(v);
  if (compact) {
    if (v >= 1e9) return (v/1e9).toFixed(1).replace('.', ',') + ' bi';
    if (v >= 1e6) return (v/1e6).toFixed(1).replace('.', ',') + ' mi';
    if (v >= 1e3) return (v/1e3).toFixed(0) + ' mil';
  }
  return v.toLocaleString('pt-BR', {maximumFractionDigits: 0});
}
function formatArea(v) { if (v == null || isNaN(v)) return '—'; return Number(v).toLocaleString('pt-BR', {maximumFractionDigits: 1}); }
function segClass(seg) {
  if (!seg) return 'seg-other';
  const s = seg.toLowerCase();
  if (s.includes('luxo')) return 'seg-luxo';
  if (s.includes('médio-alto') || s.includes('medio-alto')) return 'seg-medioalto';
  if (s.includes('alto')) return 'seg-alto';
  if (s.includes('médio') || s.includes('medio')) return 'seg-medio';
  if (s.includes('popular')) return 'seg-popular';
  return 'seg-other';
}
function statusClass(st) {
  if (!st) return '';
  const s = st.toLowerCase();
  if (s.includes('pré')) return 'st-pre';
  if (s.includes('lançamento')) return 'st-lancamento';
  if (s.includes('comerc')) return 'st-comerc';
  if (s.includes('últimas')) return 'st-ultimas';
  return '';
}
function origemClass(o) {
  if (!o) return 'origem';
  const s = String(o).toLowerCase();
  if (s === 'memorial' || s === 'interno') return 'origem strong';
  if (s === 't-36' || s === 'book' || s === 'informado') return 'origem medium';
  if (s === 'pendente') return 'origem pending';
  return 'origem weak'; // imprensa, site, estimado-fraco, outros
}
function tipoClass(t) {
  if (!t) return 'tp-other';
  const s = String(t).toLowerCase();
  if (s.includes('horizontal')) return 'tp-horizontal';
  if (s.includes('vertical')) return 'tp-vertical';
  return 'tp-other';
}
function isComplete(e) {
  return e.area_med != null && e.ticket_min != null && e.ticket_max != null && e.rsm2 != null;
}
let map = null, markers = [];
function initMap() {
  if (typeof L === 'undefined') {
    const el = document.getElementById('map');
    el.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#8C8C8C;font-size:13px;background:#F2F2F2;border:1px dashed #8C8C8C;">Mapa indisponível (Leaflet não carregado). Verifique conexão com internet.</div>';
    el.style.height = '120px';
    return false;
  }
  map = L.map('map').setView([-2.51, -44.27], 12);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '© OpenStreetMap', maxZoom: 19}).addTo(map);
  return true;
}
function makeMarker(e) {
  // Pula se não estiver no mapa (bairro não identificado)
  if (!e.on_map || e.lat == null || e.lng == null) return null;
  if (!map || typeof L === 'undefined') return null;
  const color = getColor(e.incorporadora);
  const icon = L.divIcon({
    className: 'custom-marker',
    html: `<div style="background:${color};width:22px;height:22px;border-radius:50%;border:3px solid #fff;box-shadow:0 0 0 1.5px #000, 0 2px 4px rgba(0,0,0,0.3);"></div>`,
    iconSize: [22, 22], iconAnchor: [11, 11]
  });
  const marker = L.marker([e.lat, e.lng], {icon}).addTo(map);
  const ticket = (e.ticket_min && e.ticket_max) ? `R$ ${formatBRL(e.ticket_min, true)} – R$ ${formatBRL(e.ticket_max, true)}` : '—';
  const area = e.area_med ? formatArea(e.area_med) + ' m²' : (e.area_min && e.area_max ? formatArea(e.area_min)+'–'+formatArea(e.area_max)+' m²' : '—');
  marker.bindPopup(`
    <div class="pop-inc">${e.incorporadora}</div>
    <div class="pop-title">${e.empreendimento}</div>
    <div class="pop-field"><strong>Bairro:</strong> ${e.bairro}</div>
    <div class="pop-field"><strong>Segmento:</strong> ${e.segmento} · ${e.status}</div>
    <div class="pop-field"><strong>Lançamento:</strong> ${e.lancamento} <span style="color:#8B6914;font-size:10.5px;">(${e.lancamento_origem})</span></div>
    <div class="pop-field"><strong>Área:</strong> ${area}</div>
    <div class="pop-field"><strong>Ticket:</strong> ${ticket}</div>
    <div class="pop-field"><strong>R$/m²:</strong> ${e.rsm2 ? 'R$ ' + formatBRL(e.rsm2) : '—'}</div>
  `);
  return marker;
}
function populateFilters() {
  const incs = [...new Set(DATA.map(e => e.incorporadora))].sort();
  const bairros = [...new Set(DATA.map(e => e.bairro))].sort();
  const segs = [...new Set(DATA.map(e => e.segmento).filter(s => s && s !== '—'))].sort();
  // Extrai anos do campo lancamento (formato MM/AAAA ou AAAA)
  const anos = [...new Set(DATA.map(e => {
    if (!e.lancamento || e.lancamento === '—') return null;
    const m = String(e.lancamento).match(/(\d{4})/);
    return m ? m[1] : null;
  }).filter(Boolean))].sort().reverse(); // mais recentes primeiro
  const fillSel = (id, arr) => {
    const sel = document.getElementById(id);
    arr.forEach(v => { const o = document.createElement('option'); o.value = v; o.textContent = v; sel.appendChild(o); });
  };
  fillSel('f-inc', incs); fillSel('f-bairro', bairros); fillSel('f-seg', segs); fillSel('f-ano', anos);
}
function buildLegend() {
  const incs = [...new Set(DATA.map(e => e.incorporadora))].sort();
  document.getElementById('legend').innerHTML = incs.map(inc => `
    <div class="legend-item"><span class="legend-dot" style="background:${getColor(inc)}"></span><span>${inc} (${DATA.filter(e=>e.incorporadora===inc).length})</span></div>
  `).join('');
}
let sortCol = 'lancamento_sort';
let sortAsc = false;
function applyFilters() {
  const fi = document.getElementById('f-inc').value;
  const fb = document.getElementById('f-bairro').value;
  const fs = document.getElementById('f-seg').value;
  const fa = document.getElementById('f-ano').value;
  const fq = document.getElementById('f-search').value.toLowerCase();
  const filt = DATA.filter(e => {
    if (fi && e.incorporadora !== fi) return false;
    if (fb && e.bairro !== fb) return false;
    if (fs && e.segmento !== fs) return false;
    if (fa) {
      const m = String(e.lancamento || '').match(/(\d{4})/);
      if (!m || m[1] !== fa) return false;
    }
    if (fq && !(e.empreendimento.toLowerCase().includes(fq) || e.incorporadora.toLowerCase().includes(fq))) return false;
    return true;
  });
  renderTable(filt); renderMap(filt); renderKPIs(filt);
  document.getElementById('res-count').textContent = filt.length;
  document.getElementById('res-total').textContent = DATA.length;
}
function renderKPIs(data) {
  document.getElementById('kpi-count').textContent = data.length;
  document.getElementById('kpi-inc').textContent = new Set(data.map(e => e.incorporadora)).size;
  const tickets = data.flatMap(e => { const arr = []; if (e.ticket_min) arr.push(e.ticket_min); if (e.ticket_max) arr.push(e.ticket_max); return arr; });
  const tkMed = tickets.length ? tickets.reduce((a,b)=>a+b,0)/tickets.length : 0;
  document.getElementById('kpi-ticket').innerHTML = (tkMed ? formatBRL(tkMed, true) : '—') + ' <span class="unit">R$</span>';
  const rsm2 = data.map(e => e.rsm2).filter(v => v);
  const rMed = rsm2.length ? rsm2.reduce((a,b)=>a+b,0)/rsm2.length : 0;
  document.getElementById('kpi-rsm2').innerHTML = (rMed ? formatBRL(rMed) : '—') + ' <span class="unit">R$/m²</span>';
  const vgv = data.map(e => e.vgv).filter(v => v).reduce((a,b)=>a+b, 0);
  document.getElementById('kpi-vgv').innerHTML = (vgv ? formatBRL(vgv, true) : '—') + ' <span class="unit">R$</span>';
}
function renderMap(data) {
  if (!map) return;
  markers.forEach(m => m && map.removeLayer(m));
  markers = data.map(makeMarker).filter(Boolean);
  // Aviso sobre empreendimentos sem coordenadas
  const noMap = data.filter(e => !e.on_map);
  const note = document.getElementById('nomap-note');
  if (noMap.length > 0) {
    const names = noMap.map(e => `<strong>${e.empreendimento}</strong> (${e.incorporadora})`).join(', ');
    note.innerHTML = `📍 <strong>${noMap.length}</strong> empreendimento(s) sem bairro identificado, fora do mapa: ${names}.`;
    note.classList.add('show');
  } else {
    note.classList.remove('show');
  }
}
function renderTable(data) {
  const doSort = arr => [...arr].sort((a,b) => {
    let av = a[sortCol] ?? '';
    let bv = b[sortCol] ?? '';
    if (sortCol === 'ticket_med') { av = ((a.ticket_min||0) + (a.ticket_max||0))/2; bv = ((b.ticket_min||0) + (b.ticket_max||0))/2; }
    if (typeof av === 'number' && typeof bv === 'number') return sortAsc ? av-bv : bv-av;
    return sortAsc ? String(av).localeCompare(String(bv)) : String(bv).localeCompare(String(av));
  });

  // Divide em COMPLETOS e INCOMPLETOS
  const completos = doSort(data.filter(isComplete));
  const incompletos = doSort(data.filter(e => !isComplete(e)));

  // Contadores
  document.getElementById('cnt-complete').textContent = completos.length;
  document.getElementById('cnt-incomplete').textContent = incompletos.length;

  // Tabela A: completos
  document.getElementById('tbody').innerHTML = completos.map(e => {
    const ticket = `R$ ${formatBRL(e.ticket_min, true)}–${formatBRL(e.ticket_max, true)}`;
    const area = formatArea(e.area_med);
    const nomap = e.on_map ? '' : '<span class="nomap-badge" title="Empreendimento sem bairro identificado — não plotado no mapa">◌ fora do mapa</span>';
    return `
      <tr onclick="focusEmp('${e.empreendimento.replace(/'/g, "\\'")}')">
        <td><span class="inc-name" style="color:${getColor(e.incorporadora)}">●</span> <span class="inc-name">${e.incorporadora}</span></td>
        <td class="emp-name">${e.empreendimento}${nomap}</td>
        <td>${e.bairro}</td>
        <td><span class="chip ${tipoClass(e.tipo)}">${e.tipo}</span></td>
        <td><span class="chip ${segClass(e.segmento)}">${e.segmento}</span></td>
        <td class="price" style="font-weight:600">${e.lancamento}</td>
        <td><span class="${origemClass(e.lancamento_origem)}">${e.lancamento_origem}</span></td>
        <td class="price">${area}</td>
        <td class="price">${ticket}</td>
        <td class="price">R$ ${formatBRL(e.rsm2)}</td>
      </tr>
    `;
  }).join('');

  // Tabela B: incompletos — mostra o que está faltando
  document.getElementById('tbody-b').innerHTML = incompletos.map(e => {
    const nomap = e.on_map ? '' : '<span class="nomap-badge">◌ fora do mapa</span>';
    const faltam = [];
    if (e.area_med == null) faltam.push('área');
    if (e.ticket_min == null || e.ticket_max == null) faltam.push('ticket');
    if (e.rsm2 == null) faltam.push('R$/m²');
    return `
      <tr onclick="focusEmp('${e.empreendimento.replace(/'/g, "\\'")}')">
        <td><span class="inc-name" style="color:${getColor(e.incorporadora)}">●</span> <span class="inc-name">${e.incorporadora}</span></td>
        <td class="emp-name">${e.empreendimento}${nomap}</td>
        <td>${e.bairro}</td>
        <td><span class="chip ${tipoClass(e.tipo)}">${e.tipo}</span></td>
        <td><span class="chip ${segClass(e.segmento)}">${e.segmento}</span></td>
        <td class="dim">${e.lancamento}</td>
        <td><span class="${origemClass(e.lancamento_origem)}">${e.lancamento_origem}</span></td>
        <td><span class="chip or-pendente" title="Precisa buscar tabela">${faltam.join(' · ')}</span></td>
      </tr>
    `;
  }).join('');

  document.querySelectorAll('#tbl thead th, #tbl-b thead th').forEach(th => {
    th.classList.remove('sorted', 'asc');
    if (th.dataset.col === sortCol) { th.classList.add('sorted'); if (sortAsc) th.classList.add('asc'); }
  });
}
function focusEmp(name) {
  if (!map) return;
  const e = DATA.find(x => x.empreendimento === name);
  if (e && e.on_map && e.lat != null) {
    map.setView([e.lat, e.lng], 15);
    const m = markers.find(mk => mk.getLatLng().lat === e.lat && mk.getLatLng().lng === e.lng);
    if (m) m.openPopup();
  }
}
function resetFilters() {
  ['f-inc','f-bairro','f-seg','f-ano','f-search'].forEach(id => document.getElementById(id).value = '');
  applyFilters();
}
document.querySelectorAll('.filters select, .filters input').forEach(el => { el.addEventListener('input', applyFilters); el.addEventListener('change', applyFilters); });
document.querySelectorAll('#tbl thead th, #tbl-b thead th').forEach(th => {
  th.addEventListener('click', () => {
    const col = th.dataset.col;
    if (sortCol === col) sortAsc = !sortAsc; else { sortCol = col; sortAsc = false; }
    applyFilters();
  });
});
// ─── TAB: DADOS COMPLETOS ─────────────────────────────────────────────────
let sortColFull = 'lancamento_sort';
let sortAscFull = false;

function populateFullFilters() {
  const incs = [...new Set(ALL_DATA.map(e => e.incorporadora))].filter(Boolean).sort();
  const statuses = [...new Set(ALL_DATA.map(e => e.status).filter(s => s && s !== '—'))].sort();
  const fillSel = (id, arr) => {
    const sel = document.getElementById(id);
    arr.forEach(v => { const o = document.createElement('option'); o.value = v; o.textContent = v; sel.appendChild(o); });
  };
  fillSel('fd-inc', incs); fillSel('fd-status', statuses);
}

function cell(v, opts={}) {
  if (v == null || v === '' || v === '—') return '<span class="dim">—</span>';
  if (opts.currency) return 'R$ ' + formatBRL(v);
  if (opts.area) return formatArea(v);
  if (opts.pct && typeof v === 'number') return (v*100).toFixed(0) + '%';
  return String(v);
}

function applyFullFilters() {
  const fq = document.getElementById('fd-search').value.toLowerCase();
  const fi = document.getElementById('fd-inc').value;
  const fs = document.getElementById('fd-status').value;
  const filt = ALL_DATA.filter(e => {
    if (fi && e.incorporadora !== fi) return false;
    if (fs && e.status !== fs) return false;
    if (fq) {
      const blob = [e.incorporadora, e.empreendimento, e.endereco, e.bairro, e.segmento, e.status,
                    e.lancamento, e.entrega, e.dorms, e.orig_precos, e.orig_estoque, e.orig_lancamento,
                    e.data_verif, e.obs].filter(Boolean).join(' ').toLowerCase();
      if (!blob.includes(fq)) return false;
    }
    return true;
  });
  renderFullTable(filt);
  document.getElementById('fd-res-count').textContent = filt.length;
  document.getElementById('fd-res-total').textContent = ALL_DATA.length;
}

function renderFullTable(data) {
  const sorted = [...data].sort((a,b) => {
    let av = a[sortColFull] ?? '';
    let bv = b[sortColFull] ?? '';
    if (typeof av === 'number' && typeof bv === 'number') return sortAscFull ? av-bv : bv-av;
    if (av === null || av === undefined) av = '';
    if (bv === null || bv === undefined) bv = '';
    return sortAscFull ? String(av).localeCompare(String(bv)) : String(bv).localeCompare(String(av));
  });
  document.getElementById('tbody-full').innerHTML = sorted.map(e => `
    <tr>
      <td><span class="inc-name" style="color:${getColor(e.incorporadora)}">●</span> <strong>${e.incorporadora || '—'}</strong></td>
      <td class="emp-name">${e.empreendimento || '—'}</td>
      <td class="wrap dim">${e.endereco || '—'}</td>
      <td>${e.bairro || '—'}</td>
      <td>${e.tipo ? `<span class="chip ${tipoClass(e.tipo)}">${e.tipo}</span>` : '—'}</td>
      <td>${e.segmento ? `<span class="chip ${segClass(e.segmento)}">${e.segmento}</span>` : '—'}</td>
      <td>${e.status ? `<span class="chip ${statusClass(e.status)}">${e.status}</span>` : '—'}</td>
      <td class="price">${cell(e.unidades)}</td>
      <td class="price">${e.lancamento || '—'}</td>
      <td>${e.entrega || '—'}</td>
      <td class="price">${cell(e.area_min, {area:true})}</td>
      <td class="price">${cell(e.area_max, {area:true})}</td>
      <td class="price">${cell(e.area_med, {area:true})}</td>
      <td class="dim">${e.dorms || '—'}</td>
      <td class="price">${cell(e.ticket_min, {currency:true})}</td>
      <td class="price">${cell(e.ticket_max, {currency:true})}</td>
      <td class="price">${cell(e.rsm2, {currency:true})}</td>
      <td class="price">${cell(e.vgv, {currency:true})}</td>
      <td class="price">${cell(e.vendido, {pct:true})}</td>
      <td class="dim">${e.orig_precos || '—'}</td>
      <td class="dim">${e.orig_estoque || '—'}</td>
      <td class="dim">${e.orig_lancamento || '—'}</td>
      <td class="dim">${e.data_verif || '—'}</td>
      <td class="wrap dim" style="font-size:10.5px">${e.obs || '—'}</td>
    </tr>
  `).join('');
  document.querySelectorAll('#tbl-full thead th').forEach(th => {
    th.classList.remove('sorted', 'asc');
    if (th.dataset.col === sortColFull) { th.classList.add('sorted'); if (sortAscFull) th.classList.add('asc'); }
  });
}

document.querySelectorAll('#tab-dados .filters select, #tab-dados .filters input').forEach(el => {
  el.addEventListener('input', applyFullFilters); el.addEventListener('change', applyFullFilters);
});
document.querySelectorAll('#tbl-full thead th').forEach(th => {
  th.addEventListener('click', () => {
    const col = th.dataset.col;
    if (sortColFull === col) sortAscFull = !sortAscFull; else { sortColFull = col; sortAscFull = false; }
    applyFullFilters();
  });
});

// ─── Tab switcher ─────────────────────────────────────────────────────────
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    // Ajusta tamanho do mapa quando reabre Panorama
    if (btn.dataset.tab === 'panorama' && map) {
      setTimeout(() => map.invalidateSize(), 100);
    }
  });
});

// Contadores no topo das abas
document.getElementById('tab-count-panorama').textContent = DATA.length;
document.getElementById('tab-count-dados').textContent = ALL_DATA.length;

// Inicializa ambas
initMap(); populateFilters(); buildLegend(); applyFilters();
populateFullFilters(); applyFullFilters();
if (map) {
  const latlngs = DATA.filter(e => e.on_map && e.lat != null).map(e => [e.lat, e.lng]);
  if (latlngs.length > 0) map.fitBounds(latlngs, {padding: [40, 40]});
}
</script>
</body>
</html>"""


# ─── Pipeline ────────────────────────────────────────────────────────────────
def build(include_all: bool = False) -> None:
    from datetime import datetime
    print("─" * 70)
    print("DOM Incorporação · Inteligência de Mercado · build_panorama")
    print("─" * 70)

    planilha = find_latest_planilha()
    print(f"📊 Planilha: {planilha.name}")

    rows = read_planilha(planilha)
    print(f"📋 Linhas lidas: {len(rows)}")

    enriched = enrich(rows, include_all=include_all)
    active = [e for e in enriched if e.get("is_active")]
    print(f"📐 Total enriquecido: {len(enriched)} (aba Dados Completos)")
    print(f"🎯 Ativos no ciclo: {len(active)} (aba Panorama)")

    # Info por incorporadora (só ativos)
    from collections import Counter
    incs = Counter(e["incorporadora"] for e in active)
    print("   Por incorporadora (panorama):")
    for inc, n in incs.most_common():
        print(f"      {inc}: {n}")

    # Gera HTML
    data_json = json.dumps(enriched, ensure_ascii=False, separators=(",", ":"), default=str)
    inc_colors_json = json.dumps(INC_COLORS, ensure_ascii=False)
    version_match = re.search(r"v([\d.]+)", planilha.stem)
    version = "v" + version_match.group(1) if version_match else "v?"
    hoje = datetime.now().strftime("%d/%m/%Y")
    ciclo = "Todos os empreendimentos" if include_all else "2025/2026"

    # Carrega logo DOM como data URI para embutir no HTML
    logo_path = SCRIPT_DIR / "dom_logo.png"
    logo_b64 = ""
    if logo_path.exists():
        import base64
        logo_b64 = "data:image/png;base64," + base64.b64encode(logo_path.read_bytes()).decode('ascii')

    html = (HTML_TEMPLATE
            .replace("__DATA_PLACEHOLDER__", data_json)
            .replace("__INC_COLORS_PLACEHOLDER__", inc_colors_json)
            .replace("__VERSAO__", version)
            .replace("__DATA_UPDATE__", hoje)
            .replace("__CICLO__", ciclo)
            .replace("__PLANILHA_NAME__", planilha.name)
            .replace("__LOGO_B64__", logo_b64))

    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"\n✅ HTML gerado: {OUTPUT_HTML.name}")
    print(f"   Tamanho: {len(html):,} caracteres")
    print(f"   Caminho: {OUTPUT_HTML}")
    print("─" * 70)


def main():
    parser = argparse.ArgumentParser(description="Gera o Panorama de Lançamentos HTML")
    parser.add_argument("--all", action="store_true", help="Inclui todos os empreendimentos (sem filtro de ciclo)")
    args = parser.parse_args()
    build(include_all=args.all)


if __name__ == "__main__":
    main()
