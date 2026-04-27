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
VERSION = "5.2"
DATE_STR = "27/04/2026"
# v5.0 — (25/04/2026): MUDANÇA ESTRUTURAL — adoção do PADRAO v2.0.
# +Coluna Tipo (Vertical/Horizontal/Misto) inserida como col. 5. 24 → 25 colunas.
# +Hiali e DOM Incorporação como incorporadoras monitoradas (14 → 16). Tracking da
# .xlsx no git habilitado. Total: 45 empreendimentos, 16 incorporadoras.
# v5.1 — (27/04/2026): DOIS GRUPOS de mudança:
#
# (a) NOVOS DADOS de tabelas locais:
# +Vila Coimbra (Castelucci): tabela 03/2026 → 124,63m², ticket R$1.019k-1.082k,
# 36+ casas Araçagi. +Giardino Fiore (Alfa): 6/45 → 87% vendido → Últimas unidades.
# +Giardino Luce (Alfa): 5/60 → 92%, dorms corrigido para 3 suítes. +Monte Meru
# (Berg): tabela ABR/2026 → 135m², ticket R$1.932k-1.944k. +The View (Delman):
# tabela 27.04 substitui 24.04 → ticket_min sobe para R$559k (apto 409 vendido),
# 90 aptos disponíveis de ~110 = ~20 vendas em 3 dias.
#
# (b) CORREÇÃO SISTÊMICA de Mês lançamento (PADRAO §1 — col 9 deve ser MM/AAAA):
# 13 entries com pasta XX_MMAAAA tinham datas imprecisas no E_RAW (ex: Lagoon
# como ~2024 quando pasta dizia 042026). Atualizadas para MM/AAAA preciso.
# 8 entries sem pasta-data: estimadas como 06/AAAA + ⚠ T-36. parse_launch_date
# em ambos os scripts agora REJEITA AAAA puro (vai pro fim da lista).
# Validação assert no início do script bloqueia E_RAW com mês fora do padrão.
# v5.2 — (27/04/2026): +Edifício Bossa (Mota Machado) atualizado a partir da tabela
# local 04/2026: tickets R$2,85-3,71M, áreas 191-196m², R$/m² médio R$16.663 (faixa
# 14,9-19,2k), 36 aptos disponíveis de 60 (~60% estoque, 40% vendido), entrega
# 09/2030. Endereço completo. Segmento reclassifica auto pelo R$/m².
# +Fix reclassificar_status: preserva "Lançamento" como decisão de tempo (< 6m de
# venda), não força "Em comercialização" só por estoque > 15%.
# +Fix áreas em horizontais (Dom Lucas + Dom José): valores armazenados como
# construído/terreno misturados — corrigido para área CONSTRUÍDA em min e max
# (uma única tipologia em ambos). Terreno migrado para Observações. Convenção
# nova no PADRAO v2.0 §1 nota.

# ═══════════════════════════════════════════════════════════════
# IDENTIDADE VISUAL DOM
# ═══════════════════════════════════════════════════════════════
DOM_BLACK="FF000000"; DOM_GRAY_DARK="FF4D4D4D"; DOM_GRAY_MID="FF8C8C8C"
DOM_GRAY_LIGHT="FFF2F2F2"; DOM_WHITE="FFFFFFFF"; DOM_GOLD="FFC9A84C"
DOM_GOLD_LIGHT="FFE8D5A3"; DOM_GOLD_DARK="FF8B6914"
DOM_RED_SOFT="FFF4B7B7"; DOM_GREEN_SOFT="FFBEE0B4"
DOM_BLUE_SOFT="FFCEE1F2"

SKILL_ASSETS="/sessions/intelligent-festive-lamport/mnt/.claude/skills/dom-xlsx-theme/assets"
LOGO_TRANSP=os.path.join(SKILL_ASSETS,"DOM_LOGO_TRANSPARENTE.png")

