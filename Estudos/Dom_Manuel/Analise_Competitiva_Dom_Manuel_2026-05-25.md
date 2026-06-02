# Análise Competitiva — Lançamento Condomínio Dom Manuel

**Comando:** §5.2 `analisa` — análise focada
**Data:** 25/05/2026 · **rev. 5** — correção tipologia Renaissance Conceito (02/06/2026)
**Base IM vigente:** Planilha Mestre Panorama **v11.25** · U_RAW (28 YAMLs / 1.073 unidades) · Composição (109 linhas) · PADRAO v7.0

> **O que mudou da rev.4 para a rev.5** (Planilha v11.25, site Monteplan)
> 1. **Renaissance Conceito — Torre Leonardo da Vinci reclassificada de 4D para 3D** (110 m², 3 suítes + lavabo), confirmado pelo site oficial Monteplan. O empreendimento é **100% 3D** (Botticelli 82 m² 3D + Leonardo 110 m² 3D); não existe 4 dormitórios.
> 2. **Consequência analítica:** Renaissance deixa de figurar entre os concorrentes **4D** do DM Tipo 01. O Leonardo (110 m², 3 suítes) passa a ser comparável direto do DM **Tipo 02** (3D 116 m², 3 suítes) — e por R$/m² (~13.168) é o concorrente **mais barato** de toda a referência 3D. Com isso, o **único 4D fora da Ponta d'Areia** (Tier 2) passa a ser a Reserva SM Litorânea.
> 3. Tabelas §1.1/§1.2 e gráficos B.2/B.4 + escada T01 atualizados. Sem mudança de preço/VGV do Dom Manuel.
> 4. Causa raiz: heurística de área §3.7 (110 m²>95→4D) no U_RAW — 3º caso após Landscape e Giardino Fiore Col 03.
>
> **O que mudou da rev.3 para a rev.4** (Planilha v11.24, book Alfa)
> 1. **Giardino Torre Fiore — Coluna 01 (127,30 m²) e Coluna 02 (128,37 m²) reclassificadas de 3D para 4D** (2 suítes + 2 semissuítes + dependência + 3 vagas), confirmado pelo book Alfa. Coluna 03 (110,77 m²) e toda a Torre Luce permanecem 3D (3 suítes).
> 2. **Consequência analítica:** o Giardino passa a ser um **comparável 4D direto** do Dom Manuel Tipo 01 — antes era lido como 3D-grande. Isso **reforça** a tese do nicho 3D-grande não disputado (§3): o que parecia uma 3D de 127 m² na Ponta do Farol some do mapa de concorrência da 3D-116 do Dom Manuel.
> 3. Tabelas §1.1 e §1.2 e leitura por ticket §2.1 atualizadas. Sem mudança de preço/VGV do Dom Manuel.
>
> **O que mudou da rev.2 para a rev.3**
> 1. **Modelo de preço corrigido** (kickoff item 3): R$ 13.400/m² é a **média ponderada** da T0 (não o piso do 1º andar); curva de andar **centrada no 8º andar**; escada T0→T4 **+2,0% simples**; VGV T0 = **R$ 77.533.740**.
> 2. **§2.2 — o "+R$ 2,7 M" da rev.2 caiu.** A curva centrada é VGV-neutra; mudar a inclinação redistribui valor entre andares, não cria VGV.
> 3. **§2.4 — o alarme de "zona morta" da rev.2 estava superdimensionado.** Com a escada correta, o teto da tabela é R$ 14.979/m².
> 4. **Conjunto competitivo** reorganizado nos **4 rótulos** do piloto (direta / indireta / referência-teto / referência de produto).
> 5. Base corrigida: entry Dom Manuel atualizada e bug do Renaissance saneado (Planilha v11.21 — ver §4.3).

---

## 0. Objeto da análise — Condomínio Dom Manuel

