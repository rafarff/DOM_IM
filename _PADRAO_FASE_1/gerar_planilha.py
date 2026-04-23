"""
gerar_planilha.py — Script ÚNICO da Fase 1 (Inteligência de Mercado DOM)
Padrão congelado em 14/04/2026. Ver PADRAO.md no mesmo diretório.

Regras:
  - Não criar variantes deste script (v11, v12, etc.). Versiona-se OS DADOS, não o código.
  - Não adicionar colunas ao template sem atualizar antes o PADRAO.md e obter aprovação.
  - Gerar: Planilha_Mestre_Panorama_vX.Y.xlsx em /00_ESTUDO_CONSOLIDADO/

Uso: python3 gerar_planilha.py
"""
import os, glob, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage

# ═══════════════════════════════════════════════════════════════
# PARÂMETROS GLOBAIS
# ═══════════════════════════════════════════════════════════════
VERSION = "4.2"
DATE_STR = "14/04/2026"
# v4.1 — Varredura web geral (14/04/2026): +13 novos empreend. mapeados via
# site oficial + Instagram + imprensa (Imirante, Diego Emir, MaHoje).
# Novos: Bossa (Mota Machado) atualizado; Giardino (Alfa); Villagio Treviso;
# Village Reserva II / Prime Eldorado / Del Ville II (Canopus);
# Vila Coimbra + Villa di Carpi + Ana Vitória (Castelucci);
# Varandas Grand Park (Franere); Villa Adagio + Lagoon (Lua Nova);
# Dom Ricardo + Prime Cohama + Dom Antônio (MB); Renaissance Conceito + Sanpaolo (Monteplan);
# Reserva Península (Sá Cavalcante). Handles IG corrigidos para 13 incorp.

# ═══════════════════════════════════════════════════════════════
# IDENTIDADE VISUAL DOM
# ═══════════════════════════════════════════════════════════════
DOM_BLACK="FF000000"; DOM_GRAY_DARK="FF4D4D4D"; DOM_GRAY_MID="FF8C8C8C"
DOM_GRAY_LIGHT="FFF2F2F2"; DOM_WHITE="FFFFFFFF"; DOM_GOLD="FFC9A84C"
DOM_GOLD_LIGHT="FFE8D5A3"; DOM_GOLD_DARK="FF8B6914"
DOM_RED_SOFT="FFF4B7B7"; DOM_GREEN_SOFT="FFBEE0B4"
DOM_BLUE_SOFT="FFCEE1F2"

SKILL_ASSETS="/sessions/brave-confident-meitner/mnt/.claude/skills/dom-xlsx-theme/assets"
LOGO_TRANSP=os.path.join(SKILL_ASSETS,"DOM_LOGO_TRANSPARENTE.png")

# ═══════════════════════════════════════════════════════════════
# ENUMERAÇÕES (ver §4 do PADRAO.md)
# ═══════════════════════════════════════════════════════════════
INCORPORADORAS = [
    "Mota Machado","Berg Engenharia","Alfa Engenharia","Lua Nova",
    "Delman","Treviso","Ergus","Monteplan","Franere","Canopus",
    "Niágara","MB Engenharia","Sá Cavalcante","Castelucci"
]

SEGMENTOS = ["Popular","Médio","Médio-alto","Alto","Luxo"]

STATUS = ["Pré-lançamento","Lançamento","Em comercialização",
          "Últimas unidades","Entregue","Esgotado"]

ORIG_PRECOS    = ["tabela_local","site_oficial","agregador","imprensa","estimativa","N/A"]
ORIG_ESTOQUE   = ["tabela_local","site_oficial","agregador","corretor","estimativa","N/A"]
ORIG_LANCAMENTO= ["book","release","treinamento_corretor","site_oficial","imprensa","estimativa_T-36"]

def classificar_segmento_por_m2(preco_m2):
    if preco_m2 is None: return None
    if preco_m2 < 6000: return "Popular"
    if preco_m2 < 9000: return "Médio"
    if preco_m2 < 13000: return "Médio-alto"
    if preco_m2 < 18000: return "Alto"
    return "Luxo"

def reclassificar_status(status_atual, estoque_pct):
    """§4.3 — Status comercial. Reclassifica automaticamente quando houver estoque.
    Preserva Pré-lançamento, Lançamento, Entregue, Esgotado (manuais)."""
    # Estados manuais preservados (não dependem de estoque)
    if status_atual in ("Pré-lançamento", "Entregue", "Esgotado"):
        return status_atual
    if estoque_pct is None:
        return status_atual
    if estoque_pct == 0:
        return "Esgotado"
    if estoque_pct <= 0.15:
        return "Últimas unidades"
    if estoque_pct > 0.40:
        # Se estava como Lançamento e tem estoque >40%, pode continuar Lançamento
        # se for recente; por ora deixamos "Em comercialização" como padrão quando >40%
        # exceto se foi explicitamente "Lançamento" (até 6m de venda — info não temos agora)
        return "Em comercialização" if status_atual != "Lançamento" else "Lançamento"
    # 15% < estoque <= 40%
    return "Em comercialização"

# ═══════════════════════════════════════════════════════════════
# DATASET — 18 EMPREENDIMENTOS (Fase 1 v2.0 — migrado do v1.2)
# ═══════════════════════════════════════════════════════════════
# Estrutura de cada linha (tupla de 24 campos conforme §1 do PADRAO.md):
#  0  Incorporadora
#  1  Empreendimento
#  2  Endereço
#  3  Bairro
#  4  Segmento            (pode ser None → será auto-classificado por R$/m²)
#  5  Status
#  6  Nº total unidades   (None se desconhecido)
#  7  Mês lançamento      (texto MM/AAAA, sufixar "⚠ T-36" se estimado)
#  8  Mês entrega         (texto MM/AAAA ou "—")
#  9  Área mín (m²)       (None se desconhecido)
# 10  Área máx (m²)       (None se desconhecido)
# 11  Tipologia média m²  (None → será calculado)
# 12  Tipologia dorms
# 13  Ticket mín R$
# 14  Ticket máx R$
# 15  Preço médio R$/m²   (None → será calculado)
# 16  VGV estimado R$     (None → será calculado)
# 17  Estoque %           (None se desconhecido, como fração 0-1)
# 18  Origem preços
# 19  Origem estoque
# 20  Origem lançamento
# 21  Link fonte principal
# 22  Data última verificação
# 23  Observações

