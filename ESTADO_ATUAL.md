# ESTADO ATUAL — Inteligência de Mercado DOM

> **Para Claude (toda sessão):** este é o **primeiro arquivo a ler** antes de qualquer ação. Confirma a base de trabalho. Se a invariante 0.3 do PADRAO falhar contra os números aqui, **PARAR**.

**Última atualização:** 03/05/2026
**Versão Planilha vigente:** v11.1
**Versão PADRAO vigente:** v7.0
**Versão script `gerar_planilha.py`:** 11.1 (DATE_STR: 03/05/2026)

---

## Snapshot da carteira (v11.1)

| Métrica | Valor |
|---|---:|
| Aba Empreendimentos | **44 linhas** (sem mudança vs v10.9) |
| Aba Incorporadoras | **16 linhas** (em rota de eliminação — backlog R2) |
| Aba Composição | **78 linhas / 2.246 unidades / 34 empreend.** ← granularidade de PLANTA refinada (era 53 em v11.0; +25 plantas pelos 6 re-parsed) |
| Fonte de C_RAW | **29 arquivos YAML** em `composicao/<inc>__<emp>.yaml` (R1 done — não é mais hardcoded) |
| Aba Empreendimentos schema | **27 colunas** (sem mudança) |
| Aba Composição schema | **12 colunas (v7.0)** ← +1 vs v6.2 (Planta + Área única + Total planta separado de Disp) |
| Drift script ↔ planilha | **0** ✅ |
| VGV total mapeado | **R$ 2,52 bi** (sem mudança — ajuste de granularidade não muda VGV) |
| Cobertura Composição | **34/44 empreend. = 77%** (mantida vs v10.9) |
| **Invariante v6.2 Σ Total tip = E_RAW.Total** | **30/34 fechado exato** ⚠ 4 parciais (Vila Coimbra, Le Noir, Bossa, Reserva SM) |
| **Invariante v7.0 Σ Total planta = Total tip** | **49/49 fechado exato** ✅ (NOVA — pro-rata fecha por construção) |
| Bloqueados sem Total | **10 empreend.** → `pendencias_TOTAL.md` (sem mudança) |
| **Plantas declaradas com label** | **9 plantas** (Renaissance Botticelli/Leonardo, Mount Solaro Loft 68/Apt 72/Apt 104, Dom Ricardo Col 1/2/3, Reserva SM Planta 1/2, Legacy 175m²/185m², ORO Padrão/Cobertura Duplex) |

### Cobertura por incorporadora (% empreend. com composição detalhada)

| Incorporadora | Empreend. total | Em Composição | % |
|---|---:|---:|---:|
| Delman | 7 | 7 | **100%** ✅ |
| Mota Machado | 4 | 4 | **100%** ✅ |
| Treviso | 4 | 3 | 75% |
| Monteplan | 3 | 3 | **100%** ✅ |
| Hiali | 1 | 1 | **100%** ✅ |
| Niágara | 1 | 1 | **100%** ✅ |
| Ergus | 2 | 1 | 50% (Zion via visão; Nexus pendente) |
| Castelucci | 3 | 1 | 33% |
| Demais (10 inc.) | 26 | 0 | 0% |

### Lote 2 (v8.1, 02/05/2026) — 13 linhas / 209 unidades

| Empreend. | Tipologias | Unid. | R$/m² médio |
|---|---|---:|---:|
| Vernazza Torre Norte (Treviso) | 4D | 37 | R$ 15.219 |
| Vernazza Torre Sul (Treviso) | 3D | 26 | R$ 15.599 |
| ORO Ponta d'Areia (Niágara) | 3D (88) + 4D (8) | 96 | R$ 15-16k |
| Entre Rios (Mota Machado) | 4D | 30 | R$ 14.679 |
| Reserva São Marcos (Mota Machado) | 2D + 4D | 6 | R$ 17k / 16k |
| Le Noir (Hiali) | 1D + 2D | 4 | R$ 14k / 13k |
| Quartier 22 (Delman) | 4D | 1 | R$ 18.182 |
| Sky Residence (Delman) | 4D | 1 | R$ 19.052 |
| Azimuth (Delman) | 4D | 1 | R$ 18.309 |
| Al Mare Tirreno (Mota Machado) | 4D | 1 | R$ 14.074 |
| Edifício Sanpaolo (Monteplan) | 1D | 2 | R$ 5.648 |