| Parâmetro | Valor |
|---|---|
| Tipo / local | Vertical · **Ponta D'Areia** · São Luís/MA |
| Porte | 45 unidades · 15 pavimentos-tipo · 3 aptos/andar |
| **Tipo 01** | 134,68 m² · 4 quartos (3 suítes) · **30 unidades** (finais 01 e 03) |
| **Tipo 02** | 116,38 m² · 3 quartos (3 suítes) · **15 unidades** (final 02) |
| Cronograma | lançamento **jun/2026** · entrega **nov/2029** |

### Modelo de preço (tabela de pré-lançamento)

- **R$ 13.400/m² = média ponderada** do preço total (apartamento + vagas) ÷ área privativa, sobre as 45 unidades, na tabela **T0**. É o número-âncora — não é o preço do 1º andar.
- **Curva de andar centrada no 8º andar:** multiplicador `1 + (andar − 8) × 0,5%`. Andar 1 = 0,965 (−3,5% vs média) · andar 8 = 1,000 · andar 15 = 1,035 (+3,5%). A soma dos 15 multiplicadores é exatamente 15,000 → **a curva é VGV-neutra**.
- **Escada T0 → T4 = +2,0% simples** (linear) sobre a T0. R$/m² médio: **T0 13.400 · T1 13.668 · T2 13.936 · T3 14.204 · T4 14.472**.
- **VGV T0 (45 un.) = R$ 77.533.740.** VGV de comercialização (39 un., escalonado T0–T4) ≈ **R$ 69,2 M**. Ticket médio comercial ≈ **R$ 1,77 M**.

**Tickets na T0** (área × 13.400 × multiplicador de andar):

| Tipo | Área | Andar 1 (×0,965) | Andar 8 / média (×1,000) | Andar 15 (×1,035) |
|---|---|---|---|---|
| Tipo 01 — 4D | 134,68 m² | R$ 1.741.547 | R$ 1.804.712 | R$ 1.867.877 |
| Tipo 02 — 3D | 116,38 m² | R$ 1.504.910 | R$ 1.559.492 | R$ 1.614.074 |

**Extremos de R$/m² em toda a tabela:** mínimo R$ 12.931 (T0 × andar 1) · máximo **R$ 14.979** (T4 × andar 15).

---

## 1. Conjunto competitivo — 4 rótulos de relevância

O Dom Manuel fica em **Ponta d'Areia**. A **Península** é uma região distinta e **mais valorizada** — entra como referência-teto, não como concorrência de bairro.

| Rótulo | Empreendimentos | Região |
|---|---|---|
| **Concorrência direta** | Vernazza · Zion · LIV Residence · ORO | Ponta d'Areia (microlocalização) |
| **Concorrência indireta** | Renaissance Conceito · Entre Rios | Renascença II |
| **Referência-teto** (região-prêmio) | Monte Meru · Mount Solaro · Reserva Península | Península |
| **Referência de produto** | Giardino Residenza · Landscape · Reserva São Marcos | Ponta do Farol · Calhau |

**Calibração da referência de produto.** Plantas-alvo: 3D ≈ 116,38 m² e 4D ≈ 134,68 m². Banda ±15% combinada: **98,9 – 154,9 m²**. Entram verticais de regiões distintas com pelo menos uma planta 3D/4D na banda. Descartados por área: The View (36–86 m²), Edifício Bossa (191–196 m²), Fiji (62–81 m²), Cidade de Viena (61–87 m²), Le Noir (50–63 m²), Wave/Sky/Azimuth/Quartier 22/Al Mare (165–293 m²), entre outros.

### 1.1 Tabela comparativa — nível planta

R$/m² e ticket do **U_RAW** (unidade a unidade) onde disponível; caso contrário da Composição/E_RAW.

#### Concorrência direta — Ponta d'Areia