E_RAW = [
    # ═══ ALFA ENGENHARIA ═════════════════════════════════════════════════
    ("Alfa Engenharia","Connect Península",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Alto","Pré-lançamento",
     None,"~2024","—", None,None,None, "—",
     None,None, None,None,None,
     "N/A","N/A","site_oficial",
     "https://www.alfaengenharia.com.br","14/04/2026",
     "Tipologia a confirmar em book/site/Instagram. Tecnologia Housi (gestão de locação) NÃO determina tipologia — descrição anterior corrigida. Sem tabela comercial pública."),

    ("Alfa Engenharia","Legacy Residence",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Luxo","Lançamento",
     None,"~2023","10/2027", None,None,None, "4 suítes",
     None,None, None,None,None,
     "N/A","N/A","imprensa",
     "https://www.alfaengenharia.com.br","14/04/2026",
     "13 opções de lazer, elevador privativo. Book local (375MB) + site oficial. Sem ticket público."),

    ("Alfa Engenharia","LIV Residence",
     "Rua Aziz Heluy, S/N, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Alto","Lançamento",
     None,"~2024","—", None,None,None, "3 suítes",
     None,None, None,None,None,
     "N/A","N/A","site_oficial",
     "https://www.alfaengenharia.com.br","14/04/2026",
     "1º Housi do MA. Book local + site Alfa. Sem tabela comercial."),

    # ═══ DELMAN ═════════════════════════════════════════════════════════
    ("Delman","Azimuth",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     None,"Em comercialização",
     30,"~2023","10/2026", 196.62,196.62,None, "3 suítes",
     3600000,3600000, None,None, 1/30,
     "tabela_local","tabela_local","imprensa",
     "https://www.delman.com.br","14/04/2026",
     "Tabela 04/2026: 1 apto (901) de 30. ≈97% vendido. Lançamento confirmado 2023 pela imprensa."),

    ("Delman","Landscape",
     "Avenida dos Holandeses, S/N, Calhau, São Luís - MA","Calhau",
     None,"Lançamento",
     95,"2026","09/2029", 88,103,None, "3 suítes",
     1200000,1500000, None,None, 52/95,
     "tabela_local","tabela_local","imprensa",
     "https://www.delman.com.br","14/04/2026",
     "Tabela 04/2026 marcada 'pré-lançamento'. Fonte web confirma lançamento 2026. Duplex cobertura 123-143m²."),

    ("Delman","Quartier 22",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     None,"Em comercialização",
     30,"09/2022 ⚠ T-36","09/2025", 165,165,None, "3 suítes",
     3000000,3000000, None,None, 1/30,
     "tabela_local","tabela_local","estimativa_T-36",
     "https://www.delman.com.br","14/04/2026",
     "Entrega iminente. 1 apto (601) de 30 à venda. ≈97% vendido."),

    ("Delman","Sky Residence",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     None,"Em comercialização",
     12,"09/2024 ⚠ T-36","09/2027", 246.69,246.69,None, "4 suítes",
     4700000,4700000, None,None, 1/12,
     "tabela_local","tabela_local","estimativa_T-36",
     "https://www.delman.com.br","14/04/2026",
     "Prédio pequeno (12 aptos). 1 à venda. ≈92% vendido."),

    ("Delman","Studio Design 7 Península",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     None,"Em comercialização",
     125,"04/2025 ⚠ T-36","04/2028", 43,64,None, "Studio / 1Q",
     710000,1000000, None,None, 33/125,
     "tabela_local","tabela_local","estimativa_T-36",
     "https://www.delman.com.br","14/04/2026",
     "33 de 125 aptos à venda. ≈74% vendido em ~18 meses. Forte velocidade em compactos."),

    ("Delman","Wave Residence",
     "Endereço não localizado, Ponta do Farol, São Luís - MA","Ponta do Farol",
     None,"Em comercialização",
     30,"2024","03/2029", 293.69,293.69,None, "4 suítes",
     5500000,5800000, None,None, 5/30,
     "tabela_local","tabela_local","imprensa",
     "https://www.delman.com.br","14/04/2026",
     "Evento de apresentação oficial 2024. 5 de 30 à venda. ≈83% vendido. Piscina privativa na varanda."),

    # ═══ ERGUS ═════════════════════════════════════════════════════════
    ("Ergus","Zion Ponta d'Areia",
     "Rua Aziz Heluy, S/N, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Alto","Em comercialização",
     None,"09/2025","12/2026", 148,148,None, "4 suítes + 3 vagas",
     None,None, None,None,None,
     "site_oficial","N/A","treinamento_corretor",
     "https://www.ergus.com.br","14/04/2026",
     "2 torres, 2 aptos/andar, 15 andares. Elevadores triplos. Treinamento corretor 12/09/2025 confirma lançamento comercial ~set/2025."),

    ("Ergus","Nexus Renascença",
     "Endereço não localizado, Renascença, São Luís - MA","Renascença",
     "Médio-alto","Em comercialização",
     None,"~2023","—", 33,94,None, "Studio a 2Q",
     None,None, None,None,None,
     "site_oficial","N/A","imprensa",
     "https://www.ergus.com.br","14/04/2026",
     "Complexo 10mil m² multi-produto (residencial + comercial + Open Mall). Book local + site oficial."),

    # ═══ TREVISO ═══════════════════════════════════════════════════════
    ("Treviso","Vernazza Residenziale",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     None,"Em comercialização",
     120,"2025","12/2029", 88,130,None, "3 suítes",
     1250000,2190000, None,None, 64/120,
     "tabela_local","tabela_local","imprensa",
     "https://www.treviso.com.br","14/04/2026",
     "Tabela 02/2026: 37 Norte + 27 Sul = 64 de 120. ≈47% vendido. Fonte web indica pré-lançamento 2025."),

    # ═══ NIÁGARA ═══════════════════════════════════════════════════════
    ("Niágara","ORO Ponta d'Areia",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     None,"Lançamento",
     None,"~2026 ⚠ T-36","~2029", 80.32,160.64,None, "2-4 suítes",
     1000000,2600000, None,None,None,
     "tabela_local","N/A","estimativa_T-36",
     "https://www.niagara-imoveis.com.br","14/04/2026",
     "Tabela JAN/26 é matriz por posição (não espelha estoque). Duplex cobertura 160m². Parcelamento 48m pós-assinatura."),

    # ═══ MOTA MACHADO ═══════════════════════════════════════════════════
    ("Mota Machado","Edifício Bossa",
     "Endereço não localizado, Calhau, São Luís - MA","Calhau",
     "Luxo","Lançamento",
     60,"04/2026","—", 191,195,None, "4 suítes + vista mar",
     None,None, None,None,None,
     "imprensa","N/A","imprensa",
     "https://motamachado.com.br","14/04/2026",
     "LANÇAMENTO ABRIL/2026 — evento oficial em 09/04/2026 (Frisson, MaHoje, Portal IN). 2 torres, 4 suítes, 191-195m², vista mar. Alto padrão/luxo. Mota Machado (CE) expandindo no NE, VGV 2025 R$350M."),

    ("Mota Machado","Reserva São Marcos",
     "Endereço não localizado, Calhau, São Luís - MA","Calhau",
     "Alto","Em comercialização",
     None,"~2024","—", None,None,None, "—",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://www.motamachado.com.br","14/04/2026",
     "Obras iniciadas 09/2025. Empresa de Fortaleza expandindo no Nordeste. SEM material local."),

    # ═══ BERG ══════════════════════════════════════════════════════════
    ("Berg Engenharia","Monte Meru",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Alto","Pré-lançamento",
     None,"~2025","—", None,None,None, "—",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://www.bergengenharia.com.br","14/04/2026",
     "Histórico Berg: Montparnasse, Golden Tower, Peninsula Mall, Monte Olimpo, Monte Fuji. SEM material local."),

    ("Berg Engenharia","Mount Solaro",
     "Endereço não localizado, São Luís - MA","São Luís",
     None,"Pré-lançamento",
     None,"~2025","—", None,None,None, "—",
     None,None, None,None,None,
     "N/A","N/A","imprensa",
     "https://www.bergengenharia.com.br","14/04/2026",
     "SPE Berg + Gonçalves requereu Licença de Instalação (Diário Oficial SL)."),

    # ═══ SÁ CAVALCANTE ══════════════════════════════════════════════════
    ("Sá Cavalcante","Ilha Parque Residence",
     "Endereço não localizado, Maranhão Novo, São Luís - MA","Maranhão Novo",
     "Médio","Entregue",
     120,"—","Entregue", 64,85,None, "2-3 quartos",
     None,None, None,None,None,
     "N/A","N/A","site_oficial",
     "https://www.sacavalcante.com.br","14/04/2026",
     "120 aptos (60 2Q + 60 3Q), 12/andar, 15 pavs. Pronto p/ morar. Ao lado do Shopping da Ilha."),

    # ═══ v4.1 — NOVOS EMPREENDIMENTOS MAPEADOS VIA WEB (14/04/2026) ═══

    # ─── MOTA MACHADO (atualização Bossa com dados de imprensa) ───
    # (mantém linha Bossa anterior e adiciona nada; obs complementar abaixo só para referência)

    # ─── ALFA ENGENHARIA — Giardino Residenza (novo, Ponta do Farol) ───
    ("Alfa Engenharia","Giardino Residenza",
     "Endereço não localizado, Ponta do Farol, São Luís - MA","Ponta do Farol",
     None,"Lançamento",
     None,"~2025","—", None,None,None, "—",
     None,None, None,None,None,
     "N/A","N/A","imprensa",
     "https://www.instagram.com/alfaengenhariama/","14/04/2026",
     "Lançamento Alfa — Ponta do Farol. Fonte: @alfaengenhariama + reel de corretor (CRECI/MA 3021). Sem tabela pública."),

    # ─── TREVISO — Villagio Treviso ───
    ("Treviso","Villagio Treviso",
     "Endereço não localizado, São Luís - MA","São Luís",
     None,"Em comercialização",
     None,"~2025","—", None,None,None, "Terrenos em condomínio",
     None,None, None,None,None,
     "N/A","N/A","site_oficial",
     "https://trevisoengenharia.com.br","14/04/2026",
     "Condomínio de terrenos (loteamento fechado). Divulgação ativa abr/2026. Sem tabela pública mapeada."),

    # ─── CANOPUS — 3 lançamentos out/2025 (Imirante) ───
    ("Canopus","Village Reserva II",
     "Endereço não localizado, São Luís - MA","São Luís",
     None,"Lançamento",
     None,"10/2025","—", None,None,None, "—",
     None,None, None,None,None,
     "N/A","N/A","imprensa",
     "https://canopusconstrucoes.com.br","14/04/2026",
     "1 dos 3 novos lançamentos Canopus anunciados em 31/10/2025 (Imirante). SEM tabela ou book mapeado."),

    ("Canopus","Village Prime Eldorado",
     "Endereço não localizado, Jardim Eldorado, São Luís - MA","Jardim Eldorado",
     None,"Lançamento",
     None,"10/2025","—", None,None,None, "—",
     None,None, None,None,None,
     "N/A","N/A","imprensa",
     "https://canopusconstrucoes.com.br","14/04/2026",
     "Canopus em movimento forte no Eldorado. Fonte: Imirante 31/10/2025."),

    ("Canopus","Village Del Ville II",
     "Endereço não localizado, São Luís - MA","São Luís",
     None,"Lançamento",
     None,"10/2025","—", None,None,None, "—",
     None,None, None,None,None,
     "N/A","N/A","imprensa",
     "https://canopusconstrucoes.com.br","14/04/2026",
     "Série Village (estratégia de marca clara). Imirante 31/10/2025. Confirmar tipologia/ticket via site+IG."),

    # ─── CASTELUCCI — 3 empreend. mapeados (site + Instagram + agregador) ───
    ("Castelucci","Vila Coimbra",
     "Endereço não localizado, Araçagi, São Luís - MA","Araçagi",
     "Alto","Lançamento",
     None,"~2026","—", None,None,None, "—",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://construtoracastelucci.com.br","14/04/2026",
     "Novo alto padrão no Araçagi em parceria com Grupo Coimbra Alves. Paulo Castelucci (CEO) em entrevista à Mirante FM. Patrocinando Imob Summit 2026."),

    ("Castelucci","Villa di Carpi",
     "Endereço não localizado, Cohatrac, São Luís - MA","Cohatrac",
     None,"Em comercialização",
     None,"~2024","—", 49,52,None, "2Q",
     None,None, None,None,None,
     "agregador","N/A","site_oficial",
     "https://construtoracastelucci.com.br","14/04/2026",
     "Compactos 49-52m², 2Q. Público Cohatrac/médio. Instagram @construtoracastelucci anunciou como lançamento; preço não divulgado."),

    ("Castelucci","Residencial Ana Vitória",
     "Endereço não localizado, Araçagy, São Luís - MA","Araçagy",
     None,"Em comercialização",
     None,"~2023","—", None,None,None, "2-3Q",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://construtoracastelucci.com.br","14/04/2026",
     "Apartamentos 2-3Q Araçagy. Site oficial Castelucci."),

    # ─── FRANERE — série Gran Park ───
    ("Franere","Varandas Grand Park",
     "Endereço não localizado, São Luís - MA","São Luís",
     None,"Em comercialização",
     None,"~2024","—", None,None,None, "—",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://franere.com.br","14/04/2026",
     "Franere ('Maior construtora do Maranhão', 40 anos). Série 'Gran Park' tem múltiplos módulos. IG @franereoficial_."),

    # ─── LUA NOVA — 2 empreend. ───
    ("Lua Nova","Villa Adagio",
     "Endereço não localizado, São Luís - MA","São Luís",
     None,"Em comercialização",
     None,"~2024","—", None,None,None, "—",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://construtoraluanova.com.br","14/04/2026",
     "Construtora Lua Nova desde 1985. IG @construtoraluanova. Detalhes tipologia/ticket a coletar via book."),

    ("Lua Nova","Lagoon Residence",
     "Endereço não localizado, Santo Amaro, São Luís - MA","Santo Amaro",
     None,"Em comercialização",
     None,"~2024","—", None,None,None, "—",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://construtoraluanova.com.br","14/04/2026",
     "Residência no Santo Amaro — região com oferta crescente de médio padrão."),

    # ─── MB ENGENHARIA — 3 empreend. ───
    ("MB Engenharia","Edifício Dom Ricardo",
     "Rua dos Rouxinóis, 8, Jardim Renascença, São Luís - MA","Jardim Renascença",
     None,"Últimas unidades",
     None,"~2023","—", 71,85,None, "2-3Q",
     None,None, None,None, 6/100,
     "agregador","agregador","imprensa",
     "https://www.imeu.com.br/empreendimento/dom-ricardo-apartamentos-sao-luis-2-a-3-quartos-71-a-85-m/19044585-MIM","14/04/2026",
     "Próximo à Praça da Lagoa (Foguete). 'Sucesso de vendas, 6 unidades disponíveis' (IG jan/2025). Estoque estimado ≤6%."),

    ("MB Engenharia","Condomínio Prime Cohama",
     "Endereço não localizado, Cohama, São Luís - MA","Cohama",
     None,"Em comercialização",
     22,"~2023","—", 140,140,None, "Casas duplex",
     None,None, None,None,None,
     "N/A","N/A","imprensa",
     "https://www.instagram.com/mbengenharia.br/","14/04/2026",
     "22 casas duplex 140m² — produto horizontal diferenciado. Pré-lançamento anunciado 2023, hoje em comercialização."),

    ("MB Engenharia","Dom Antônio",
     "Endereço não localizado, Jardim Eldorado (Turú), São Luís - MA","Jardim Eldorado",
     None,"Em comercialização",
     None,"~2024","—", 136,136,None, "3Q casas duplex",
     906870,906870, None,None,None,
     "agregador","N/A","site_oficial",
     "https://www.imovelnacidade.com/destaque/mb-construtora/","14/04/2026",
     "Casa duplex 3Q, 136m², R$906.870. Produto horizontal Eldorado/Turú."),

    # ─── MONTEPLAN — 2 empreend. ativos ───
    ("Monteplan","Renaissance Conceito",
     "Rua Caxuxa, S/N, Renascença II, São Luís - MA","Renascença II",
     "Alto","Lançamento",
     None,"~2025","—", None,None,None, "3Q",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://monteplanengenharia.com.br/empreendimentos/renaissance-conceito/","14/04/2026",
     "Alto padrão Renascença II (Loteamento Boa Vista). Dois torres, lazer completo."),

    ("Monteplan","Edifício Sanpaolo",
     "Endereço não localizado, São Luís - MA","São Luís",
     "Médio-alto","Esgotado",
     None,"~2023","—", None,None,None, "2-3Q",
     None,None, None,None, 0.0,
     "site_oficial","site_oficial","site_oficial",
     "https://monteplanengenharia.com.br/empreendimentos/edificio-sanpaolo/","14/04/2026",
     "2Q (2 suítes, 1 reversível) ou 3Q (1 suíte). 'Todas as unidades vendidas' (Facebook out/2025)."),

    # ─── SÁ CAVALCANTE — Reserva Península (novo) ───
    ("Sá Cavalcante","Reserva Península",
     "Endereço não localizado, Ponta d'Areia (Península), São Luís - MA","Ponta d'Areia",
     "Alto","Lançamento",
     None,"10/2025","—", None,None,None, "—",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://www.instagram.com/sacavalcantema/","14/04/2026",
     "Lançamento Sá Cavalcante out/2025. Estande 'Casa Sal' na Península. 'Os espaços conversam...' — narrativa de estilo de vida."),
]

