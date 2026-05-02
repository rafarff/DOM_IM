# ESTADO ATUAL — Inteligência de Mercado DOM

> **Para Claude (toda sessão):** este é o **primeiro arquivo a ler** antes de qualquer ação. Confirma a base de trabalho. Se a invariante 0.3 do PADRAO falhar contra os números aqui, **PARAR**.

**Última atualização:** 02/05/2026
**Versão Planilha vigente:** v7.0.1
**Versão PADRAO vigente:** v3.5
**Versão script `gerar_planilha.py`:** 7.0.1 (DATE_STR: 02/05/2026)

---

## Snapshot da carteira

| Métrica | Valor |
|---|---:|
| Total de empreendimentos no E_RAW | **46** |
| Total de empreendimentos na v7.0.1.xlsx | **46** |
| Drift script ↔ planilha | **0** ✅ |
| Incorporadoras monitoradas (lista fechada) | **16** |
| Schema aba Empreendimentos | **24 colunas** (sem mudança desde v6.0) |
| Schema aba Incorporadoras | **15 colunas** |
| VGV total mapeado | **R$ 1,45 bi** |
| Preço calculável | 27/46 |

### Distribuição por incorporadora (v7.0)

| Incorporadora | # Empreend. |
|---|---:|
| Delman | 7 |
| Alfa Engenharia | 5 |
| Mota Machado | 4 |
| DOM Incorporação | 4 |
| Treviso | 4 |
| Lua Nova | 3 |
| Castelucci | 3 |
| Canopus | 3 |
| Monteplan | 3 |
| Berg Engenharia | 2 |
| Ergus | 2 |
| Sá Cavalcante | 2 |
| MB Engenharia | 1 |
| Niágara | 1 |
| Hiali | 1 |
| Franere | 1 |

---

## Comando one-liner (versão vigente)

```bash
cd 00_ESTUDO_CONSOLIDADO/ && ls -1 Planilha_Mestre_Panorama_v*.xlsx | sort -V | tail -1
```

---

## Mudanças estruturais recentes

- **v6.0–v6.5** (27-28/04/2026) — limpezas de schema, fixes estruturais, PADRAO §0.4/§0.5.
- **v6.6** (29/04/2026) — UI: logo 90px + col % Vendido com tooltip. Dados: 3 dos 4 gaps preenchidos (Renaissance, Sanpaolo, Reserva SM). Zion pendente.
- **v7.0.1** (02/05/2026) — FIX: restaurada inicialização da aba Panorama (KPIs e tabelas A/B estavam vazios na v7.0 — substituição do JS removeu chamadas `populateFilters/buildLegend/applyFilters` por engano).
- **v7.0** (02/05/2026) — **MUDANÇA ESTRUTURAL: aba Dashboard do HTML completamente redesenhada.** 6 seções (KPIs, Bairro, Tipologia, Incorporadora, Segmento, Heatmaps) + filtros globais (default últimos 24 meses). Inspirado no estudo BRAIN/Piacentini (em `_REFERENCIAS_EXTERNAS/`). Schema da .xlsx **não mudou** — v7.0 é redesenho do HTML, dados idênticos à v6.6.

---

## Pasta de referências externas (nova em v7.0)

`/_REFERENCIAS_EXTERNAS/` — guarda estudos e materiais que não pertencem às 16 incorporadoras monitoradas, mas servem como referência metodológica:
- `Estudo_BRAIN_Piacentini_Curitiba_2020.pdf` — base do redesenho do dashboard.

Distinto do `_INBOX/` (entrada de material das concorrentes).

---

## Bugs latentes / pendências

### 🟡 Zion Ponta d'Areia (Ergus) — tabela em imagem
9 PDFs, todos baseados em imagem. OCR ilegível.
**Próximas ações (em ordem de custo):**
1. Pedir ao corretor da Ergus tabela em formato texto/Excel
2. OCR mais robusto (Google Vision, Adobe)
3. Manual: ler em PDF e digitar (~10 min)

### 🟡 13 empreend. com gap só de % Vendido
Têm tickets/áreas, faltam contar unidades disponíveis em tabelas já arquivadas.

### 🟡 Roadmap de enriquecimento (v7.x – v8.0): breakdown de unidades por tipologia
**Hoje:** o E_RAW tem total agregado de unidades por empreend., sem distribuição por tipologia. Para empreend. mono-tipologia (ex: Bossa = 60 unid 4D), o dado é bom. Para multi-tipologia (ex: The View = Studio+1D+2D+3D), não sabemos quantas de cada.

**Impacto:** colunas "Unid. mono" e "% Abs. mono" da Seção 3 (Tipologia) do dashboard agregam só os mono-tipologia, com nota explicativa.

**Solução:** abrir as 26 tabelas arquivadas e contar linha-a-linha. A maioria das tabelas (The View, Renaissance, Bossa) já tem o detalhe linha-a-linha visível em `pdftotext`. É trabalho braçal mas direto.

**Quando fazer:** próxima rodada de enriquecimento. Pode evoluir o schema do E_RAW pra incluir uma coluna nova "Distribuição tipologias" (ex: `Studio:32; 1D:48; 2D:80; 3D:22`).

### 🟢 Lançamentos DOM em estudo (Fase 2 do dashboard)
Rafael vai preparar essa info em paralelo. Quando ele tiver hipóteses (terreno + produto candidato), virá a "Aba de Análise Específica" — comparação dirigida entre o produto DOM hipotético e a concorrência.

---

## Armadilhas comuns (lições aprendidas)

1. Glob recursivo amplo trunca silenciosamente — usar `sort -V | tail -N`.
2. Filtros por prefixo de nome são frágeis (cuidado com footer "DOM Incorporação ●").
3. `v4.5` aparece depois de `v4.16` em ordem lexicográfica — sempre `sort -V`.
4. NFD vs NFC em paths macOS — `pathlib.Path(__file__).resolve()` herda forma correta.
5. Bossa e The View são vizinhos (Quadra 02, Av. dos Holandeses, Calhau).
6. Tabelas em PDF imagem (Zion) não são triviais — precisa OCR robusto ou solicitação ao corretor.
7. `p.write_text` precisa ser explícito.
8. **Multi-tipologia em "Studio; 2D; 3D"** — não temos breakdown por tipologia, então agregações de unidades/absorção por tipologia usam apenas mono-tipologia (com nota no UI).

---

## O que mantém este arquivo atualizado

`publish.sh` (idealmente) deve regenerar este arquivo em cada rodada — ainda não implementado. Por enquanto, **toda vez que VERSION ou schema mudar, atualizar manualmente**.