| Empreend. · Bairro | Tipologia · Planta · Área | Total / Disp | R$/m² mín · méd · máx | Ticket mín – máx (R$) | % vend. | Lanç. → Entrega | Frescor |
|---|---|---|---|---|---|---|---|
| **Vernazza** (Treviso) | 4D · Torre Norte · 130,0 m² | — / 20 | 14.005 · 15.560 · 17.199 | 1.820.603 – 2.235.846 | 65% (180 u) | 02/2025 → 12/2029 | Tab. 02/2026 |
| **Vernazza** (Treviso) | 4D · Torre Norte · 130,49 m² | — / 17 | 14.237 · 15.482 · 17.027 | 1.857.759 – 2.221.890 | " | " | " |
| **Vernazza** (Treviso) | 3D · Torre Sul · 87,98 m² | — / 8 | 14.521 · 15.477 · 17.615 | 1.277.584 – 1.549.799 | " | " | " |
| **Vernazza** (Treviso) | 3D · Torre Sul · 90,10 m² | — / 18 | 14.180 · 15.653 · 17.607 | 1.277.584 – 1.586.363 | " | " | " |
| **Zion** (Ergus) | 4D · mono · 148,55 m² | 60 / 10 | 14.610 · ~15.900 · 17.213 | 2.170.378 – 2.556.972 | **83%** | 09/2025 → 12/2026 | **Tab. 05/2026 — atual** |
| **LIV Residence** (Alfa) | 3D · mono · 90,83 / 91,77 / 100,23 m² | 75 / n/d | **sem dado** | **sem dado** | n/d | 07/2023 → 07/2027 | ⚠️ **Sem tabela** |
| **ORO** (Niágara) | 3D · padrão · 80,32 m² | 88 / 88 | 12.492 · 15.952 · 19.141 | 1.003.326 – 1.537.396 | n/d | 01/2026 → ~2029 | Tab. 01/2026 |
| **ORO** (Niágara) | 4D · Cobertura Duplex · 160,65 m² | 8 / 8 | 15.095 (flat) | 2.425.000 | " | " | " |

#### Concorrência indireta — Renascença II

| Empreend. · Bairro | Tipologia · Planta · Área | Total / Disp | R$/m² mín · méd · máx | Ticket mín – máx (R$) | % vend. | Lanç. → Entrega | Frescor |
|---|---|---|---|---|---|---|---|
| **Renaissance Conceito** (Monteplan) | 3D · Botticelli · 82,0 m² | 72 / 15 | 12.666 · 13.686 · 14.363 | 1.038.621 – 1.177.759 | **~79%** | 06/2025 → 08/2027 | Tab. 04/2026 |
| **Renaissance Conceito** (Monteplan) | 3D · Leonardo · 110,0 m² | 45 / 7 | 12.358 · 13.168 · 14.229 | 1.359.410 – 1.565.192 | " | " | " |
| **Entre Rios** (Mota Machado) | 3D · 125 / 146,82 / 156,94 m² | 30 / 30 | ~14.679 (planta 146,82) · pond. 15.787 | 1.732.638 – 2.719.860 | **0%** (21 meses) | 08/2024 → — | Tab. 04/2026 |

#### Referência-teto — Península (região-prêmio)

| Empreend. · Bairro | Tipologia · Planta · Área | Total / Disp | R$/m² | Ticket (R$) | % vend. | Lanç. → Entrega | Frescor |
|---|---|---|---|---|---|---|---|
| **Monte Meru** (Berg) | 3D · ~135,3–135,8 m² | ~11 rastr. / 2 | 14.280 · 14.298 · 14.316 | 1.932.400 – 1.944.500 | ~82% rastr. | 04/2024 → 04/2027 | **Tab. 05/2026 — atual** |
| **Mount Solaro** (Berg+Gonçalves) | 3D · 104 m² | 50 / n/d | ~15.384 (site) | a partir de ~R$ 1,5 M | 0 | 06/2025 → — | Só site |
| **Reserva Península** (Sá Cavalcante) | 4D · mono · 127,14–171,36 m² | n/d | **sem dado** | **sem dado** | n/d | 09/2025 → — | ⚠️ **Sem tabela** |