### Lote 1 (v8.0) — 15 linhas / 322 unidades
The View (Delman, 4 tipologias), Landscape (Delman, 2), Studio Design 7 Pen. (Delman, 3), Wave (Delman, 1), Edifício Bossa (Mota Machado, 1), Altos São Francisco (Treviso, 1), Renaissance Conceito (Monteplan, 2), Vila Coimbra (Castelucci, 1).

---

## Comando one-liner (versão vigente)

```bash
cd 00_ESTUDO_CONSOLIDADO/ && ls -1 Planilha_Mestre_Panorama_v*.xlsx | sort -V | tail -1
```

---

## Mudanças estruturais recentes

- **v6.0–v7.0.1** — limpezas, dashboard redesenhado, fix init.
- **v8.0** (02/05/2026) — Aba Composição introduzida. Lote 1: 15 linhas / 322 unid.
- **v8.1** (02/05/2026) — **Lote 2 entregue.** +13 linhas / +209 unid. Cobertura 17% → 39%.
- **v8.2** (02/05/2026) — **Lote 3 (parcial — Zion via visão multimodal).** +1 linha / +10 unid. Cobertura 39% → 41%.

- **v11.1** (03/05/2026) — **R1 entregue + re-parsing granular dos 6 com range grande.**
   - **(R1)** C_RAW migrado de hardcoded em Python para 29 arquivos YAML em `composicao/<inc>__<emp>.yaml`. Função `load_c_raw_from_dir()` carrega no startup. Schema 12-col v7.0 idêntico ao v11.0; smoke test confirma output bit-a-bit. Edição de empreend agora é YAML (zero-friction, qualquer editor), não mais Python.
   - **(Re-parsing)** 6 empreend. com range grande de área dentro da mesma tipologia foram re-parseados unidade-a-unidade via `pdftotext -layout` + parsers (Delman, Treviso Altos, Alfa) + bucketizador `bucketizar_plantas()`:
     - The View (Delman): 4 entries → **13 plantas** (93 unid parseadas)
     - Landscape (Delman): 2 → **4 plantas** (51 unid)
     - Studio Design 7 Península (Delman): 3 → **12 plantas** (32 unid)
     - Altos do São Francisco (Treviso): 1 → **2 plantas** (25 unid)
     - Giardino Fiore (Alfa): 1 → **3 plantas** (6 unid — Coluna 01 127m², Coluna 02 128m², Coluna 03 110m² — match exato com book)
     - Giardino Luce (Alfa): 1 → **3 plantas** (5 unid — Coluna 01 99m², Coluna 02 101m², Coluna 04 93m²)
   - C_RAW expandido de 53 → **78 linhas** (+25 plantas reais). Total unidades render mantido em 2.246. Invariantes §3.7.C.4 (30/34) e §3.7.C.6 (49/49) preservadas.
   - **Catálogo de parsers atualizado:** Alfa (parse_alfa) agora trata header "COLUNA NN - YYY,YYm²" pra atribuir área às unidades seguintes (formato Giardino).
   - Próxima frente backlog: R2 (eliminar aba Incorporadoras) ou R3 (U_RAW unidade-a-unidade) — definir quando voltar.

