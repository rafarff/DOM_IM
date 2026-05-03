# ESTADO ATUAL — Inteligência de Mercado DOM

> **Para Claude (toda sessão):** este é o **primeiro arquivo a ler** antes de qualquer ação. Confirma a base de trabalho. Se a invariante 0.3 do PADRAO falhar contra os números aqui, **PARAR**.

**Última atualização:** 03/05/2026
**Versão Planilha vigente:** v10.2
**Versão PADRAO vigente:** v6.1
**Versão script `gerar_planilha.py`:** 10.2 (DATE_STR: 03/05/2026)

---

## Snapshot da carteira

| Métrica | Valor |
|---|---:|
| Aba Empreendimentos | **46 linhas** |
| Aba Incorporadoras | **16 linhas** |
| Aba Composição | **36 linhas / 570 unidades**
| Aba Empreendimentos schema | **27 colunas (v10.0)** ← +Origem total (v9.0) + Origem % Vendido (v9.4) + Origem Bairro (v10.0) | ✅ Lote 1+2 |
| Drift script ↔ planilha | **0** ✅ |
| VGV total mapeado | **R$ 2,48 bi** |
| Cobertura Composição | **25/46 empreend. = 54%** |

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