#### Referência de produto — Ponta do Farol / Calhau (banda 98,9–154,9 m²)

| Empreend. · Bairro | Tipologia · Planta · Área | Total / Disp | R$/m² mín · méd · máx | Ticket mín – máx (R$) | % vend. | Lanç. → Entrega | Frescor |
|---|---|---|---|---|---|---|---|
| **Giardino Residenza** (Alfa) · Ponta do Farol | 3D · Col. 01 (Luce) · 99,08 m² | — / 2 | 14.556 · 14.778 · 15.000 | 1.442.168 – 1.486.200 | **~89%** (11 disp / 105) | 02/2025 → 12/2029 | Tab. 03/2026 |
| **Giardino Residenza** (Alfa) · Ponta do Farol | 3D · Col. 02 (Luce) · 101,31 m² | — / 2 | 15.668 · 15.708 · 15.747 | 1.587.366 – 1.595.303 | " | " | " |
| **Giardino Residenza** (Alfa) · Ponta do Farol | 3D · Col. 03 (Fiore) · 110,77 m² | — / 1 | 16.865 | 1.868.169 | " | " | " |
| **Giardino Residenza** (Alfa) · Ponta do Farol | **4D** · Col. 01 (Fiore) · 127,30 m² | — / 4 | 14.442 · 15.181 · 15.970 | 1.838.492 – 2.032.938 | " | " | " |
| **Giardino Residenza** (Alfa) · Ponta do Farol | **4D** · Col. 02 (Fiore) · 128,37 m² | — / 1 | 14.650 | 1.880.620 | " | " | " |
| **Landscape** (Delman) · Calhau | 3D · 88,07 m² *(abaixo da banda)* | — / 17 | 13.697 · 14.755 · 15.900 | 1.206.282 – 1.400.282 | **46%** (44 / 95) | 03/2026 → 09/2029 | Tab. 04/2026 |
| **Landscape** (Delman) · Calhau | 4D · 103,60 m² | — / 31 | 13.789 · 14.578 · 15.517 | 1.428.516 – 1.607.516 | " | " | " |
| **Landscape** (Delman) · Calhau | 4D · duplex cob. · 123,69 m² | — / 1 | 16.197 | 2.003.372 | " | " | " |
| **Landscape** (Delman) · Calhau | 4D · duplex cob. · 143,64 m² | — / 2 | 16.000 · 16.106 · 16.213 | 2.298.197 – 2.328.766 | " | " | " |
| **Reserva São Marcos** (Mota Machado) · Calhau | 4D · Litorânea · 103,15 m² | 36 / 4 | 14.581 · 16.263 · 17.944 | 1.504.065 – 1.850.952 | **~89%** (10 disp / 90) | 01/2025 → 02/2029 | Tab. 04/2026 |

> **Tipologia Giardino (book Alfa, v11.24).** Torre Fiore: Col 01 (127,30 m²) e Col 02 (128,37 m²) são **4D** (2 suítes + 2 semissuítes, 3 vagas); só a Col 03 (110,77 m²) é 3D (3 suítes). Torre Luce é 100% 3D (3 suítes, 93–101 m²). Ou seja, **a única 3D-grande do Giardino é a Col 03 de 110,77 m²** — toda a faixa 127–128 m² é 4D.

### 1.2 Curva de andar — prêmio %/pavimento praticado

Andar derivado da numeração do apto; prêmio = variação composta do ticket entre o andar mais baixo e o mais alto de um mesmo "final".

