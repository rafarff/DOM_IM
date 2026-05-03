# Pendências de TOTAL — Empreendimentos sem Total apurado

> Atualizado em **03/05/2026** com a planilha **v10.9** e o **PADRAO v6.2**.
> Documento gerencial: lista os empreendimentos da carteira que **ainda não têm Total apurado** via §3.6 (hierarquia de 7 níveis).

## Status

**Total da carteira:** 44 empreendimentos
**Com Total apurado:** 34 (77%) — destravam Composição automaticamente
**Bloqueados aqui:** 10 (23%)

**Histórico desta lista:**
- v10.6: 17 bloqueados
- v10.7: 15 (Dom Antônio + Dom Ricardo destravados pelo Rafael)
- v10.8: 11 (LIV, Ana Vitória, Mount Solaro, Village Prime Eldorado destravados via web research)
- **v10.9: 10** (Legacy Residence destravado por Rafael — 30u 4D 175/185m²)

---

## Lista priorizada (10 empreendimentos restantes)

### Tier A — Pacotes que destravam vários de uma vez (pesquisa concentrada)

#### A1. Pacote Canopus (2 restantes)
Os 3 lançamentos Canopus 31/10/2025 totalizam **1.487 unidades / R$ 300M VGV** (Imirante). Sabemos: Village Prime Eldorado = 400 unid. Restam 1.087 entre Reserva II e Del Ville II. **Atalho:** 1 contato com comercial Canopus → 2 destravados.

| # | Empreend. | Bairro | Tipologia (já mapeada) | Área | Falta |
|---|---|---|---|---|---|
| 1 | **Village Reserva II** | Cohatrac | 2D | 41m² | Total |
| 2 | **Village Del Ville II** | Iguaíba | 2D | 42-43m² | Total |

#### A2. Alfa Engenharia — Connect Península (1 restante)
Legacy Residence destravado pelo Rafael na v10.9 (30u 4D 175m² + 185m²). Resta Connect Península, que precisa de book/site Alfa.

| # | Empreend. | Bairro | Tipologia | Área | Falta |
|---|---|---|---|---|---|
| 3 | **Connect Península** | Península | a confirmar (perfil Housi → Studio/1D) | a confirmar | Total + tipologia |

### Tier B — Empreendimentos individuais (cada um 1 contato)

| # | Empreend. | Inc. | Bairro | Tipologia | Área | Próxima ação |
|---|---|---|---|---|---|---|
| 4 | **Reserva Península** | Sá Cavalcante | Península | 4D mono | 127-171m² | Pedir book (lançamento 09/2025, evento 'Casa Sal') |
| 5 | **Nexus Renascença** | Ergus | Renascença | Studio;1D;2D | 33-94m² | Imprensa Diego Emir / site Ergus |
| 6 | **Villagio Treviso** | Treviso | a confirmar | Lote (loteamento) | terreno | Site Treviso ou contato comercial |
| 7 | **Villa di Carpi** | Castelucci | Cohatrac | 2D mono (3 plantas) | 49,36-51,88m² | Site meuvilladicarpi.com.br ou Ziag |
| 8 | **Varandas Grand Park** | Franere | Calhau | 3D mono | 74-87m² | Pronto pra entrega — ofício direto à Franere/Gafisa |
| 9 | **Villa Adagio** | Lua Nova | Iguaíba | 2D mono | 48,90m² | Site Lua Nova / IG / vídeo Sinduscon |

### Tier C — Fora do escopo (decidir antes de pesquisar)

| # | Empreend. | Inc. | Status | Decisão pendente |
|---|---|---|---|---|
| 10 | **Lagoon Residence** | Lua Nova | **Santo Amaro do Maranhão** (cidade satélite, ~250km de SLZ — porta dos Lençóis) | ⚠ **Manter na carteira ou tirar?** Não é Grande SLZ. |

---

## Como destravar

Para cada empreendimento, seguir a hierarquia §3.6:
1. **Memorial de incorporação** (mais forte) — registro de imóveis
2. **Book oficial** com tabela ou implantação numerada — site, corretor
3. **Tabela ABR/2026** ou outra com listagem completa — corretor, agregador
4. **Imagens de implantação** com numeração — book ou redes
5. **Treinamento de corretor**
6. **Informado manualmente** (Rafael)
7. **N/A** — apenas se nada das opções acima é viável (raro)

Após apurar, atualizar a tupla em `gerar_planilha.py` (col 7 do E_RAW). A invariante v6.2 destrava automaticamente: Composição é gerada via §3.7 nível 5 (estimativa) ou recebe fonte forte (1-4) conforme o que estiver disponível.

---

## Achados v10.8 que ainda precisam de validação Rafael

1. **Lagoon Residence (Tier C)** — fora do escopo geográfico, decidir manter ou tirar
2. **Village Prime Eldorado bairro** — endereço CEP "Vila Vicente Fialho", mas marca/posicionamento Canopus = "Eldorado". Mantive `Jardim Eldorado` por origem `imprensa` (Imirante) — confirmar?
3. **Mount Solaro entries C_RAW** — agreguei 20u 68m² + 10u 72m² em uma única entry "2D" (30u 68-72m²) por simplicidade. Pode-se desagregar em 2 entries 2D distintas se preferir granularidade fina.
4. **Residencial Ana Vitória "Entregue"** — marquei como `Entregue` pelo lançamento de 01/2018, mas vale confirmar se ainda está em comercialização (ticket parte de R$ 557k indica que sim).
