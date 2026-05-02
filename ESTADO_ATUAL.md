# ESTADO ATUAL — Inteligência de Mercado DOM

> **Para Claude (toda sessão):** este é o **primeiro arquivo a ler** antes de qualquer ação. Confirma a base de trabalho. Se a invariante 0.3 do PADRAO falhar contra os números aqui, **PARAR**.

**Última atualização:** 02/05/2026
**Versão Planilha vigente:** v8.0
**Versão PADRAO vigente:** v4.0
**Versão script `gerar_planilha.py`:** 8.0 (DATE_STR: 02/05/2026)

---

## Snapshot da carteira

| Métrica | Valor |
|---|---:|
| Aba Empreendimentos | **46 linhas** (sem mudança) |
| Aba Incorporadoras | **16 linhas** |
| Aba Composição (NOVA, v8.0) | **15 linhas / 322 unidades** |
| Drift script ↔ planilha | **0** ✅ |
| VGV total mapeado | **R$ 1,45 bi** |
| Empreend. com R$/m² calculável | 27/46 |

### Distribuição por incorporadora (v8.0, aba Empreendimentos)

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

### Cobertura da Aba Composição (v8.0)

| Empreendimento | Tipologias | Unidades |
|---|---|---:|
| The View (Delman) | Studio, 1D, 2D, 3D | 93 |
| Landscape (Delman) | 3D, 4D | 51 |
| Studio Design 7 Pen. (Delman) | 1D, 2D, 3D | 31 |
| Wave Residence (Delman) | 4D | 5 |
| Edifício Bossa (Mota Machado) | 4D | 36 |
| Altos São Francisco (Treviso) | 2D | 26 |
| Renaissance Conceito (Monteplan) | 3D, 4D | 44 |
| Vila Coimbra (Castelucci) | 4D | 36 |
| **Total Lote 1** | | **322** |

**Empreend. ainda sem entry em Composição:** 38 (cobertura atual: 8/46 = 17%).

---

## Comando one-liner (versão vigente)

```bash
cd 00_ESTUDO_CONSOLIDADO/ && ls -1 Planilha_Mestre_Panorama_v*.xlsx | sort -V | tail -1
```

---

## Mudanças estruturais recentes

- **v6.0–v6.6** — limpezas de schema, redesign HTML, fixes.
- **v7.0** (02/05/2026) — Dashboard redesenhado em 6 seções + filtros globais.
- **v7.0.1** (02/05/2026) — Fix init Panorama.
- **v8.0** (02/05/2026) — **MUDANÇA ESTRUTURAL: nova aba "Composição" na .xlsx** (1 linha por empreend × tipologia, 10 colunas). Lote 1 entregue (8 empreend., 322 unidades). Build_panorama lê 2 abas; Seção 3 do dashboard usa dados precisos. PADRAO bumpado v3.5 → v4.0 com §2.1 nova.

---

## Roadmap dos próximos lotes

### Lote 2 — empreend. com tabela texto extraível (~10 empreend.)

| Empreend. | Inc. | Status |
|---|---|---|
| Vernazza Norte e Sul | Treviso | Texto OK, formato AGR |
| Quartier 22 | Delman | Texto OK |
| Sky Residence | Delman | Texto OK |
| Azimuth | Delman | Texto OK |
| Al Mare Tirreno | Mota Machado | Texto OK |
| Le Noir | Hiali | Parser parcial (PAR) |
| ORO Ponta d'Areia | Niágara | Texto OK |
| Edifício Sanpaolo | Monteplan | Texto OK (1 unid livre) |
| Reserva São Marcos | Mota Machado | Texto OK (sem áreas inline) |
| Entre Rios | Mota Machado | Texto OK |
| Vernazza Torre Norte/Sul | Treviso | Texto OK |

### Lote 3 — visão multimodal (PDFs imagem)

- **Dom Lucas, Dom José** (DOM Incorporação) — tabelas em imagem
- **Zion Ponta d'Areia** (Ergus, item D pendente) — tabelas em imagem

Estratégia: converter páginas em PNG e usar visão multimodal de Claude para ler. Comando do Rafael necessário pra atacar.

---

## Bugs latentes / pendências

### 🟡 Lote 2 e 3 da composição — incompletos
Cobertura atual 17%. Aumentar via processamento das tabelas restantes.

---

## Armadilhas comuns (lições aprendidas)

1. Glob recursivo amplo trunca silenciosamente — usar `sort -V | tail -N`.
2. Filtros por prefixo de nome são frágeis (cuidado com footer "DOM Incorporação ●").
3. `v4.5` aparece depois de `v4.16` em ordem lexicográfica — sempre `sort -V`.
4. NFD vs NFC em paths macOS — `pathlib.Path(__file__).resolve()` herda forma correta.
5. Bossa e The View são vizinhos (Quadra 02, Av. dos Holandeses, Calhau).
6. Tabelas em PDF imagem (Zion, Dom Lucas/José) não dão extração via pdftotext — Lote 3.
7. `p.write_text` precisa ser explícito.
8. **F-string com backslash escape causa SyntaxError no Python** — não usar `f"...{x \"y\"...}"`. Usar variável intermediária ou aspas simples.
9. **Substituição de blocos grandes de JS exige reverificação das chamadas de inicialização** (caso v7.0.1).

---

## O que mantém este arquivo atualizado

`publish.sh` (idealmente) deve regenerar este arquivo em cada rodada — ainda não implementado. Por enquanto, **toda vez que VERSION ou schema mudar, atualizar manualmente**.