| Concorrente | Rótulo | Planta | **Prêmio praticado** | Confiança |
|---|---|---|---|---|
| **ORO** | direta | 3D 80 m² | **+3,41%/andar** (escalonado — salto no 5º) | Alta |
| **Reserva São Marcos** | ref. produto | 4D 103 m² | +1,90%/andar | Baixa (2 pontos) |
| **Vernazza** | direta | 4D 130 m² | **+1,50%/andar** | Alta |
| **Vernazza** | direta | 3D 88–90 m² | +1,38%/andar | Alta |
| **Zion** | direta | 4D 148 m² | ~+1,3%/andar (inferido) | Baixa — SKUs sintéticos |
| **Giardino Residenza** | ref. produto | **4D** 127 m² | +1,12%/andar | Média |
| **Renaissance** | indireta | 3D Leonardo 110 m² | +1,09%/andar | Média |
| **Renaissance** | indireta | 3D Botticelli 82 m² | +0,94%/andar | Média-alta |
| **Landscape** | ref. produto | 3D 88 m² | +0,93%/andar | Alta |
| **Landscape** | ref. produto | 4D 103,6 m² | **+0,78%/andar** | Alta |
| **➤ Dom Manuel (proposto)** | — | 3D/4D | **±0,50%/andar** (curva centrada — spread topo×base ~7,3%) | — |

> **Armadilha metodológica (kickoff item 4).** Em São Luís, o número do apto **nem sempre reflete a posição física** — algumas construtoras numeram o 1º pavimento-tipo como "4º andar". O **prêmio %/andar acima é confiável** (a variação entre andares consecutivos independe de onde a contagem começa). O que exige o offset físico real é o agrupamento por **faixa de andar** (baixa 1º–4º · médio 5º–9º · alto 10º–15º) — a ser registrado nas próximas extrações.

**Mediana do conjunto com curva confiável: ≈ +1,1 a +1,5%/andar.** O Dom Manuel, a ±0,50%/andar, tem a **menor diferenciação por andar de toda a amostra**.

---

## 2. Síntese para o Dom Manuel

### 2.1 Onde os R$ 13.400/m² (T0) se posicionam

Como o R$ 13.400/m² é a **média ponderada da T0** (já incorpora a curva de andar, que é centrada), ele é diretamente comparável à média dos concorrentes.