# ═══════════════════════════════════════════════════════════════
# DATASET — 13 INCORPORADORAS (serão auto-calculadas a partir de E)
# ═══════════════════════════════════════════════════════════════
# Campos editáveis manualmente por incorporadora (os calculáveis ficam None):
# (incorporadora, site, instagram, posicionamento)
# v4.2: removidas colunas RI e Capital Aberto (irrelevantes para o mercado SLZ).
I_META = {
    "Mota Machado":     ("https://motamachado.com.br","@motamachado",
                         "Cearense em expansão no NE. Lançou Bossa em abr/2026 no Calhau (4 suítes, 191-195m², vista mar). Reserva São Marcos em obras. VGV 2025 R$350M."),
    "Berg Engenharia":  ("https://www.bergengenharia.com.br","@bergengenharia",
                         "28 anos em SL. Monte Meru (Península, 135m²) em comercialização. Mount Solaro em parceria com Gonçalves Empreend. (SPE, LI solicitada)."),
    "Alfa Engenharia":  ("https://www.alfaengenharia.com.br","@alfaengenhariama",
                         "Tech-forward (1º Housi do MA em LIV). Novo lançamento Giardino Residenza (Ponta do Farol). Marca no IG: @alfaengenhariama."),
    "Lua Nova":         ("https://construtoraluanova.com.br","@construtoraluanova",
                         "Desde 1985 (40+ anos). Villa Adagio + Lagoon Residence (Santo Amaro). Perfil médio-padrão. Mapeada via web."),
    "Delman":           ("https://www.delman.com.br","@delmanincorporadora",
                         "Referência de luxo em Ponta d'Areia; 6 empreend. ticket R$710k-R$5,8M. Novo LandSpace (Landscape) no Calhau 2026."),
    "Treviso":          ("https://trevisoengenharia.com.br","@treviso.engenharia",
                         "Vernazza (120 un. Ponta d'Areia) + Villagio Treviso (loteamento). Ed. Biadene Oaice é sede."),
    "Ergus":            ("https://ergusengenharia.com.br","@ergusengenharia",
                         "25 anos em 2026. Multi-produto (Zion, Nexus, Lead Office, On Residence, Open Design). Proposta sustentável. Projeto Nexus 10.000m² em Renascença."),
    "Monteplan":        ("https://monteplanengenharia.com.br","@monteplanengenharia",
                         "Renaissance Conceito (Renascença II, alto padrão) + Sanpaolo (esgotado). Portfólio residencial e comercial."),
    "Franere":          ("https://franere.com.br","@franereoficial_",
                         "'Maior construtora do Maranhão' (self-proclamada). 40 anos. Série Gran Park / Varandas Grand Park."),
    "Canopus":          ("https://canopusconstrucoes.com.br","@canopusconstrucoes",
                         "Endereço: Av. Cel. Colares Moreira, 1, J. Renascença. 3 lançamentos out/2025: Village Reserva II, Prime Eldorado, Del Ville II. Atua também em Imperatriz."),
    "Niágara":          ("https://niagaraempreendimentos.com.br","@niagaraimoveis",
                         "ORO com ampla faixa 80-160m², parcelamento 48m pós-assinatura. Reserva dos Vinhais (Vinhais 2Q 48m²) + Reserva dos Buritis."),
    "MB Engenharia":    ("","@mbengenharia.br",
                         "Ed. Dom Ricardo (Renascença, 2-3Q 71-85m²) + Prime Cohama (22 casas duplex 140m²) + Dom Antônio (Turú 136m² R$906k) + Fernando de Noronha 2ª etapa. Ativo e diversificado."),
    "Sá Cavalcante":    ("https://www.sacavalcante.com.br","@sacavalcantema",
                         "Grupo desde 1974 (shoppings + incorporação). Ilha Parque entregue + NOVO Reserva Península (out/2025, Ponta d'Areia)."),
    "Castelucci":       ("https://construtoracastelucci.com.br","@construtoracastelucci",
                         "10+ anos. CEO Paulo Castelucci (Mirante FM). Vila Coimbra (parceria Coimbra Alves, Araçagi alto padrão) + Villa di Carpi (Cohatrac) + Ana Vitória (Araçagy). Patrocinador Imob Summit."),
}

