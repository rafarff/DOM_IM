# Pendências de TOTAL — Empreendimentos sem Total apurado

> Criado em **03/05/2026** com a planilha **v10.6** e o **PADRAO v6.2**.
> Documento gerencial: lista os empreendimentos da carteira que **ainda não têm Total apurado** via §3.6 (hierarquia de 7 níveis: memorial → book → tabela_completa → tabela_parcial → numeração → imagens → manual → N/A).
> Sem Total apurado, **§3.7 não pode ser aplicado** (nem fontes fortes níveis 1–4, nem estimativa nível 5). Esses empreendimentos ficam fora das análises por unidades até que o Total seja apurado.

## Como destravar

Para cada empreendimento abaixo, seguir a hierarquia §3.6:

1. **Memorial de incorporação** (mais forte) — buscar em registro de imóveis ou pedir ao corretor.
2. **Book oficial** com tabela ou implantação numerada — site, corretor, redes sociais.
3. **Tabela ABR/2026** ou outra com listagem completa de unidades — corretor, agregador, parceria.
4. **Imagens de implantação** com numeração (UH 01–NN) — book ou redes.
5. **Treinamento de corretor** — ele declara o total durante apresentação.
6. **Informado manualmente** (Rafael) — se já souber.
7. **N/A** — apenas se nada das opções acima é viável (raro).

Após apurar, atualizar a tupla em `gerar_planilha.py` (col 7 do E_RAW) com:
- `Total` (int)
- `Origem total unid.` (col 24, valor do enum §4.7)
- Observações registrando fonte, data, link

A invariante v6.2 (Σ Composição = Total) destrava automaticamente: se já existir C_RAW para o empreend., o script reconcilia via §3.7.C.4; se não, o nível 5 estimativa é aplicado conforme árvore §3.7.A.1.

---

## Lista priorizada (17 empreendimentos)

### Tier 1 — Tipologia conhecida em E_RAW (mais fácil — só falta o Total)

Esses caem direto em §3.7 nível 5 sub-regra 5.1, 5.2 ou 5.3 assim que Total chegar. Priorizar.

| # | Incorporadora | Empreend. | Tipologia E_RAW | Bairro | Sub-regra após Total |
|---|---|---|---|---|---|
| 1 | DOM Incorporação | Dom Antônio | 3D | Jardim Eldorado | 5.1 (mono) |
| 2 | DOM Incorporação | Edifício Dom Ricardo | 2D; 3D | Renascença II | 5.2/5.3 (multi) |
| 3 | Alfa Engenharia | LIV Residence | 3D | Ponta d'Areia | 5.1 (mono) |
| 4 | Alfa Engenharia | Legacy Residence | 4D | Península | 5.1 (mono) |
| 5 | Castelucci | Residencial Ana Vitória | 2D; 3D | Araçagi | 5.2/5.3 (multi) |
| 6 | Castelucci | Villa di Carpi | 2D | Cohatrac | 5.1 (mono) |
| 7 | Ergus | Nexus Renascença | Studio; 1D; 2D | Renascença | 5.2/5.3 (multi) |
| 8 | Treviso | Villagio Treviso | Lote | São Luís (genérico) | 5.1 (loteamento) |

### Tier 2 — Sem tipologia em E_RAW (precisa de mais info — Total + Tipologia)

Esses caem em sub-regra 5.4 (sem tipologia) se chegar só Total, ou direto em fonte forte se chegar tabela completa.

| # | Incorporadora | Empreend. | Bairro |
|---|---|---|---|
| 9 | Alfa Engenharia | Connect Península | Península |
| 10 | Berg Engenharia | Mount Solaro | São Luís (genérico) |
| 11 | Canopus | Village Reserva II | São Luís (genérico) |
| 12 | Canopus | Village Prime Eldorado | Jardim Eldorado |
| 13 | Canopus | Village Del Ville II | São Luís (genérico) |
| 14 | Sá Cavalcante | Reserva Península | Ponta d'Areia |
| 15 | Franere | Varandas Grand Park | São Luís (genérico) |
| 16 | Lua Nova | Villa Adagio | São Luís (genérico) |
| 17 | Lua Nova | Lagoon Residence | Santo Amaro |

---

## Status

**Total da carteira:** 44 empreendimentos
**Com Total apurado:** 27 (61%)
**Bloqueados aqui:** 17 (39%)

**Cobertura §3.7 atual (v10.6):**
- 26 fontes fortes (níveis 1–4, mantidas após consolidação multi-torre)
- 3 estimativas nível 5 aplicadas automaticamente (Ilha Parque, Golden Green Beach, Cond. Prime Cohama)
- 17 bloqueados (esta lista)

À medida que os 17 caem da fila, a estimativa nível 5 ou a fonte forte é aplicada automaticamente pelo script — sem intervenção manual no §3.7.

---

## Observação importante (PADRAO v6.2)

> §3.6 (Total) e §3.7 (Composição) são processos ortogonais. **Total é a âncora.** Composição se conforma ao Total, nunca o contrário. Não criar estimativas de Total a partir de Composição. Se faltar Total, o empreend. fica nesta lista até que uma fonte real seja consultada.