| Rótulo | R$/m² representativo dos concorrentes | Dom Manuel T0 | Gap |
|---|---|---|---|
| **Concorrência direta** (Ponta d'Areia) | Vernazza ~15.500 · Zion ~15.900 · ORO ~15.950 · *LIV s/ dado* | 13.400 | **−14% a −16% abaixo** |
| **Concorrência indireta** (Renascença II) | Renaissance ~13.560 · Entre Rios ~14.700–15.800 | 13.400 | Par com Renaissance |
| **Referência-teto** (Península) | Monte Meru ~14.300 *(vintage 2024)* | 13.400 | abaixo da região-prêmio |
| **Referência de produto** (Ponta do Farol/Calhau) | Giardino ~15.400 · Landscape núcleo ~14.600 · Reserva SM ~16.300 | 13.400 | **−8% a −18% abaixo** |

**Conclusão:** R$ 13.400/m² é o **R$/m² mais baixo de todo o conjunto comparável** — único par é o Renaissance (Renascença II, microrregião inferior à Ponta d'Areia). Mesmo o **teto absoluto da tabela** (T4 × andar 15 = R$ 14.979/m²) fica abaixo da concorrência direta atual. **O Dom Manuel oferece produto de Ponta d'Areia ao R$/m² de Renascença II.**

**Leitura por ticket.** O Dom Manuel vende unidades grandes (116–135 m²). O **Tipo 01** (4D 134,68 m², ticket T0 médio R$ 1,80 M) fica abaixo de Vernazza Norte (R$ 1,82–2,24 M) e Zion (R$ 2,17–2,56 M), na própria Ponta d'Areia, ao nível de Monte Meru (R$ 1,93 M, Península) e — agora confirmado pelo book — **abaixo do par 4D do Giardino Fiore** (127–128 m², R$ 1,84–2,03 M, Ponta do Farol). Ou seja, o Dom Manuel entrega um 4D **maior** (134,68 vs 127–128 m²) e **mais barato** que o 4D do Giardino. O **Tipo 02** (3D 116 m², ticket T0 médio R$ 1,56 M) **não tem par direto** — ver §3.

### 2.2 Curva de andar — ±0,5% é conservador, mas a discussão mudou

**A inclinação da curva é VGV-neutra.** A curva é centrada no 8º andar e a soma dos 15 multiplicadores é exatamente 15,000. Tornar a curva mais inclinada **redistribui** valor (andares baixos mais baratos, altos mais caros) mas **não cria VGV** — *o "+R$ 2,7 M" da rev.2 não existe*.

A discussão de inclinação, portanto, **não é de captura de VGV — é de sell-through:**

- Dom Manuel diferencia os andares em ~7,3% topo×base (±0,5%/andar). O mercado pratica bem mais: Vernazza +1,5%/andar (~+21% topo×base), Giardino +1,1%, ORO +3,4% com salto de vista no 5º andar.
- **Argumento para inclinar mais:** na Ponta d'Areia o andar alto tem vista mar e vende-se sozinho — pode absorver prêmio maior; o andar baixo é a venda difícil e um desconto mais fundo acelera a absorção. Uma curva mais inclinada **alinha preço à disposição a pagar** e tende a melhorar a velocidade global.
- **Limite:** como a curva é centrada, inclinar mais **levanta o topo**. A ±1,0%/andar, o apto andar 15 na T4 chega a **R$ 15.485/m²** — dentro da faixa de giro lento (ver §2.4). A ±0,75%/andar fica em ~R$ 15.230/m². **Recomendação:** se inclinar por razões de sell-through, manter em torno de **+0,75%/andar** — preserva o topo abaixo de ~R$ 15,3 k e ainda assim quase dobra a diferenciação atual.

### 2.3 Velocidade — 39 unidades em ~12 meses é realista?

**Meta:** 39 u / 12 meses = **3,25 u/mês** (≈ 87% do total no ano 1).

| Concorrente | Absorção observada | Ritmo |
|---|---|---|
| Vernazza | 65% (~117 u) / ~12 meses | ~9,7 u/mês |
| Renaissance | ~79% (~83 u) / ~10 meses | ~8,3 u/mês |
| Giardino Residenza | ~89% (~94 u) / ~13 meses | ~7,2 u/mês |
| Zion | 83% (50 u) / ~8 meses (*0 vendas desde abr/26*) | ~6,3 u/mês |
| Reserva São Marcos | ~89% (80 u) / ~15 meses | ~5,3 u/mês |

**Veredito: realista — e até conservadora, se o preço for disciplinado.** O ritmo-alvo de 3,25 u/mês está bem abaixo da absorção típica das fases boas desses lançamentos. Vender 87% no ano 1 é ambicioso mas alinhado aos fortes; e o Dom Manuel joga a favor: só 45 unidades (carteira pequena) e o R$/m² mais barato do conjunto. **O gargalo não é demanda — é disciplina de preço** (§2.4).

### 2.4 Teto de preço / elasticidade do bairro

**A zona de giro lento existe e está documentada:**

- **Zion** (Ponta d'Areia) — as 10 unidades não vendidas estão a R$ 14,6–17,2 k/m² · **0 vendas entre abr e mai/2026**.
- **Entre Rios** (Renascença II) — R$ 13,9–17,3 k/m² · **0% vendido em 21 meses**.

**A escada do Dom Manuel está inteira na zona líquida.** Com o modelo atual (±0,5%/andar, escada +2% simples), o **R$/m² máximo de toda a tabela é R$ 14.979** (T4 × andar 15) — abaixo do patamar onde Zion/Entre Rios travam. O alarme de "zona morta" da rev.2 estava superdimensionado (vinha de ter lido o 13.400 como piso e a escada como composta). **Não há risco de teto no modelo atual.**

A única forma de criar exposição é **inclinar demais a curva de andar**: a ±1,0%/andar o topo na T4 sobe a R$ 15.485/m² e entra na faixa de giro lento — daí o limite de ~+0,75%/andar recomendado em §2.2.

---

## 3. Sinais de oportunidade para a DOM

- **Posição "3D grande" não disputada — agora ainda mais clara.** O Tipo 02 (3D 116 m², 3 suítes, ticket T0 ~R$ 1,56 M) não tem concorrente direto: as 3D da Ponta d'Areia são pequenas (ORO 80 m², Vernazza Sul 88–90 m², LIV 91–100 m²) e as grandes são 4D. A correção do book **reforça** o nicho: o que parecia uma 3D de 127 m² no Giardino (Ponta do Farol) é na verdade **4D** — a única 3D-grande de toda a referência de produto agora é a Col 03 do Fiore (110,77 m², 1 unidade restante). Uma 3D de 116 m² entrega **espaço de 4D com ticket de 3D** — nicho efetivamente vazio na microrregião.
- **Preço-âncora competitivo.** R$ 13.400/m² na Ponta d'Areia, com Zion travado no teto na mesma microrregião, posiciona o Dom Manuel como o melhor custo-benefício do bairro no lançamento.
- **Folga de tabela.** A escada T0→T4 inteira fica abaixo da concorrência direta — há espaço de manobra comercial sem perder a âncora de preço.

---

## 4. Lacunas e recomendações de refresh

### 4.1 Frescor do dado por concorrente

| Concorrente | Status | Ação |
|---|---|---|
| **Zion / Monte Meru** | Tabela mai/2026 — atual | OK (Zion: re-parsear SKUs sintéticos para a curva de andar real) |
| **LIV Residence** | ⚠️ **Crítico — sem tabela** | Concorrente direto cego. Capturar tabela atual (corretor Alfa) |
| **ORO** | Tabela 01/2026 · matriz por posição | % vendido não determinável — obter tabela de estoque |
| **Vernazza** | Tabela 02/2026 (~3,5 m) | Refresh para velocidade atualizada |
| **Entre Rios** | Tabela 04/2026 · agregada | Extração por unidade; confirmar o "0% em 21 meses" |
| **Mount Solaro / Reserva Península** | Só site, sem tabela | Capturar tabelas (fecham a referência-teto da Península) |
| **Giardino / Landscape / Reserva São Marcos** | Tabelas 03–04/2026 | Aceitável; re-checar as "pré-lançamento" |

### 4.2 Armadilha a corrigir nas próximas extrações

Registrar o **andar físico real** (offset de pódio) por unidade — habilita a comparação por faixa de andar (baixa/médio/alto) que a versão final do estudo exige.

### 4.3 Manutenção da base — concluído nesta rodada (Planilha v11.21)

- ✅ **Entry Dom Manuel corrigida:** Tipo 02 área 113,50 → **116,38 m²**; R$/m² 12.000 → **13.400** (média ponderada); tickets e VGV (**R$ 77.533.740**) recalculados; cronograma 06/2026 → 11/2029; modelo de preço documentado nas Observações.
- ✅ **Bug do Renaissance saneado:** U_RAW deduplicado (44 → 22) — % vendido corrigido de 58% para **~79%**.
- ✅ Planilha regenerada (**v11.21**), `index.html` regenerado, `ESTADO_ATUAL.md` atualizado. Falta o commit/push, feito pelo Rafael via `publish.sh`.
- ✅ **(rev.4, 02/06/2026)** Tipologia Giardino Torre Fiore corrigida via book (Col 01/02 3D→4D); base regenerada (**v11.24**), `ESTADO_ATUAL.md` atualizado. Falta o commit/push (Rafael, `publish.sh`).

---

*Relatório rev.5 — correção de tipologia do Renaissance Conceito (Leonardo 4D→3D, site Monteplan, 02/06/2026) sobre a rev.4. Base: Planilha Mestre Panorama v11.25, U_RAW, Composição, `ESTADO_ATUAL.md`.*