# ═══════════════════════════════════════════════════════════════
# CÁLCULOS AUTOMÁTICOS (ver §3 do PADRAO.md)
# ═══════════════════════════════════════════════════════════════
def calc_preco_m2(tmin,tmax,amin,amax):
    """§3.1 — padrão: ticket_médio / área_média"""
    if None in (tmin,tmax,amin,amax): return None
    tm = (tmin+tmax)/2
    am = (amin+amax)/2
    if am==0: return None
    return tm/am

def calc_vgv(tmin,tmax,unidades):
    """§3.2"""
    if None in (tmin,tmax,unidades): return None
    return ((tmin+tmax)/2) * unidades

def calc_area_media(amin,amax):
    if None in (amin,amax): return None
    return (amin+amax)/2

def extract_year(mes_str):
    """Extrai ano de string tipo '04/2025', '~2024', '~2025 ⚠ T-36', '2024 ♦'"""
    if not mes_str or mes_str=="—": return None
    import re
    m=re.search(r'(\d{4})',mes_str)
    return int(m.group(1)) if m else None

def parse_launch_date(mes_str):
    """Converte string de mês de lançamento para tupla (ano, mês) para ordenação.
    Retorna (0,0) para desconhecidos (vão para o fim em ordem decrescente)."""
    if not mes_str or mes_str=="—":
        return (0, 0)
    import re
    # Formato MM/AAAA
    m = re.search(r'(\d{1,2})/(\d{4})', mes_str)
    if m:
        return (int(m.group(2)), int(m.group(1)))
    # Formato só ano
    y = re.search(r'(\d{4})', mes_str)
    if y:
        return (int(y.group(1)), 0)  # sem mês: assume janeiro para ordenação
    return (0, 0)