# ═══════════════════════════════════════════════════════════════
# ENUMERAÇÕES (ver §4 do PADRAO.md)
# ═══════════════════════════════════════════════════════════════
INCORPORADORAS = [
    "Mota Machado","Berg Engenharia","Alfa Engenharia","Lua Nova",
    "Delman","Treviso","Ergus","Monteplan","Franere","Canopus",
    "Niágara","MB Engenharia","Sá Cavalcante","Castelucci",
    "Hiali","DOM Incorporação"
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
    Preserva Pré-lançamento, Lançamento, Entregue, Esgotado (manuais).

    Lógica (v5.2): Lançamento é decisão de TEMPO (< 6 meses de venda), não de
    estoque. Por isso preserva Lançamento independente do estoque (exceto se zerar
    ou ficar nas últimas unidades). Antes da v5.2, estoque entre 15-40% forçava
    "Em comercialização" mesmo em Lançamento — bug detectado com Bossa."""
    # Estados manuais preservados (não dependem de estoque)
    if status_atual in ("Pré-lançamento", "Entregue", "Esgotado"):
        return status_atual
    if estoque_pct is None:
        return status_atual
    if estoque_pct == 0:
        return "Esgotado"
    if estoque_pct <= 0.15:
        return "Últimas unidades"  # >85% vendido sobrescreve até Lançamento
    # estoque entre 15% e 100%
    if status_atual == "Lançamento":
        return "Lançamento"  # preserva: tempo de venda < 6m é decisão manual
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
     "Vertical","Alto","Pré-lançamento",
     None,"07/2024","—", None,None,None, "—",
     None,None, None,None,None,
     "N/A","N/A","site_oficial",
     "https://www.alfaengenharia.com.br","14/04/2026",
     "Tipologia a confirmar em book/site/Instagram. Tecnologia Housi (gestão de locação) NÃO determina tipologia — descrição anterior corrigida. Sem tabela comercial pública."),

    ("Alfa Engenharia","Legacy Residence",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Vertical","Luxo","Lançamento",
     None,"07/2024","10/2027", None,None,None, "4 suítes",
     None,None, None,None,None,
     "N/A","N/A","imprensa",
     "https://www.alfaengenharia.com.br","14/04/2026",
     "13 opções de lazer, elevador privativo. Book local (375MB) + site oficial. Sem ticket público."),

    ("Alfa Engenharia","LIV Residence",
     "Rua Aziz Heluy, S/N, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Vertical","Alto","Lançamento",
     None,"07/2023","—", None,None,None, "3 suítes",
     None,None, None,None,None,
     "N/A","N/A","site_oficial",
     "https://www.alfaengenharia.com.br","14/04/2026",
     "1º Housi do MA. Book local + site Alfa. Sem tabela comercial."),

    # ═══ DELMAN ═════════════════════════════════════════════════════════
    ("Delman","Azimuth",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Vertical",None,"Em comercialização",
     30,"07/2023","10/2026", 196.62,196.62,None, "3 suítes",
     3600000,3600000, None,None, 1/30,
     "tabela_local","tabela_local","imprensa",
     "https://www.delman.com.br","14/04/2026",
     "Tabela 04/2026: 1 apto (901) de 30. ≈97% vendido. Lançamento confirmado 2023 pela imprensa."),

    ("Delman","Landscape",
     "Avenida dos Holandeses, S/N, Calhau, São Luís - MA","Calhau",
     "Vertical",None,"Lançamento",
     95,"03/2026","09/2029", 88,103,None, "3 suítes",
     1200000,1500000, None,None, 52/95,
     "tabela_local","tabela_local","imprensa",
     "https://www.delman.com.br","14/04/2026",
     "Tabela 04/2026 marcada 'pré-lançamento'. Fonte web confirma lançamento 2026. Duplex cobertura 123-143m²."),

    ("Delman","Quartier 22",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Vertical",None,"Em comercialização",
     30,"09/2022 ⚠ T-36","09/2025", 165,165,None, "3 suítes",
     3000000,3000000, None,None, 1/30,
     "tabela_local","tabela_local","estimativa_T-36",
     "https://www.delman.com.br","14/04/2026",
     "Entrega iminente. 1 apto (601) de 30 à venda. ≈97% vendido."),

    ("Delman","Sky Residence",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Vertical",None,"Em comercialização",
     12,"09/2024 ⚠ T-36","09/2027", 246.69,246.69,None, "4 suítes",
     4700000,4700000, None,None, 1/12,
     "tabela_local","tabela_local","estimativa_T-36",
     "https://www.delman.com.br","14/04/2026",
     "Prédio pequeno (12 aptos). 1 à venda. ≈92% vendido."),

    ("Delman","Studio Design 7 Península",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Vertical",None,"Em comercialização",
     125,"04/2025 ⚠ T-36","04/2028", 43,64,None, "Studio / 1Q",
     710000,1000000, None,None, 33/125,
     "tabela_local","tabela_local","estimativa_T-36",
     "https://www.delman.com.br","14/04/2026",
     "33 de 125 aptos à venda. ≈74% vendido em ~18 meses. Forte velocidade em compactos."),

    ("Delman","Wave Residence",
     "Endereço não localizado, Ponta do Farol, São Luís - MA","Ponta do Farol",
     "Vertical",None,"Em comercialização",
     30,"09/2025","03/2029", 293.69,293.69,None, "4 suítes",
     5500000,5800000, None,None, 5/30,
     "tabela_local","tabela_local","imprensa",
     "https://www.delman.com.br","14/04/2026",
     "Evento de apresentação oficial 2024. 5 de 30 à venda. ≈83% vendido. Piscina privativa na varanda."),

    ("Delman","The View",
     "Avenida dos Holandeses, Qd. 02, Nº 08, Calhau, São Luís - MA","Calhau",
     "Vertical",None,"Pré-lançamento",
     None,"04/2026","—", 36.05,85.87,None, "Studio a 3Q (1Q/2Q dominantes)",
     559580,1504011, None,None,None,
     "tabela_local","tabela_local","tabela_local",
     "https://delman.com.br/maranhao/empreendimentos/proximos-lancamentos/edificio-the-view","27/04/2026",
     "PRÉ-LANÇAMENTO. Tabela atualizada 27/04/2026 (v2 — antiga 24/04 mantida em arquivo). 14 pavtos tipo (1º pav.tipo = 4º andar). 90 aptos disponíveis na 27.04 (vs ~110 na 24.04 → ~20 unidades vendidas/reservadas em 3 dias = TRAÇÃO FORTE na pré-venda). Tipologias 36,05–85,87 m² + cobertura. 17º andar premium R$/m² ~R$18.090. Site oficial indica até 101,06m². Ticket mín sobe para R$559k (apto 409 do 4º andar foi vendido). Parcelamento 100m + INCC/IGP-M+1%. Vista mar Calhau."),

    # ═══ ERGUS ═════════════════════════════════════════════════════════
    ("Ergus","Zion Ponta d'Areia",
     "Rua Aziz Heluy, S/N, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Vertical","Alto","Em comercialização",
     None,"09/2025","12/2026", 148,148,None, "4 suítes + 3 vagas",
     None,None, None,None,None,
     "site_oficial","N/A","treinamento_corretor",
     "https://www.ergus.com.br","14/04/2026",
     "2 torres, 2 aptos/andar, 15 andares. Elevadores triplos. Treinamento corretor 12/09/2025 confirma lançamento comercial ~set/2025."),

    ("Ergus","Nexus Renascença",
     "Endereço não localizado, Renascença, São Luís - MA","Renascença",
     "Vertical","Médio-alto","Em comercialização",
     None,"04/2026","—", 33,94,None, "Studio a 2Q",
     None,None, None,None,None,
     "site_oficial","N/A","imprensa",
     "https://www.ergus.com.br","14/04/2026",
     "Complexo 10mil m² multi-produto (residencial + comercial + Open Mall). Book local + site oficial."),

    # ═══ TREVISO ═══════════════════════════════════════════════════════
    ("Treviso","Vernazza Torre Norte",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Vertical","Alto","Em comercialização",
     120,"02/2025","12/2029", 130,130,None, "Aptos 130 m² — Leste/Sul/Norte",
     1820000,2235000, None,None, 0.4666666666666667,
     "tabela_local","tabela_local","informado",
     "https://www.treviso.com.br","23/04/2026",
     "Lançamento 02/2025 informado pelo Rafael (fonte externa confiável). Tabela de 02/2026 arquivada confirma vendas ativas naquela data, mas não é data de lançamento — aguarda book ou memorial para data confiável. Torre Norte: 37 unid, área 130 m², ticket R$ 1,82-2,24M (méd R$ 2,02M). R$/m² méd R$ 15.524. VGV listado R$ 74,8M. Entrega 12/2029. [reconstituído da v4.16 em 25/04/2026]"),

    ("Treviso","Vernazza Torre Sul",
     "Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Vertical","Alto","Em comercialização",
     None,"02/2025","12/2029", 87.98,90.1,None, "87,98 e 90,10 m² (Norte/Sul)",
     1277000,1586000, None,None, None,
     "tabela","tabela","informado",
     "—","23/04/2026",
     "Lançamento 02/2025 informado pelo Rafael. 26 unid listadas, área 87,98/90,10 m². Ticket R$ 1,28-1,59M (méd R$ 1,40M). R$/m² pond R$ 15.600 (faixa R$ 14,2-17,6k). VGV listado R$ 36,3M. Entrega 12/2029. [reconstituído da v4.16 em 25/04/2026]"),

    ("Treviso","Altos do São Francisco",
     "Bairro São Francisco, São Luís - MA","São Francisco",
     "Vertical","Médio-alto","Entregue",
     26,"01/2024 ⚠ T-36","Pronto", 57.93,67.15,None, "2-3Q (1 ou 2 vagas)",
     495800,761700, None,None, None,
     "tabela","tabela","pendente",
     "https://trevisoengenharia.com.br","23/04/2026",
     "IMÓVEL PRONTO. 26+ unid na tab ABR/26 (VGV R$ 15,8M). Tipos: 57,93 m² (1 vaga) e 67,15 m² (2 vagas). Ticket R$ 495k–762k (méd R$ 607k). R$/m² pond R$ 10.042. Estoque amplo. [reconstituído da v4.16 em 25/04/2026]"),

    # ═══ NIÁGARA ═══════════════════════════════════════════════════════
    ("Niágara","ORO Ponta d'Areia",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Vertical",None,"Lançamento",
     None,"01/2026 ⚠ T-36","~2029", 80.32,160.64,None, "2-4 suítes",
     1000000,2600000, None,None,None,
     "tabela_local","N/A","estimativa_T-36",
     "https://www.niagara-imoveis.com.br","14/04/2026",
     "Tabela JAN/26 é matriz por posição (não espelha estoque). Duplex cobertura 160m². Parcelamento 48m pós-assinatura."),

    # ═══ MOTA MACHADO ═══════════════════════════════════════════════════
    ("Mota Machado","Edifício Bossa",
     "Avenida dos Holandeses, Lote 07, Quadra 02, Calhau, São Luís - MA","Calhau",
     "Vertical",None,"Lançamento",
     60,"04/2026","09/2030", 191.02,196.04,None, "4 suítes (1 master c/ varanda, closet, banheiro duplo) + lavabo + varanda gourmet + qto/WC serviço",
     2850507,3708342, None,None, 36/60,
     "tabela_local","tabela_local","tabela_local",
     "https://motamachado.com.br","27/04/2026",
     "LANÇAMENTO 04/2026 — evento oficial 09/04/2026 (Frisson, MaHoje, Portal IN). 2 torres (Harmonia + Sintonia) × 15 pavtos tipo × 2 aptos/andar = 60 aptos. 6 elevadores. 3 tipologias: 191,02 / 192,64 / 196,04 m². 3 vagas (até 12º andar) ou 4 vagas (13º+ premium). Tabela 04/2026: 36 aptos disponíveis (24 vendidos = 40%). Tickets R$ 2,85-3,71M. R$/m² médio R$ 16.663 (faixa 14,9-19,2k — andares altos finais 01/02 tocam Luxo). Entrega 09/2030 (T-53). Memorial R 01, Matrícula 134.922 - 1º RI SL. Projeto: Nasser Hissa Arquitetos. Lazer: brinquedoteca, salão festas, academia, pista funcional, quadra, lounge champanheira, piscina, pet wash, minimercado, estação carro elétrico. Mota Machado (CE) expandindo no NE, VGV 2025 R$350M."),

    ("Mota Machado","Reserva São Marcos",
     "Endereço não localizado, Calhau, São Luís - MA","Calhau",
     "Vertical","Alto","Em comercialização",
     None,"01/2025","—", None,None,None, "—",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://www.motamachado.com.br","14/04/2026",
     "Obras iniciadas 09/2025. Empresa de Fortaleza expandindo no Nordeste. SEM material local."),

    ("Mota Machado","Entre Rios",
     "Rua dos Bicudos, S/N, Qd. XIV-A Lote 02, Renascença, São Luís - MA","Renascença",
     "Vertical","Alto","Lançamento",
     None,"08/2024","—", 125,157,None, "3 suítes (1 master)",
     1732000,2720000, None,None, None,
     "tabela","tabela","book",
     "https://motamachado.com.br","23/04/2026",
     "3 tipologias (125 / 146,82 / 156,94 m²). 2 torres x 15 pav. Tab ABR/26: 15 unid, VGV R$ 32,3M. Ticket R$ 1,73–2,72M (méd R$ 2,15M). R$/m² pond R$ 15.162 (faixa R$ 13,9k–17,3k). Rua dos Bicudos, Renascença. [reconstituído da v4.16 em 25/04/2026]"),

    ("Mota Machado","Al Mare Tirreno",
     "Av. dos Holandeses, Qd 9 Lt 9, São Marcos, São Luís - MA","São Marcos",
     "Vertical","Alto","Em comercialização",
     None,"08/2024","Pronto", 215,215,None, "4 suítes, 3 vagas",
     3025856,3120721, None,None, None,
     "tabela","tabela","book",
     "https://motamachado.com.br","23/04/2026",
     "Torre A 'Tirreno' da Mota Machado Collection. Imóvel PRONTO. 215 m², 4 suítes, 3 vagas. Apts 102, 201, 202 listados. Ticket R$ 3,02-3,12M. R$/m² méd R$ 14.293. Av. dos Holandeses / São Marcos. [reconstituído da v4.16 em 25/04/2026]"),

    # ═══ BERG ══════════════════════════════════════════════════════════
    ("Berg Engenharia","Monte Meru",
     "Endereço não localizado, Ponta d'Areia, São Luís - MA","Ponta d'Areia",
     "Vertical",None,"Em comercialização",
     None,"04/2024","04/2027", 135.32,135.83,None, "Aptos 135 m², 2-3 vagas",
     1932400,1944500, None,None,None,
     "tabela_local","tabela_local","imprensa",
     "https://www.bergengenharia.com.br","27/04/2026",
     "Tabela ABR/2026 (Berg Engenharia). 4 tipologias (1-4) com áreas similares 135,32 / 135,83 m². Lançamento 04/2024 estimado pela pasta. Conclusão: 30/04/2027 (T-36 perfeito). Tipo 3 (135,32m²): apto 103 disponível R$ 1.932.400. Tipo 4 (135,83m²): apto 104 disponível R$ 1.944.500, demais (204-1004) VENDIDOS = 9 vendidos no Tipo 4 → estoque concentrado em 1 unidade visível. Apto 704 tem 3 vagas (diferencial). Correção INCC. Histórico Berg: Montparnasse, Golden Tower, Peninsula Mall, Monte Olimpo, Monte Fuji."),

    ("Berg Engenharia","Mount Solaro",
     "Endereço não localizado, São Luís - MA","São Luís",
     "Vertical",None,"Pré-lançamento",
     None,"06/2025 ⚠ T-36","—", None,None,None, "—",
     None,None, None,None,None,
     "N/A","N/A","imprensa",
     "https://www.bergengenharia.com.br","14/04/2026",
     "SPE Berg + Gonçalves requereu Licença de Instalação (Diário Oficial SL)."),

    # ═══ SÁ CAVALCANTE ══════════════════════════════════════════════════
    ("Sá Cavalcante","Ilha Parque Residence",
     "Endereço não localizado, Maranhão Novo, São Luís - MA","Maranhão Novo",
     "Horizontal","Médio","Entregue",
     120,"02/2019","Entregue", 64,85,None, "2-3 quartos",
     None,None, None,None,None,
     "N/A","N/A","site_oficial",
     "https://www.sacavalcante.com.br","14/04/2026",
     "120 aptos (60 2Q + 60 3Q), 12/andar, 15 pavs. Pronto p/ morar. Ao lado do Shopping da Ilha."),

    # ═══ v4.1 — NOVOS EMPREENDIMENTOS MAPEADOS VIA WEB (14/04/2026) ═══

    # ─── MOTA MACHADO (atualização Bossa com dados de imprensa) ───
    # (mantém linha Bossa anterior e adiciona nada; obs complementar abaixo só para referência)

    # ─── ALFA ENGENHARIA — Giardino Residenza split (Torre Fiore Norte + Torre Luce Sul) ───
    ("Alfa Engenharia","Giardino Residenza Torre Fiore",
     "Ponta do Farol, São Luís - MA","Ponta do Farol",
     "Vertical","Alto","Últimas unidades",
     45,"02/2025","12/2029", 110.77,128.37,None, "2 suítes + 2 semi-suítes OU 3 suítes, varanda, lavabo, 3 vagas, depósito",
     1838492,2032939, None,None, 6/45,
     "tabela_local","tabela_local","memorial",
     "https://www.instagram.com/alfaengenhariama/","27/04/2026",
     "Torre NORTE do Giardino. 15 pav × 3 un = 45 unidades. 3 tipologias: 127,30 / 128,37 / 110,77 m². Tabela MAR/2026: 6 unidades disponíveis (1001/701/201/101 da coluna 127m², 102 da coluna 128m², 1403 da coluna 110m²) = ~13% estoque, 87% VENDIDO → Últimas unidades. Entrega DEZ/29. Memorial R.06/56.931 - 1º RI SL. Endereço Alfa: Rua Peixe Pedra, Qd 12 lote 04, Calhau."),

    ("Alfa Engenharia","Giardino Residenza Torre Luce",
     "Ponta do Farol, São Luís - MA","Ponta do Farol",
     "Vertical","Alto","Últimas unidades",
     60,"02/2025","12/2029", 93.18,101.31,None, "3 suítes, varanda, lavabo, 2 vagas, depósito",
     1442168,1595303, None,None, 5/60,
     "tabela_local","tabela_local","memorial",
     "https://www.instagram.com/alfaengenhariama/","27/04/2026",
     "Torre SUL do Giardino. 15 pav × 4 un = 60 unidades. 4 tipologias: 99,08 / 101,31 / 93,18 / 93,62 m². Tabela MAR/2026: 5 unidades disponíveis (701/101 col 99m², 1502/1402 col 101m², 104 col 93m²) = ~8% estoque, 92% VENDIDO → Últimas unidades. CORREÇÃO v5.1: dorms = 3 suítes (descrição da tabela MAR/26), antes constava '2 suítes/1 suíte' incorretamente. 2 vagas + 1 depósito. Mais acessível que Torre Fiore. Entrega DEZ/29. Memorial R.06/56.931 - 1º RI SL."),

    # ─── TREVISO — Villagio Treviso ───
    ("Treviso","Villagio Treviso",
     "Endereço não localizado, São Luís - MA","São Luís",
     "Horizontal",None,"Em comercialização",
     None,"06/2025 ⚠ T-36","—", None,None,None, "Terrenos em condomínio",
     None,None, None,None,None,
     "N/A","N/A","site_oficial",
     "https://trevisoengenharia.com.br","14/04/2026",
     "Condomínio de terrenos (loteamento fechado). Divulgação ativa abr/2026. Sem tabela pública mapeada."),

    # ─── CANOPUS — 3 lançamentos out/2025 (Imirante) ───
    ("Canopus","Village Reserva II",
     "Endereço não localizado, São Luís - MA","São Luís",
     "Horizontal",None,"Lançamento",
     None,"10/2025","—", None,None,None, "—",
     None,None, None,None,None,
     "N/A","N/A","imprensa",
     "https://canopusconstrucoes.com.br","14/04/2026",
     "1 dos 3 novos lançamentos Canopus anunciados em 31/10/2025 (Imirante). SEM tabela ou book mapeado."),

    ("Canopus","Village Prime Eldorado",
     "Endereço não localizado, Jardim Eldorado, São Luís - MA","Jardim Eldorado",
     "Horizontal",None,"Lançamento",
     None,"10/2025","—", None,None,None, "—",
     None,None, None,None,None,
     "N/A","N/A","imprensa",
     "https://canopusconstrucoes.com.br","14/04/2026",
     "Canopus em movimento forte no Eldorado. Fonte: Imirante 31/10/2025."),

    ("Canopus","Village Del Ville II",
     "Endereço não localizado, São Luís - MA","São Luís",
     "Horizontal",None,"Lançamento",
     None,"10/2025","—", None,None,None, "—",
     None,None, None,None,None,
     "N/A","N/A","imprensa",
     "https://canopusconstrucoes.com.br","14/04/2026",
     "Série Village (estratégia de marca clara). Imirante 31/10/2025. Confirmar tipologia/ticket via site+IG."),

    # ─── CASTELUCCI — 3 empreend. mapeados (site + Instagram + agregador) ───
    ("Castelucci","Vila Coimbra",
     "Endereço não localizado, Araçagi, São Luís - MA","Araçagi",
     "Horizontal",None,"Lançamento",
     None,"03/2026","03/2029", 124.63,124.63,None, "Casa 124,63 m² (terreno 164-204 m²)",
     1019834,1081967, None,None,None,
     "tabela_local","N/A","book",
     "https://construtoracastelucci.com.br","27/04/2026",
     "Tabela LANÇAMENTO 03/2026. Parceria Castelucci + Grupo Coimbra Alves. ~36-41 casas no Araçagi (numeração até casa 41, várias agrupadas: 02-17, 36-38, 39-40). Área construída UNIFORME 124,63 m². Terreno varia 164-204 m². Ticket à vista R$ 1.019.834 (casa 21) a R$ 1.081.967 (casa 41) — VARIAÇÃO POR TAMANHO DE TERRENO, não por área construída. Avaliação: R$ 915.000. Pagamento: 24m IPCA+0,49% / 36m IPCA+1,49% / Caixa. Lazer privativa não integrada ao preço. Paulo Castelucci (CEO) em entrevista à Mirante FM. Patrocínio Imob Summit 2026."),

    ("Castelucci","Villa di Carpi",
     "Endereço não localizado, Cohatrac, São Luís - MA","Cohatrac",
     "Horizontal",None,"Em comercialização",
     None,"06/2024 ⚠ T-36","—", 49,52,None, "2Q",
     None,None, None,None,None,
     "agregador","N/A","site_oficial",
     "https://construtoracastelucci.com.br","14/04/2026",
     "Compactos 49-52m², 2Q. Público Cohatrac/médio. Instagram @construtoracastelucci anunciou como lançamento; preço não divulgado."),

    ("Castelucci","Residencial Ana Vitória",
     "Endereço não localizado, Araçagy, São Luís - MA","Araçagy",
     "Horizontal",None,"Em comercialização",
     None,"01/2018","—", None,None,None, "2-3Q",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://construtoracastelucci.com.br","14/04/2026",
     "Apartamentos 2-3Q Araçagy. Site oficial Castelucci."),

    # ─── FRANERE — série Gran Park ───
    ("Franere","Varandas Grand Park",
     "Endereço não localizado, São Luís - MA","São Luís",
     "Horizontal",None,"Em comercialização",
     None,"06/2024 ⚠ T-36","—", None,None,None, "—",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://franere.com.br","14/04/2026",
     "Franere ('Maior construtora do Maranhão', 40 anos). Série 'Gran Park' tem múltiplos módulos. IG @franereoficial_."),

    # ─── LUA NOVA — 2 empreend. ───
    ("Lua Nova","Villa Adagio",
     "Endereço não localizado, São Luís - MA","São Luís",
     "Horizontal",None,"Em comercialização",
     None,"06/2024 ⚠ T-36","—", None,None,None, "—",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://construtoraluanova.com.br","14/04/2026",
     "Construtora Lua Nova desde 1985. IG @construtoraluanova. Detalhes tipologia/ticket a coletar via book."),

    ("Lua Nova","Lagoon Residence",
     "Endereço não localizado, Santo Amaro, São Luís - MA","Santo Amaro",
     "Vertical",None,"Em comercialização",
     None,"04/2026","—", None,None,None, "—",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://construtoraluanova.com.br","14/04/2026",
     "Residência no Santo Amaro — região com oferta crescente de médio padrão."),

    # ─── MB ENGENHARIA — 3 empreend. ───
    ("DOM Incorporação","Edifício Dom Ricardo",
     "Rua dos Rouxinóis, 8, Jardim Renascença, São Luís - MA","Jardim Renascença",
     "Vertical",None,"Últimas unidades",
     None,"12/2023","—", 71,85,None, "2-3Q",
     None,None, None,None, 0.06,
     "agregador","agregador","interno",
     "https://www.imeu.com.br/empreendimento/dom-ricardo-apartamentos-sao-luis-2-a-3-quartos-71-a-85-m/19044585-MIM","23/04/2026",
     "DOM Incorporação com MB Engenharia como sócia (empreendimento conjunto). Lançamento 12/2023 confirmado internamente. Próximo à Praça da Lagoa (Foguete). 'Sucesso de vendas, 6 unidades disponíveis' (IG jan/2025). Estoque estimado ≤6%. [reconstituído da v4.16 em 25/04/2026]"),

    ("MB Engenharia","Condomínio Prime Cohama",
     "Endereço não localizado, Cohama, São Luís - MA","Cohama",
     "Vertical",None,"Em comercialização",
     22,"01/2026","—", 140,140,None, "Casas duplex",
     None,None, None,None,None,
     "N/A","N/A","imprensa",
     "https://www.instagram.com/mbengenharia.br/","14/04/2026",
     "22 casas duplex 140m² — produto horizontal diferenciado. Pré-lançamento anunciado 2023, hoje em comercialização."),

    ("DOM Incorporação","Dom Antônio",
     "Endereço não localizado, Jardim Eldorado (Turú), São Luís - MA","Jardim Eldorado",
     "Horizontal","Médio","Em comercialização",
     None,"06/2023","—", 136,136,None, "3Q casas duplex",
     906870,906870, None,None,None,
     "agregador","N/A","interno",
     "https://www.imovelnacidade.com/destaque/mb-construtora/","23/04/2026",
     "DOM Incorporação com MB Engenharia como sócia (empreendimento conjunto). Lançamento 06/2023 confirmado internamente. Casa duplex 3Q, 136m², R$906.870. Produto horizontal Eldorado/Turú. [reconstituído da v4.16 em 25/04/2026]"),

    # ─── MONTEPLAN — 2 empreend. ativos ───
    ("Monteplan","Renaissance Conceito",
     "Rua Caxuxa, S/N, Renascença II, São Luís - MA","Renascença II",
     "Vertical","Alto","Lançamento",
     None,"06/2025 ⚠ T-36","—", None,None,None, "3Q",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://monteplanengenharia.com.br/empreendimentos/renaissance-conceito/","14/04/2026",
     "Alto padrão Renascença II (Loteamento Boa Vista). Dois torres, lazer completo."),

    ("Monteplan","Edifício Sanpaolo",
     "Endereço não localizado, São Luís - MA","São Luís",
     "Vertical","Médio-alto","Esgotado",
     None,"12/2022","—", None,None,None, "2-3Q",
     None,None, None,None, 0.0,
     "site_oficial","site_oficial","site_oficial",
     "https://monteplanengenharia.com.br/empreendimentos/edificio-sanpaolo/","14/04/2026",
     "2Q (2 suítes, 1 reversível) ou 3Q (1 suíte). 'Todas as unidades vendidas' (Facebook out/2025)."),

    ("Monteplan","Residencial Novo Anil",
     "Rua Estevão Braga, Cohab Anil IV, São Luís - MA","Cohab Anil IV",
     "Vertical","Médio","Entregue",
     None,"01/2022","Pronto", 53.94,53.94,None, "—",
     324142,324142, None,None, None,
     "tabela","tabela","memorial",
     "https://monteplanengenharia.com.br","23/04/2026",
     "OBRA CONCLUÍDA (Monteplan, Cohab Anil IV). 32 unid listadas, todas ~R$ 324.142 (área 53,94 m²). R$/m² uniforme R$ 6.009. Padrão popular. SFH 60%. VGV residual listado R$ 10,4M. [reconstituído da v4.16 em 25/04/2026]"),

    # ─── SÁ CAVALCANTE — Reserva Península (novo) ───
    ("Sá Cavalcante","Reserva Península",
     "Endereço não localizado, Ponta d'Areia (Península), São Luís - MA","Ponta d'Areia",
     "Vertical","Alto","Lançamento",
     None,"10/2025","—", None,None,None, "—",
     None,None, None,None,None,
     "site_oficial","N/A","site_oficial",
     "https://www.instagram.com/sacavalcantema/","14/04/2026",
     "Lançamento Sá Cavalcante out/2025. Estande 'Casa Sal' na Península. 'Os espaços conversam...' — narrativa de estilo de vida."),

    # ═══ HIALI ═════════════════════════════════════════════════════════
    ("Hiali","Le Noir",
     "Rua Osires, 05, Renascença II, São Luís - MA","Renascença II",
     "Vertical","Alto","Lançamento",
     25,"04/2025","12/2027", 49.74,62.62,None, "Studios e 1-2 dorm (compactos premium)",
     710000,870000, None,None, None,
     "tabela","tabela","memorial",
     "","23/04/2026",
     "Parceria Hiali + Silveira Inc. Compactos premium: 49,74 / 58,91 / 62,62 m². 5 pavimentos tipo × 5 aptos/andar = ~25 unidades. Entrega DEZ/2027. Ticket R$ 710-870k. R$/m² méd R$ 13.810. Memorial R.09/25.101 registrado 17/04/2025 no 1º RI São Luís. Foco em mercado jovem / investidor. [reconstituído da v4.16 em 25/04/2026]"),

    # ═══ DOM INCORPORAÇÃO (própria) ═════════════════════════════════════
    ("DOM Incorporação","Dom Lucas",
     "Tv. Boa Esperança, 101 - Cantinho do Céu, São Luís - MA, 65074-030","Cantinho do Céu",
     "Horizontal",None,"Em comercialização",
     None,"02/2026","01/2029", 100.35,100.35,None, "Casa 3 dorm (1 suíte) + 2 vagas",
     835000,851000, None,None, None,
     "tabela","tabela","interno",
     "","27/04/2026",
     "Condomínio horizontal (sobrados). 1 ÚNICA tipologia: casa 100,35 m² construída (área usada para R$/m²). Terreno varia 136-146 m² conforme posição. ~38 casas. Lazer: campo society, piscina, deck, salão, gourmet, petplay, playground. Muitas unidades VENDIDAS. Entrega 01/2029. Ticket R$ 835-851k → R$/m² construção ~R$ 8.400. CORREÇÃO v5.2: Área máx era 145,78 (terreno) — corrigida para 100,35 (construída). Convenção PADRAO §1: Tipo=Horizontal usa área construída."),

    ("DOM Incorporação","Dom José",
     "FQV9+JJ Jardim Eldorado, São Luís - MA","Jardim Eldorado",
     "Horizontal",None,"Em comercialização",
     None,"06/2024","06/2027", 154.64,154.64,None, "Casa 4+ dorm, alto padrão",
     1400000,1415000, None,None, None,
     "tabela","tabela","interno",
     "","27/04/2026",
     "Condomínio horizontal alto padrão. 1 ÚNICA tipologia: casa 154,64 m² construída. Terreno varia 170-181 m² conforme posição. Maioria das unidades VENDIDAS (14+ marcadas VENDIDA na tabela ABR/2026). Entrega 06/2027. Ticket ~R$ 1,4M → R$/m² construção ~R$ 9.150. CORREÇÃO v5.2: Área máx era 180,98 (terreno) — corrigida para 154,64 (construída). Convenção PADRAO §1: Tipo=Horizontal usa área construída."),
]

# ═══════════════════════════════════════════════════════════════
# VALIDAÇÃO §0.1 do PADRAO v2.0: Mês lançamento DEVE ser MM/AAAA (com ⚠ T-36
# opcional) ou "—". Qualquer outro formato (AAAA puro, ~AAAA) é REJEITADO.
# ═══════════════════════════════════════════════════════════════
import re as _re_validate
_RGX_MES = _re_validate.compile(r'^(\d{2}/\d{4}( ⚠ T-36)?|—)$')
_problemas = []
for _row in E_RAW:
    _inc, _emp, _mes = _row[0], _row[1], _row[8]  # idx 8 = Mês lançamento
    if _mes is None:
        _problemas.append(f"  • {_inc} | {_emp}: Mês lançamento é None — usar \"—\" se faltam dados")
    elif not _RGX_MES.match(str(_mes)):
        _problemas.append(f"  • {_inc} | {_emp}: Mês lançamento {_mes!r} fora do padrão MM/AAAA")
if _problemas:
    raise ValueError(
        "❌ VALIDAÇÃO PADRAO v2.0 §1 (col 9 — Mês lançamento) FALHOU:\n" +
        "\n".join(_problemas) +
        "\n\nFormato exigido: MM/AAAA, ou MM/AAAA ⚠ T-36, ou \"—\" (sem dados)."
    )

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
                         "Referência de luxo em Ponta d'Areia; 7 empreend. mapeados (ticket R$530k-R$5,8M). 2026 traz forte movimento no Calhau: Landscape (lançamento) + The View (pré-lançamento ABR/2026, 36-101m², 17º andar premium ~R$18k/m²)."),
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
                         "Sócia da DOM Incorporação em Dom Antônio + Edifício Dom Ricardo (reclassificados como DOM em v4.18). Próprios: Prime Cohama (22 casas duplex 140m²) + Fernando de Noronha 2ª etapa."),
    "Sá Cavalcante":    ("https://www.sacavalcante.com.br","@sacavalcantema",
                         "Grupo desde 1974 (shoppings + incorporação). Ilha Parque entregue + NOVO Reserva Península (out/2025, Ponta d'Areia)."),
    "Castelucci":       ("https://construtoracastelucci.com.br","@construtoracastelucci",
                         "10+ anos. CEO Paulo Castelucci (Mirante FM). Vila Coimbra (parceria Coimbra Alves, Araçagi alto padrão) + Villa di Carpi (Cohatrac) + Ana Vitória (Araçagy). Patrocinador Imob Summit."),
    "Hiali":            ("","@hialiconstrucoes",
                         "Parceria com Silveira Inc. Le Noir (Renascença II): compactos premium 49-62m², ticket R$ 710-870k. Memorial 04/2025. Posicionamento jovem/investidor. Mapeada via tabela arquivada."),
    "DOM Incorporação": ("https://domincorporacao.com.br","@domincorporacao",
                         "EU. Portfólio próprio: Dom Lucas (horizontal Cantinho do Céu, 100m²+terreno, R$ 835-851k), Dom José (horizontal Eldorado alto padrão, casa 154m², R$ 1,4M). Em parceria com MB Engenharia: Dom Antônio (Turú) + Edifício Dom Ricardo (Jd. Renascença). Tracked aqui para benchmarking interno."),
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
    PADRAO v2.0 §1: formato esperado é SEMPRE MM/AAAA (com flag opcional ⚠ T-36).
    Retorna (0,0) para vazios E para formatos inválidos (AAAA puro, ~AAAA) —
    todos vão para o fim em ordem decrescente, sinalizando que falta dado preciso."""
    if not mes_str or mes_str=="—":
        return (0, 0)
    import re
    # Aceita SOMENTE MM/AAAA (com ou sem ⚠ T-36)
    m = re.match(r'^(\d{1,2})/(\d{4})( ⚠ T-36)?$', mes_str)
    if m:
        return (int(m.group(2)), int(m.group(1)))
    # Formato inválido — vai pro fim (faltam dados)
    return (0, 0)

# Processa cada empreendimento: preenche campos calculados
E_PROCESSED = []
for row in E_RAW:
    row = list(row)
    # calcular área média (idx 12 — antes 11; +1 por inserção da col Tipo)
    if row[12] is None:
        row[12] = calc_area_media(row[10],row[11])
    # calcular preço médio R$/m² (idx 16 — antes 15)
    if row[16] is None:
        row[16] = calc_preco_m2(row[14],row[15],row[10],row[11])
    # calcular VGV (idx 17 — antes 16)
    if row[17] is None:
        row[17] = calc_vgv(row[14],row[15],row[7])
    # auto-classificar segmento se não definido (idx 5 — antes 4)
    if row[5] is None and row[16] is not None:
        row[5] = classificar_segmento_por_m2(row[16])
    elif row[5] is None:
        row[5] = "—"
    # auto-reclassificar status pelo estoque (idx 6 usando idx 18)
    row[6] = reclassificar_status(row[6], row[18])
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
N_COLS_E = 25
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
    "Incorporadora","Empreendimento","Endereço","Bairro","Tipo","Segmento","Status",
    "Nº unid.","Mês lançamento","Mês entrega",
    "Área mín (m²)","Área máx (m²)","Tipologia média (m²)","Tipologia (dorms)",
    "Ticket mín (R$)","Ticket máx (R$)","R$/m²","VGV (R$)","% Vendido",
    "Orig. preços","Orig. estoque","Orig. lançamento",
    "Link fonte principal","Data verif.","Observações"
]
apply_header_row(ws1,5,headers_e)