- **v11.0** (03/05/2026) — **VIRADA ESTRUTURAL §3.7 v7.0 — granularidade de PLANTA.** Decisão Rafael 03/05: "ticket dita absorção mais do que tipologia. Mesma 3D em 100m² vs 125m² tem público-alvo distinto (~R$400k de diferença de ticket = mudança de público)."
   - **(1) Aba Composição: schema 11 → 12 col.** Entram: `Planta` (label do book quando declarado: Botticelli, Loft 68, Coluna 1) + `Área (m²)` (única, não mais range). Sai: `Área mín/máx`. Total planta separado de Disp. Granularidade vira (empreend × tipologia × planta).
   - **(2) Invariante de 3 níveis.** Antes: `Σ Total tip = E_RAW.Total`. Agora: `Σ Total planta = Total tipologia` (NOVA §3.7.C.6) + `Σ Total tipologia = E_RAW.Total` (mantida §3.7.C.4). Ortogonalidade §3.6/§3.7 preservada — Total continua âncora.
   - **(3) Função `bucketizar_plantas()`** nova: agrupa parser output por área (round 1 dec) → 1 entry por planta. Função `compute_total_planta()` nova: pro-rata por planta dentro da tipologia (preserva comportamento v6.2 quando origem é tabela_local parcial).
   - **(4) Re-extração C_RAW:** 38 entries 10-col → **44 entries 12-col**. Plantas declaradas: Renaissance (Botticelli 82m² / Leonardo 110m²), Mount Solaro (Loft 68 / Apt 72 / Apt 104), Dom Ricardo (Coluna 1 85,75 / Coluna 2 84,96 / Coluna 3 71,92), Reserva São Marcos (Planta 1 / Planta 2), Legacy Residence (Planta 175m² / Planta 185m²), ORO (Padrão 80m² / Cobertura Duplex 160m²). Após estimativa nível 5 + multi-torre: **53 linhas / 2.246 unidades / 34 empreend.**
   - **(5) build_panorama v8.0.0:** `read_composicao()` lê schema 12-col com fallback v6.2. **Bubble de oferta** vira granular: cada bolha = (bairro × tipologia × planta), Y = Total planta render (oferta), tamanho = nº empreend. Permite leitura "3D 100m² em Calhau é mono-oferta vs 3D 125m² é disputado".
   - **(6) §3.7.B item 6 NOVO** — bucketização explícita no workflow. Catálogo §3.7.1 mantém os 8 parsers (não mudam — bucketizador opera sobre output deles).
   - **(7) Validações:** §3.7.C.1 (anti-dup) chave virou (inc, emp, tip, planta_label, area_round). §3.7.C.6 NOVA fecha 49/49. §3.7.C.4 mantida (30/34, 4 parciais não-pro-rata aceitos como WARN). PADRAO bumpa v6.2 → v7.0.

- **v10.9** (03/05/2026) — **+1 destravado manual (Rafael 03/05).** Legacy Residence (Alfa, Península): Total = 30 (2 apto/andar × 15 andares), mono-tipologia 4D em 2 plantas (15u 175m² + 15u 185m²). Áreas E_RAW atualizadas (175-180 → 175-185), origem total = `informado_manualmente`. C_RAW agregada §3.7: 4D 30 unid 175-185m², origem `informado_manualmente`. Convenção Mount Solaro: disp=Total como placeholder (Rafael forneceu apenas product specs, sem info de vendas — Observações flagam isso, lançamento 07/2024 sugere venda parcial). §3.7 nível 5.1 deixa de aplicar a Legacy. Cobertura Composição 33→34/44 = 77%. Invariante 30/30 fechada exato. Bloqueados 11→10. VGV mantido R$ 2,52 bi (tickets Legacy ainda pendentes — entrarão como calculáveis quando tabela comercial chegar). **Pendentes Tier A2 Alfa: restou Connect Península.** Tier A1 Canopus 2 / Tier B 6 / Tier C 1.