# Processa cada empreendimento: preenche campos calculados
E_PROCESSED = []
for row in E_RAW:
    row = list(row)
    # calcular área média (idx 11)
    if row[11] is None:
        row[11] = calc_area_media(row[9],row[10])
    # calcular preço médio R$/m² (idx 15)
    if row[15] is None:
        row[15] = calc_preco_m2(row[13],row[14],row[9],row[10])
    # calcular VGV (idx 16)
    if row[16] is None:
        row[16] = calc_vgv(row[13],row[14],row[6])
    # auto-classificar segmento se não definido (idx 4)
    if row[4] is None and row[15] is not None:
        row[4] = classificar_segmento_por_m2(row[15])
    elif row[4] is None:
        row[4] = "—"
    # auto-reclassificar status pelo estoque (idx 5 usando idx 17)
    row[5] = reclassificar_status(row[5], row[17])
    E_PROCESSED.append(tuple(row))

# ═══════════════════════════════════════════════════════════════
# FUNÇÕES DE ESTILO
# ═══════════════════════════════════════════════════════════════
def fill(c): return PatternFill("solid",fgColor=c)
def font(color=DOM_GRAY_DARK,size=10,bold=False,italic=False):
    return Font(name="Calibri",color=color,size=size,bold=bold,italic=italic)