formats_e = [None]*N_COLS_E
formats_e[10] = formats_e[11] = formats_e[12] = '0.0'
formats_e[14] = formats_e[15] = 'R$ #,##0'
formats_e[16] = 'R$ #,##0'
formats_e[17] = 'R$ #,##0'
formats_e[18] = '0.0%'

# §7 PADRAO.md: ordenar por Mês Lançamento DESCENDENTE (mais recente 1º),
# depois Incorporadora A-Z, depois Empreendimento A-Z
empreend_sorted = sorted(
    E_PROCESSED,
    key=lambda r: (
        -parse_launch_date(r[8])[0],  # ano desc
        -parse_launch_date(r[8])[1],  # mês desc
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
    if isinstance(row_values[18], (int, float)):
        row_values[18] = 1 - row_values[18]
    for j, v in enumerate(row_values):
        cel = ws1.cell(row=row_idx, column=1+j, value=v)
        cel.font = font(DOM_GRAY_DARK, 9)
        cel.fill = fill(row_fill)
        cel.alignment = left() if j in (2, 13, 24) else center()
        cel.border = border_thin()
        if formats_e[j]:
            cel.number_format = formats_e[j]
    # Sem coloração condicional na coluna % Vendido (Rafael pediu p/ remover)
    # Destaque da incorporadora
    ws1.cell(row=row_idx, column=1).font = font(DOM_GRAY_DARK, 9, bold=True)

total_row_e = 6+len(empreend_sorted)

widths_e = [15,22,30,14, 11, 11,17, 7,14,11, 10,10,11,20, 13,13,11,14,10,
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
    vgv_list = [r[17] for r in emps if r[17] is not None]
    vgv_total = sum(vgv_list) if vgv_list else None
    vgv_2024=vgv_2025=vgv_2026=0
    for r in emps:
        if r[17] is None: continue
        y = extract_year(r[8])
        if y==2024: vgv_2024 += r[17]
        elif y==2025: vgv_2025 += r[17]
        elif y==2026: vgv_2026 += r[17]
    segs = sorted(set(r[5] for r in emps if r[5] and r[5]!="—"))
    bairros = sorted(set(r[3] for r in emps if r[3]))
    tickets = []
    for r in emps:
        if r[14] is not None and r[15] is not None:
            tickets.append((r[14]+r[15])/2)
    ticket_med = sum(tickets)/len(tickets) if tickets else None
    precos_m2 = [r[16] for r in emps if r[16] is not None]
    preco_m2_med = sum(precos_m2)/len(precos_m2) if precos_m2 else None
    # % com arquivo: heurística — se tem tabela_local em preços OU estoque
    com_arquivo = sum(1 for r in emps if r[19]=="tabela_local" or r[20]=="tabela_local")
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
BASE = "/sessions/intelligent-festive-lamport/mnt"
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
print(f"  VGV total mapeado: R$ {sum(r[17] for r in E_PROCESSED if r[17]):,.0f}")
print(f"  Preço médio calculado para: {sum(1 for r in E_PROCESSED if r[16])} de {len(E_PROCESSED)} empreend.")