- **v10.8** (03/05/2026) — **WEB RESEARCH BATCH (15 bloqueados pesquisados).** +4 destravados completos via web/site oficial: **LIV Residence** (Alfa, 75u mono 3D 90,83-100,23m², site Alfa); **Residencial Ana Vitória** (Castelucci, 30 casas 83m² 2D;3D, site Castelucci); **Mount Solaro** (Berg+Gonçalves, 50u = 20+10+20 multi 2D+3D, site Gonçalves); **Village Prime Eldorado** (Canopus, 400u mono 2D 43,5m² em 5 torres, Imirante 31/10). +7 enriquecidos parciais (tipologia/área obtidas, total ainda falta): Legacy Residence (4D 175-180m²), Reserva Península (4D 127-171m²), Varandas Grand Park (3D 74-87m²), Villa Adagio (2D 48,9m²), Village Reserva II (2D 41m²), Village Del Ville II (2D 42-43m²), Villa di Carpi (3 plantas 2D 49-52m²). +3 correções de bairro: Mount Solaro→Península, Varandas→Calhau, Villa Adagio→Iguaíba. **Achado fora-do-escopo:** Lagoon Residence (Lua Nova) é Santo Amaro do Maranhão (cidade satélite, NÃO Grande SLZ) — flag pra Rafael decidir manter/tirar. Cobertura 27→33/44 = 75%, bloqueados 17→11.

- **v10.7** (03/05/2026) — **+2 destravados manuais (Rafael 03/05).** Dom Antônio: 12 casas 136,2m² mono 3D (origem informado_manualmente, §3.7 nível 5.1 aplica auto). Edifício Dom Ricardo: 30 unid (10 andares × 3 col) com book DOM 12/2023: 10u 2D 71,92m² + 20u 3D 84,96-85,75m² (origem book; book diz "100% vendido" → estoque manual 0.0). Função `compute_total_per_tipologia` ganha `BOOK_TOTAL_OVERRIDE` para casos onde origem `book` declara totais e c[3]=disp não basta. Cobertura 27→29/44 = 66%, invariante 25/25 fechada, VGV R$ 2,48→2,51 bi. Bloqueados 17→15.

- **v10.6** (03/05/2026) — **VIRADA ESTRUTURAL §3.7 v2 (PADRAO v6.2).** Tema: composição obrigatória + análises por unidades.
   - **(1) Consolidação multi-torre regra A (§3.7.D):** Vernazza Torre Norte (120) + Torre Sul (60) → "Vernazza Residenza" (180); Giardino Residenza Torre Fiore (45) + Luce (60) → "Giardino Residenza" (105). Carteira **46 → 44 empreendimentos**.
   - **(2) Aba Composição schema 10 → 11 col**: nova coluna "Total tipologia" entre "Tipologia" e "Disponíveis" (renomeada de "Nº Unidades"). Total tipologia computado em runtime (mono em C_RAW: Total empreend.; multi origem completa: Σ disp já bate; multi parcial: pro-rata com sufixo origem `_pro_rata`).
   - **(3) Hierarquia §3.7.A ganha NÍVEL 5 `estimativa_distribuição`** com 4 sub-regras: 5.1 mono / 5.2 multi+área / 5.3 multi sem área / 5.4 sem tipologia. Aplicada automaticamente em runtime aos empreend. com Total mas sem C_RAW. Marcação visual itálico+cinza na xlsx.
   - **(4) Invariante v6.2: Σ Total tipologia = E_RAW.Total** para todo empreend. com Total apurado. Validação §3.7.C.4 nova. Reconciliação automática de estimativas nível 5; fontes fortes (1-4) que não fechem geram WARN sem alterar Total. **Resultado 1ª execução: 23/23 fechado exato.**
   - **(5) Aplicação automática 5.x nos 3 destraváveis:** Ilha Parque (5.2 multi+área 60u 2D 64m² + 60u 3D 85m²); Golden Green Beach (5.1 mono 42u Lote); Cond. Prime Cohama (5.4 sem tipologia 22u "—"). Cobertura 26/46 → 27/44 = 61%.
   - **(6) `pendencias_TOTAL.md` criado** com os 17 empreend. bloqueados na fase Total. Tier 1 (8 com tipologia conhecida — destravam direto via 5.x assim que Total chegar): Dom Antônio, Edifício Dom Ricardo, LIV Residence, Legacy Residence, Ana Vitória, Villa di Carpi, Nexus Renascença, Villagio Treviso. Tier 2 (9 sem tipologia em E_RAW): Connect Península, Mount Solaro, Reserva Península, 3 Canopus Village, Varandas Grand Park, Villa Adagio, Lagoon Residence.
   - **(7) `build_panorama.py` `read_composicao()` atualizado** pra ler schema 11-col e expor `unidades` (= Total tipologia, p/ análise de oferta) e `disponiveis` (= estoque, p/ análise de absorção) — base pra próxima frente: migração das análises do dashboard de "nº empreend." pra "nº unidades" (combinada com Rafael nesta sessão, próximo passo).
   - **PADRAO bumpa v6.1 → v6.2** com §3.7 v2 reescrita: invariante explícita, princípio inviolável (§3.6 vs §3.7 ortogonais, Total é âncora), nova validação C.4, regra D consolidação multi-torre, enum §4.4 ampliado.