def border_thin(c=DOM_GRAY_MID):
    s=Side(style="thin",color=c); return Border(left=s,right=s,top=s,bottom=s)
def center(): return Alignment(horizontal="center",vertical="center",wrap_text=True)
def left():   return Alignment(horizontal="left",vertical="center",wrap_text=True)

def apply_header_row(ws,row,headers):
    ws.row_dimensions[row].height=42
    for i,h in enumerate(headers):
        c=ws.cell(row=row,column=1+i,value=h)
        c.font=font(DOM_WHITE,9,bold=True); c.fill=fill(DOM_GRAY_DARK); c.alignment=center()
        c.border=Border(bottom=Side(style="medium",color=DOM_GOLD),
                        left=Side(style="thin",color=DOM_GRAY_MID),
                        right=Side(style="thin",color=DOM_GRAY_MID))

def insert_logo(ws,path,cell="A1",height_px=55):
    if not os.path.exists(path): return
    img=XLImage(path); r=img.width/img.height
    img.height=height_px; img.width=int(height_px*r); ws.add_image(img,cell)

def set_column_widths(ws,widths):
    for i,w in enumerate(widths):
        ws.column_dimensions[get_column_letter(1+i)].width=w

# ═══════════════════════════════════════════════════════════════
# CONSTRUÇÃO DA PLANILHA
# ═══════════════════════════════════════════════════════════════
wb = Workbook()

# ── ABA 1: EMPREENDIMENTOS ─────────────────────────────────────
ws1 = wb.active; ws1.title = "Empreendimentos"
N_COLS_E = 24
ws1.row_dimensions[1].height=22; ws1.row_dimensions[2].height=28; ws1.row_dimensions[3].height=18
for r in (1,2,3):
    for c in range(1,N_COLS_E+1):
        ws1.cell(row=r,column=c).fill=fill(DOM_BLACK)
insert_logo(ws1,LOGO_TRANSP,"A1",55)
ws1.merge_cells(start_row=2,start_column=4,end_row=2,end_column=N_COLS_E)
t=ws1.cell(row=2,column=4,value="INTELIGÊNCIA DE MERCADO — Panorama de Empreendimentos")
t.font=font(DOM_WHITE,16,bold=True); t.alignment=Alignment(horizontal="left",vertical="center")
ws1.merge_cells(start_row=3,start_column=4,end_row=3,end_column=N_COLS_E)
s=ws1.cell(row=3,column=4,
    value=f"São Luís / MA  •  v{VERSION}  •  {DATE_STR}  •  Fase 1 (padrão congelado — ver _PADRAO_FASE_1/PADRAO.md)")
s.font=font(DOM_GOLD,10,italic=True); s.alignment=Alignment(horizontal="left",vertical="center")

headers_e = [
    "Incorporadora","Empreendimento","Endereço","Bairro","Segmento","Status",
    "Nº unid.","Mês lançamento","Mês entrega",
    "Área mín (m²)","Área máx (m²)","Tipologia média (m²)","Tipologia (dorms)",
    "Ticket mín (R$)","Ticket máx (R$)","R$/m²","VGV (R$)","% Vendido",
    "Orig. preços","Orig. estoque","Orig. lançamento",
    "Link fonte principal","Data verif.","Observações"
]
apply_header_row(ws1,5,headers_e)

formats_e = [None]*N_COLS_E
formats_e[9] = formats_e[10] = formats_e[11] = '0.0'
formats_e[13] = formats_e[14] = 'R$ #,##0'
formats_e[15] = 'R$ #,##0'
formats_e[16] = 'R$ #,##0'
formats_e[17] = '0.0%'

# §7 PADRAO.md: ordenar por Mês Lançamento DESCENDENTE (mais recente 1º),
# depois Incorporadora A-Z, depois Empreendimento A-Z
empreend_sorted = sorted(
    E_PROCESSED,
    key=lambda r: (
        -parse_launch_date(r[7])[0],  # ano desc
        -parse_launch_date(r[7])[1],  # mês desc
        r[0],                          # incorporadora asc
        r[1]                           # empreendimento asc
    )
)

for i, row_data in enumerate(empreend_sorted):
    row_idx = 6+i
    ws1.row_dimensions[row_idx].height = 52
    row_fill = DOM_WHITE if row_idx%2==0 else DOM_GRAY_LIGHT
    # Converter coluna 17 (estoque fração) em % vendido = 1 - estoque
    row_values = list(row_data)
    if isinstance(row_values[17], (int, float)):
        row_values[17] = 1 - row_values[17]
    for j, v in enumerate(row_values):
        cel = ws1.cell(row=row_idx, column=1+j, value=v)
        cel.font = font(DOM_GRAY_DARK, 9)
        cel.fill = fill(row_fill)
        cel.alignment = left() if j in (2, 12, 23) else center()
        cel.border = border_thin()
        if formats_e[j]:
            cel.number_format = formats_e[j]
    # Sem coloração condicional na coluna % Vendido (Rafael pediu p/ remover)
    # Destaque da incorporadora
    ws1.cell(row=row_idx, column=1).font = font(DOM_GRAY_DARK, 9, bold=True)

total_row_e = 6+len(empreend_sorted)

widths_e = [15,22,30,14,11,17, 7,14,11, 10,10,11,20, 13,13,11,14,10,
            14,14,18, 28,10,50]
set_column_widths(ws1, widths_e)
ws1.freeze_panes = "C6"
ws1.auto_filter.ref = f"A5:{get_column_letter(N_COLS_E)}{total_row_e-1}"

# Legenda
ws1.merge_cells(start_row=total_row_e, start_column=1, end_row=total_row_e, end_column=N_COLS_E)
leg = ws1.cell(row=total_row_e, column=1,
    value="ESTOQUE — 🟢 ≤15% (últimas unidades) | 🟡 15-40% (em absorção) | 🔴 >40% (estoque amplo).    "
          "STATUS = comercial (não físico).    "
          "SEGMENTO = classificado pelo R$/m² calculado (ver §4.2 do PADRAO.md).    "
          "⚠ T-36 = lançamento estimado por Entrega−42 meses. Substituir assim que tiver fonte.")
leg.font = font(DOM_GRAY_DARK,9,italic=True); leg.fill = fill(DOM_GRAY_LIGHT)
leg.alignment = Alignment(horizontal="left",vertical="center",wrap_text=True)
ws1.row_dimensions[total_row_e].height = 50

# Rodapé
ws1.merge_cells(start_row=total_row_e+1, start_column=1, end_row=total_row_e+1, end_column=N_COLS_E)
ft = ws1.cell(row=total_row_e+1, column=1,
    value=f"DOM Incorporação  •  Inteligência de Mercado  •  Planilha Mestre v{VERSION} (Fase 1)")
ft.font = Font(name="Calibri",color=DOM_GRAY_MID,size=8,italic=True)
ft.alignment = Alignment(horizontal="right",vertical="center")

# ── ABA 2: INCORPORADORAS ──────────────────────────────────────
ws2 = wb.create_sheet("Incorporadoras")
N_COLS_I = 15  # v4.2: removidas RI e Cap. aberto
ws2.row_dimensions[1].height=22; ws2.row_dimensions[2].height=28; ws2.row_dimensions[3].height=18
for r in (1,2,3):
    for c in range(1,N_COLS_I+1):
        ws2.cell(row=r,column=c).fill=fill(DOM_BLACK)
insert_logo(ws2,LOGO_TRANSP,"A1",55)
ws2.merge_cells(start_row=2,start_column=3,end_row=2,end_column=N_COLS_I)
t2=ws2.cell(row=2,column=3,value="INTELIGÊNCIA DE MERCADO — Panorama por Incorporadora")
t2.font=font(DOM_WHITE,16,bold=True); t2.alignment=Alignment(horizontal="left",vertical="center")
ws2.merge_cells(start_row=3,start_column=3,end_row=3,end_column=N_COLS_I)
s2=ws2.cell(row=3,column=3,
    value=f"14 incorporadoras monitoradas  •  v{VERSION}  •  {DATE_STR}")
s2.font=font(DOM_GOLD,10,italic=True); s2.alignment=Alignment(horizontal="left",vertical="center")

headers_i = [
    "Incorporadora","Nº empreend.","VGV total (R$)",
    "VGV lançado 2024","VGV lançado 2025","VGV lançado 2026",
    "Segmentos","Bairros","Ticket médio carteira","R$/m² médio carteira",
    "% carteira com arquivo","Site oficial","Instagram",
    "Posicionamento","Data verif."
]
apply_header_row(ws2,5,headers_i)