- **build_panorama v7.2.0** (03/05/2026) — **Análise por Bairro enxuta — foco em decisão.** Sem mudança de schema/planilha. Layout final: (1) bubble posicionamento (existente, ticket × R$/m²) → (2) **NOVO bubble de oferta** (cada bolha = par bairro × tipologia, X = área média m², Y = unidades disponíveis, cor = bairro top 7 + Outros, tamanho = nº empreendimentos competindo) → (3) tabela resumo (movida pro final). **Removidos:** timeline semestral + 3 heatmaps (Bairro × Incorporadora/Tipologia/Segmento). Função `renderDashHeatmaps` virou stub safe (early-return) caso heatmaps voltem ao DOM. O bubble novo responde diretamente: (a) onde está concentrada cada faixa de tamanho? (Ponta d'Areia 3D ~84m² 117 unid em 4 emp = mercado disputado), (b) quem é mono-oferta? (Araçagi 4D, Cohab Anil IV 2D, São Francisco 2D, Cohama 1D), (c) onde há diversidade? (Calhau cobre 5 tipologias).

- **v10.5** (03/05/2026) — **+3 overrides manuais §3.10** (Rafael 03/05): Al Mare Tirreno (Mota Machado) São Marcos→Calhau · Dom José (DOM) Jardim Eldorado→Turu · Residencial Ana Vitória (Castelucci) Araçagy→Araçagi (normalização ortográfica). Origem Bairro = `informado_manualmente` em todos. §3.10 warnings 41→39 (−2: Dom José já tinha origem `book` na v10.4, agora corrigida pra `informado_manualmente` mas continua fora do warning). Bonus em build_panorama.py: COORDS_BAIRRO ganha alias "Turu"=("Turú") pra geocoding case-sem-acento. Distribuição atualizada: Calhau passou de 4→5 emp.; Araçagi 2→3; Turu 1→2; São Marcos saiu da lista (Al Mare era o único); Jardim Eldorado 3→2.

- **build_panorama v7.1.0** (03/05/2026) — **Reforma da seção "Análise por Bairro" do Dashboard HTML.** Sem mudança de schema/planilha. Mudanças: (1) **removidas** as 2 barras antigas (VGV e R$/m² por bairro — redundantes com a tabela já presente); (2) **adicionado bubble** ticket × R$/m² com cada bolha = 1 bairro, tamanho proporcional a nº empreendimentos (visualização de posicionamento competitivo); (3) **adicionado stacked bar** de lançamentos por semestre × bairro (top 6 + "Outros"), com datas de origem `T-36` em opacidade reduzida + borda tracejada (sinaliza que são estimativas entrega-36m, não datas reais; nota mostra % de T-36 — atualmente 12 de 46 = 26%); (4) **3 heatmaps consolidados** na seção bairro: novo Bairro × Incorporadora + os existentes Bairro × Tipologia e Bairro × Segmento (movidos da seção "Mapas de Calor (cruzamentos)", que foi **removida**). Layout final da seção: tabela → bubble → timeline → 3 heatmaps lado a lado em "Cruzamentos do bairro".

- **v10.4** (03/05/2026) — **+1 bairro manual**: Legacy Residence (Alfa) Ponta d'Areia → Península (informado_manualmente). §3.10 warnings 42→41.

- **v10.3** (03/05/2026) — **Correção manual de bairros (Rafael, 03/05)**: 8 empreend. tiveram bairros normalizados pra "região senso comum" (§3.10): Dom Lucas Cantinho do Céu→Turu; Zion Ponta d'Areia→Península; Golden Green Beach Calhau→Araçagi; Entre Rios Renascença→Renascença II; Studio Design 7 Península, Connect Península, Azimuth, Sky Residence: todos Ponta d'Areia→Península. Origem Bairro = `informado_manualmente` em todos. §3.10 warnings 49→42 (7 a menos). Aplicação direta da hierarquia §3.10 nível 5 (Rafael forneceu manualmente). 

- **v10.2** (03/05/2026) — **Lote 5 Composição entregue (DOM via visão multimodal) + enriquecimento Dom Ricardo**. Rafael colocou no INBOX 03/05 os books DOM (Dom Ricardo + Dom José) + tabela Dom José ABR/2026 + xlsx interno Dom Ricardo. Processadas 4 fontes: (1) Book Dom Ricardo (texto OK) → enriquecimento de tipologia (3 colunas: 2× 3D 85m² + 1× 2D 71,92m²), bairro Renascença II (book diz "Pracinha da Lagoa" microregião), parceria DOM+MB Engenharia, memorial R.14/28.859, entrega DEZ/2026; xlsx interno mostra 19 contratos VENDIDOS (DR101-DR901, ticket R$ 690k-1.194k). (2) Book Dom José + (3) Tabela Dom José ABR/2026 (PDFs imagem → pdftoppm + visão Claude): TOTAL = 22 (implantação numerada 01-22), 3 disp + 19 vend = 86% vendido, tickets R$ 1.403k-1.420k, mês entrega 06/2027 → 07/2027 (correção pela tabela). (4) Tabela Dom Lucas ABR/2026 (PDF imagem → visão): TOTAL = 46 (UH 1-46), 9 disp + 1 res + 36 vend = 80% vendido, tickets R$ 835.894-850.937, mês entrega 01/2029 → 12/2028 (correção). +2 entries em C_RAW (Lote 5: Dom Lucas 3D 9 unid + Dom José 4D 3 unid, ambas `tabela_local_imagem`). Cobertura Composição: 50% → 54% (25/46 empreend.). VGV mapeado: R$ 2,40 bi → R$ 2,48 bi. §3.7.C.3 cobertura zerada para Dom Lucas e Dom José. Origem Bairro preenchida nos 3 (book). 

- **v10.1** (02/05/2026) — **Lote 4 Composição entregue + 3 inconsistências corrigidas**. +4 entries de Composição (não-DOM, tabelas texto): Monte Meru (Berg, 2 unid 3D), Residencial Novo Anil (Monteplan, 30 unid 2D), Giardino Fiore (Alfa, 6 unid 3D), Giardino Luce (Alfa, 5 unid 3D). 3 parsers novos no catálogo §3.7.1 (Alfa, Berg, Monteplan-Anil). Inconsistências §3.7.C.2 zeradas: Azimuth, Quartier 22, Entre Rios passaram de 4D→3D (declaração mono-tipologia prevalece sobre heurística por área). Cobertura Composição: 41% → 50% (23/46 empreend.). Restam 2 empreend. com tabela mas sem C_RAW (Dom Lucas, Dom José — aguardando info no INBOX). PADRAO bumpa v6.0→v6.1.
- **v10.0** (02/05/2026) — **MUDANÇA ESTRUTURAL: PADRAO §3.10 (Bairro/Região)**. Schema 26→27 col (+Origem Bairro). Bairro agora tem semântica explícita: REGIÃO SENSO COMUM (do book/marketing), não oficial do CEP. Hierarquia 6 níveis (`book`→`site_oficial`→`imprensa`→`treinamento_corretor`→`informado_manualmente`→`endereco_oficial`→`N/A`). Validação automática (Origem Bairro=None ou Bairro genérico → WARN). Memória `feedback_bairro_regiao_processo.md`. PADRAO bumpa v5.4 → v6.0. **Os 5 dados centrais do estudo (Total, Composição, % Vendido, Mês Lançamento, Bairro/Região) agora têm processo formal completo.**
- **v9.5** (02/05/2026) — **FORMALIZAÇÃO DO 4º PROCESSO: Mês de Lançamento** (PADRAO §3.9). Hierarquia 8 níveis (`imprensa` → `tabela_local` → `book` → `site_oficial` → `instagram_oficial` → `treinamento_corretor` → `informado_manualmente` → `estimativa_T-36` → `N/A`). Regra T-36 (§3.5) preservada. Validação automática: `estimativa_T-36` há > 180 dias → WARN. Memória `feedback_mes_lancamento_processo.md`. PADRAO bumpa v5.3 → v5.4. **Os 4 dados centrais do estudo (Total + Composição + % Vendido + Mês Lançamento) agora têm processo formal completo.**
- **v9.4** (02/05/2026) — **FORMALIZAÇÃO DO PROCESSO DE % VENDIDO** (PADRAO §3.8). Cálculo automático no script: `estoque = disponíveis/total`. Schema E_RAW 25→26 col (nova "Origem % Vendido"). 5 origens: `calculado_automatico`/`informado_manualmente`/`tabela_local_completa_zero`/`nao_determinavel` (Niágara)/`N/A` (lista de busca). Validação automática 5% manual vs calc. **2 bugs corrigidos pela validação na 1ª execução:** Zion (estoque 0.83→0.17) e Vernazza Norte (0.47→0.31). Em seguida (mesma sessão): **reset completo de TODOS os manuais** (3 explícitos + 11 expressões aritméticas) — % Vendido agora é 100% calculado pela fórmula §3.8. Tooltip da Tabela A no Panorama também atualizado pra referenciar §3.8 (era §3.3 antiga) — convenção invertida (E_RAW armazena estoque, não % vendido). PADRAO bumpa v5.2→v5.3. **Cobertura final v9.4 (após reset total): 16 calculados | 0 manuais | 1 zero | 1 não-det | 28 N/A** (lista automática de busca pra obter info).
- **v9.3** (02/05/2026) — **FORMALIZAÇÃO DO PROCESSO DE COMPOSIÇÃO** (PADRAO §3.7). 5 níveis de fonte (`tabela_local` → `tabela_local_imagem` → `book` → `informado_manualmente` → não preencher). Catálogo de 8 parsers por incorporadora (Delman, Mota Machado, Treviso N/V, Treviso Altos, Monteplan, Castelucci, Niágara, Hiali). 3 validações automáticas no script: anti-duplicação, heurística-vs-Tipologia-declarada, cobertura (tabela arquivada sem C_RAW). 1ª execução detectou 9 alertas (3 inconsistências mono-tipologia E_RAW vs heurística C_RAW + 6 empreend. com tabela arquivada mas sem C_RAW — entram no roadmap futuro). Memória `feedback_composicao_processo.md` registrada. PADRAO bumpa v5.1→v5.2.
- **v9.2** (02/05/2026) — **FORMALIZAÇÃO DO PROCESSO** de Total de Unidades como PADRAO §3.6 (7 níveis hierárquicos), enum §4.7 atualizado (removido `estimativa`, adicionado `informado_manualmente`), validação automática 5% no script, memória persistente nova (`feedback_total_unidades_processo.md`). Al Mare e Sanpaolo voltaram pra `None`/`N/A`. Validação pegou bug real: Renaissance Conceito C_RAW duplicado (parser SFH+FDC) — corrigido 44→22 unid, origem `tabela_local_completa`→`tabela_local_parcial`. PADRAO bumpa v5.0→v5.1.
- **v9.1** (02/05/2026) — **Aplicação do padrão de Total Unidades** (hierarquia Rafael 02/05). The View 192 (descrição), Vernazza Sul 60 (cross-check Norte memorial), ORO 96 (`tabela_local_completa`), Reserva SM 90 (numeração), Entre Rios 30 (`tabela_local_completa`), Al Mare 45 (estimativa), Vila Coimbra 41 (`book` confirmado pelo Rafael), Sanpaolo 64 (estimativa). +4 inconsistências de origem corrigidas (Ilha Parque, 2 Giardinos, Cond. Prime Cohama). +Golden Green Beach 42 (book). Cobertura: total 16→25 (54%), origem 20→25 (54%). VGV mapeado: R$ 1,59 bi → **R$ 2,59 bi** (mais empreend. com VGV calculável).
- **v9.0** (02/05/2026) — **MUDANÇA ESTRUTURAL: nova coluna 8 "Origem total unid."** no schema da aba Empreendimentos (24 → 25 col). Enum §4.7 com 9 valores (`tabela_local_completa`/`tabela_local_parcial`/`book`/`memorial`/etc). Validação automática: alerta se origem = completa mas soma C_RAW != total. Tabela A do Panorama ganha coluna "Total Unid." entre Tipologia e Área méd, com tooltip de origem + vendidas inferidas. PADRAO bumpa 4.0 → 5.0. Total Zion confirmado pelo Rafael via book = 60 unid. 20 entries com Composição preenchidas com origem do total.

---

## Roadmap próximos lotes

### Lote 3+5 — visão multimodal (CONCLUÍDO ✅)

PDFs de tabela em formato imagem (não extraível por pdftotext). Estratégia: converter páginas em PNG e usar visão multimodal de Claude para ler.

| Empreend. | Inc. | Status |
|---|---|---|
| Dom Lucas | DOM Incorporação | ✅ v10.2 (46 unid total, 9 disp) |
| Dom José | DOM Incorporação | ✅ v10.2 (22 unid total, 3 disp) |
| Zion Ponta d'Areia | Ergus | ✅ v8.2 (10 unid disponíveis) |

**Cobertura atual:** 25/46 = 54%.

### Empreend. ainda sem tabela arquivada (~20 empreend.)

Restante depende de captura de tabela junto às incorporadoras (corretor / site / book). São incorporadoras menos ativas no monitoramento atual.

---

## Bugs latentes / pendências

### 🟡 Lote 3 da composição — aguarda comando
Visão multimodal Claude.

### 🟡 % Vendido por tipologia
Composição hoje só tem **# unidades disponíveis** por tipologia. Para calcular % vendido por tipologia, precisamos do **total original** por tipologia (memorial de incorporação ou book). Roadmap: Lote 4.

---

## Armadilhas comuns (lições aprendidas)

1. Glob recursivo amplo trunca silenciosamente — usar `sort -V | tail -N`.
2. Filtros por prefixo de nome são frágeis (cuidado com footer "DOM Incorporação ●").
3. `v4.5` aparece depois de `v4.16` em ordem lexicográfica — sempre `sort -V`.
4. NFD vs NFC em paths macOS — `pathlib.Path(__file__).resolve()` herda forma correta.
5. Bossa e The View são vizinhos (Quadra 02, Av. dos Holandeses, Calhau).
6. Tabelas em PDF imagem (Zion, Dom Lucas/José) — Lote 3.
7. `p.write_text` precisa ser explícito.
8. F-string com backslash escape causa SyntaxError no Python.
9. Substituição de blocos grandes de JS exige reverificação das chamadas de inicialização.
10. **Heurística tipologia × área é pragmática:** 80m² na fronteira 2D-3D pode classificar errado. Mono-tipologia declarada do empreendimento prevalece quando explícita.
11. **Parser Sanpaolo duplicava entries** (par de unidades unidas L-L) — necessário inspeção pós-extração para entries com múltiplos aptos numa linha só.

---

## O que mantém este arquivo atualizado

`publish.sh` (idealmente) deve regenerar este arquivo em cada rodada — ainda não implementado. Por enquanto, **toda vez que VERSION ou schema mudar, atualizar manualmente**.