# Auto-calcula agregados por incorporadora
I_ROWS = []
for inc_name in INCORPORADORAS:
    meta = I_META.get(inc_name, ("","",""))
    emps = [r for r in E_PROCESSED if r[0]==inc_name]
    n = len(emps)
    vgv_list = [r[16] for r in emps if r[16] is not None]
    vgv_total = sum(vgv_list) if vgv_list else None
    vgv_2024=vgv_2025=vgv_2026=0
    for r in emps:
        if r[16] is None: continue
        y = extract_year(r[7])
        if y==2024: vgv_2024 += r[16]
        elif y==2025: vgv_2025 += r[16]
        elif y==2026: vgv_2026 += r[16]
    segs = sorted(set(r[4] for r in emps if r[4] and r[4]!="—"))
    bairros = sorted(set(r[3] for r in emps if r[3]))
    tickets = []
    for r in emps:
        if r[13] is not None and r[14] is not None:
            tickets.append((r[13]+r[14])/2)
    ticket_med = sum(tickets)/len(tickets) if tickets else None
    precos_m2 = [r[15] for r in emps if r[15] is not None]
    preco_m2_med = sum(precos_m2)/len(precos_m2) if precos_m2 else None
    # % com arquivo: heurística — se tem tabela_local em preços OU estoque
    com_arquivo = sum(1 for r in emps if r[18]=="tabela_local" or r[19]=="tabela_local")
    pct_arquivo = (com_arquivo / n) if n else 0
    I_ROWS.append((
        inc_name, n,
        vgv_total or 0,
        vgv_2024 or 0, vgv_2025 or 0, vgv_2026 or 0,
        ", ".join(segs) if segs else "—",
        ", ".join(bairros) if bairros else "—",
        ticket_med or 0,
        preco_m2_med or 0,
        pct_arquivo,
        meta[0], meta[1], meta[2],  # site, IG, posicionamento (v4.2)
        DATE_STR
    ))

# Ordena: com empreend. primeiro (desc por VGV), depois SEM material
I_ROWS_SORTED = sorted(I_ROWS, key=lambda r:(-(r[1]>0), -(r[2] or 0), r[0]))

formats_i = [None]*N_COLS_I
formats_i[2] = formats_i[3] = formats_i[4] = formats_i[5] = 'R$ #,##0'
formats_i[8] = formats_i[9] = 'R$ #,##0'
formats_i[10] = '0%'

for i, row_data in enumerate(I_ROWS_SORTED):
    row_idx = 6+i
    ws2.row_dimensions[row_idx].height = 38
    empty_row = row_data[1]==0
    row_fill = DOM_WHITE if row_idx%2==0 else DOM_GRAY_LIGHT
    for j, v in enumerate(row_data):
        c = ws2.cell(row=row_idx, column=1+j, value=v)
        c.font = font(DOM_GRAY_DARK,9)
        c.fill = fill(row_fill)
        c.alignment = left() if j in (6,7,11,13) else center()  # v4.2: posicionamento agora é idx 13
        c.border = border_thin()
        if formats_i[j]:
            c.number_format = formats_i[j]
        if empty_row:
            c.fill = fill(DOM_GOLD_LIGHT)
            c.font = font(DOM_GOLD_DARK,9,italic=True)
    # Destaque nome
    ws2.cell(row=row_idx, column=1).font = font(
        DOM_GOLD_DARK if empty_row else DOM_GRAY_DARK, 9, bold=True,
        italic=empty_row)

total_row_i = 6+len(I_ROWS_SORTED)

widths_i = [18, 10, 15, 15, 15, 15, 22, 30, 15, 14, 13, 30, 22, 48, 10]
set_column_widths(ws2, widths_i)
ws2.freeze_panes = "B6"
ws2.auto_filter.ref = f"A5:{get_column_letter(N_COLS_I)}{total_row_i-1}"

# Legenda aba 2
ws2.merge_cells(start_row=total_row_i, start_column=1, end_row=total_row_i, end_column=N_COLS_I)
leg2 = ws2.cell(row=total_row_i, column=1,
    value="Linhas DOURADAS = incorporadoras SEM material mapeado (0 empreend.) — prioridade de pesquisa web + contato local.    "
          "VGV total = soma do VGV estimado de todos os empreend.    VGV por ano = subconjunto por ano de lançamento.")
leg2.font = font(DOM_GRAY_DARK,9,italic=True); leg2.fill = fill(DOM_GRAY_LIGHT)
leg2.alignment = Alignment(horizontal="left",vertical="center",wrap_text=True)
ws2.row_dimensions[total_row_i].height = 42

ws2.merge_cells(start_row=total_row_i+1, start_column=1, end_row=total_row_i+1, end_column=N_COLS_I)
ft2 = ws2.cell(row=total_row_i+1, column=1,
    value=f"DOM Incorporação  •  Inteligência de Mercado  •  Planilha Mestre v{VERSION} (Fase 1)")
ft2.font = Font(name="Calibri",color=DOM_GRAY_MID,size=8,italic=True)
ft2.alignment = Alignment(horizontal="right",vertical="center")

# ═══════════════════════════════════════════════════════════════
# SALVAR — usa a pasta NFD (a real do usuário, com .DS_Store) para
# evitar criar pasta fantasma NFC por causa do Unicode do nome.
# ═══════════════════════════════════════════════════════════════
BASE = "/sessions/brave-confident-meitner/mnt"
# Pasta NFD (forma canônica do macOS: "e" + combining circumflex U+0302)
NFD_DIR_BYTES = os.path.join(BASE.encode(), b'01.Intelige\xcc\x82ncia Mercado')
if os.path.exists(NFD_DIR_BYTES):
    DST_BASE = NFD_DIR_BYTES.decode('utf-8')
else:
    # Fallback: se NFD não existe, usa o primeiro glob disponível
    matches = glob.glob(os.path.join(BASE, "01.Intelig*"))
    if not matches:
        raise FileNotFoundError("Pasta '01.Inteligência Mercado' não encontrada")
    DST_BASE = matches[0]
OUT = os.path.join(DST_BASE, "00_ESTUDO_CONSOLIDADO",
                   f"Planilha_Mestre_Panorama_v{VERSION}.xlsx")
wb.save(OUT)

print(f"✓ Salvo: {OUT}")
print(f"  Empreendimentos: {len(E_PROCESSED)}")
print(f"  Incorporadoras:  {len(I_ROWS)} (ativas: {sum(1 for r in I_ROWS if r[1]>0)}, sem material: {sum(1 for r in I_ROWS if r[1]==0)})")
print(f"  VGV total mapeado: R$ {sum(r[16] for r in E_PROCESSED if r[16]):,.0f}")
print(f"  Preço médio calculado para: {sum(1 for r in E_PROCESSED if r[15])} de {len(E_PROCESSED)} empreend.")
