# Estudo de Mercado — Dom Manuel
## Diagnóstico, Plano de Execução e Proposta de Padrão

**Resposta ao Kickoff de 25/05/2026** (Planejamento Comercial → Inteligência de Mercado)
**Base IM vigente:** Planilha Mestre Panorama v11.20 · PADRAO v7.0

Conforme o item 7 do kickoff, este documento **não executa** o trabalho — apresenta as três entregas pedidas: **Diagnóstico**, **Plano de execução** e **Proposta de padrão**. As correções de modelo do item 3 já foram absorvidas e estão consolidadas na Parte 0. Nada foi alterado na base nem no relatório nesta etapa (exceto a correção do bairro do Zion, feita antes do kickoff — Planilha v11.20).

---

## Parte 0 — Modelo de preço do Dom Manuel: correções absorvidas

O relatório "Análise Competitiva — Dom Manuel" (rev.2) leu o modelo de preço de forma incorreta em três pontos. Modelo correto, conferido e recalculado:

| Parâmetro | Leitura **errada** da rev.2 | Leitura **correta** (kickoff item 3) |
|---|---|---|
| R$ 13.400/m² | preço-base do 1º andar (T0) | **média ponderada** (apto + vagas) ÷ área privativa, 45 un., na T0 |
| Curva de andar | linear de baixo p/ cima: andar 1 = +0% … andar 15 = +7% | **centrada no 8º andar**: `1 + (andar − 8) × 0,5%` — andar 1 = 0,965 (−3,5%), andar 8 = 1,000, andar 15 = 1,035 (+3,5%) |
| Escada T0→T4 | +2,0% **composto** (×1,0824) | +2,0% **simples/linear** sobre a T0 |
| VGV T0 (45 un.) | R$ 80,2 M | **R$ 77.533.740** |

**Escada corrigida (R$/m² médio):** T0 13.400 · T1 13.668 · T2 13.936 · T3 14.204 · T4 14.472.
**VGV de comercialização** (39 un., escalonado) ≈ R$ 69,2 M → ticket médio comercial ≈ **R$ 1,77 M** (o VGV T0 de 45 un. a R$ 77,5 M dá ticket médio R$ 1,72 M — a diferença é a escada T0→T4).

### Consequências para o relatório rev.2 (a corrigir → rev.3)

- **§2.2 — o "+R$ 2,7 M ao subir o prêmio de andar de +0,5% para +1,0%" não existe.** A curva é centrada no 8º andar e a soma dos 15 multiplicadores é exatamente 15,000 (média 1,000). Mudar a inclinação **redistribui** valor entre andares baixos e altos, mas **não cria VGV** — é VGV-neutro. A discussão de inclinação continua válida, porém como decisão de **sell-through** (aderência à disposição a pagar: andar alto com vista vende-se sozinho; andar baixo precisa do desconto), não de captura de VGV.
- **§2.4 — o risco de "zona morta" está superdimensionado.** O teto absoluto da tabela inteira (T4 × andar 15) = 14.472 × 1,035 = **R$ 14.979/m²**. Toda a escada T0→T4, em qualquer andar, fica **abaixo** da zona morta observada (~R$ 15–16 k). O risco é praticamente dissolvido — o piso mínimo é R$ 12.931/m² (T0 × andar 1).
- **O que permanece válido na rev.2:** o posicionamento competitivo (§2.1, §2.3). Os R$ 13.400/m² sendo **média ponderada** são diretamente comparáveis à média dos concorrentes — e seguem sendo o R$/m² mais baixo do conjunto direto. As curvas de andar dos concorrentes (Vernazza +1,5%/andar, Renaissance +1,0%, etc.) seguem válidas: a **inclinação** %/andar é invariante a onde a numeração começa (ver risco 1.3.A).

---

## Parte 1 — Diagnóstico do estado atual

### 1.1 Qualidade e frescor do dado por concorrente

Conjunto competitivo organizado pelos quatro rótulos de relevância (kickoff item 2):

| Empreendimento (Incorp.) | Rótulo competitivo | Tabela na base | Qualidade do dado | Lacuna principal |
|---|---|---|---|---|
| **Vernazza** (Treviso) | Ponta d'Areia — direta | 02/2026 (~3,5 m) | Boa — 63 un. no U_RAW | Refresh de vintage |
| **Zion** (Ergus) | Ponta d'Areia — direta | **05/2026 — atual** | Preços OK | SKUs sintéticos (D01/V01) — sem curva de andar real |
| **LIV Residence** (Alfa) | Ponta d'Areia — direta | **nenhuma** | ⚠️ **Crítico — zero preço** | Tabela comercial inexistente na base |
| **ORO** (Niágara) | Ponta d'Areia — direta | 01/2026 (~5 m) | Preços OK; estoque não | Tabela é matriz por posição — % vendido não determinável |
| **Renaissance Conceito** (Monteplan) | Renascença II — indireta | 04/2026 | ⚠️ **Bug** — U_RAW duplicado | Dedup (44 linhas = 22 ×2) corrompe o % vendido |
| **Entre Rios** (Mota Machado) | Renascença II — indireta | 04/2026 | Agregada (sem U_RAW) | Sem dado por unidade → sem curva de andar; 0% vendido a confirmar |
| **Monte Meru** (Berg) | Península — referência-teto | **05/2026 — atual** | Boa | Total de unidades do prédio não confirmado |
| **Mount Solaro** (Berg+Gonçalves) | Península — referência-teto | nenhuma (só site) | Fraca | Sem tabela comercial |
| **Reserva Península** (Sá Cavalcante) | Península — referência-teto | nenhuma (só site) | ⚠️ **Fraca — zero preço** | Sem tabela comercial |
| **Giardino Residenza** (Alfa) | Ponta do Farol — ref. produto | 03/2026 | Boa | — |
| **Landscape** (Delman) | Calhau — ref. produto | 04/2026 ("pré-lanç.") | Boa | Re-checar tabela definitiva |
| **Reserva São Marcos** (Mota Machado) | Calhau — ref. produto | 04/2026 ("pré-lanç.") | Boa | Re-checar tabela definitiva |

**Síntese de frescor:** 2 atuais (Zion, Monte Meru) · 5 recentes (mar–abr) · 2 defasados (ORO jan, Vernazza fev) · **3 sem tabela** (LIV, Mount Solaro, Reserva Península).

### 1.2 Lacunas e bugs estruturais

- **LIV Residence — concorrente direto cego.** É um dos quatro de Ponta d'Areia e não tem nenhuma tabela de preço na base. Sem ele, a comparação direta cobre 3 de 4.
- **Renaissance — bug de deduplicação no U_RAW.** 44 linhas que são 22 únicas repetidas; infla a Composição e corrompe o % vendido (a base mostra 58%, o real é ~79%).
- **Zion — SKUs sintéticos.** As unidades estão como D01–D10 / V01–V50, não com a numeração real (202, 1002…). Impede derivar a curva de andar real.
- **Entre Rios — só Composição agregada.** Sem dado por unidade; não dá curva de andar, e o "0% vendido em 21 meses" precisa ser confirmado (estagnação real ou tabela incompleta).
- **ORO — tabela é matriz por posição.** Não espelha estoque; % vendido não determinável.

### 1.3 Riscos e armadilhas metodológicas

- **A. Numeração de andar ≠ posição física.** Algumas construtoras de São Luís numeram o 1º pavimento-tipo como "4º andar" (térreo + garagens/lazer ocupam os primeiros números). O número do apto **não** reflete a posição física. Implicação: a **inclinação %/andar** que extraí é confiável (a variação entre andares consecutivos independe de onde a contagem começa); mas a **faixa de andar** (baixa 1º–4º · médio 5º–9º · alto 10º–15º) exige o *offset de pódio real* de cada prédio. Hoje a comparação por faixa é aproximada por mín/médio/máx — precisa do andar físico. Restrição útil: edifícios residenciais de São Luís não passam de 15 pavimentos-tipo.
- **B. Vagas embutidas.** Os R$ 13.400/m² do Dom Manuel incluem apartamento + vagas ÷ área privativa. Para a comparação ser justa, é preciso confirmar se as tabelas dos concorrentes precificam as vagas dentro ou fora do R$/m² — e padronizar (o piloto já prevê uma linha de vagas).
- **C. Tabelas "pré-lançamento".** Landscape e Reserva São Marcos estão marcadas "pré-lançamento" — podem não refletir a tabela definitiva.
- **D. Defasagem.** ORO (jan/2026) e Vernazza (fev/2026) merecem refresh antes de virarem benchmark final.

### 1.4 Estado dos relatórios

- **Relatório-piloto** (Planejamento Comercial, `Relatorio_Analise_Concorrencia_Dom_Manuel.docx`): **não está acessível** a esta conversa — a pasta `06.Dom Manuel/06.Comercial/…` não está entre as pastas conectadas ao projeto IM. **Preciso dele** para alinhar o formato-alvo (estrutura, tabela por degrau/faixa de andar, linha de vagas, seção de viabilidade).
- **Relatório rev.2 do IM:** contém os três erros de modelo da Parte 0. Precisa virar **rev.3** (correção rápida e mecânica — ver Bloco C).

---

## Parte 2 — Plano de execução

Passos ordenados, **separando alteração de base** (cada uma com pre-flight obrigatório §0.5) **de construção nova**. Já concluído antes do kickoff: correção do bairro do Zion (Península → Ponta d'Areia), Planilha **v11.20**.

### Bloco A — Correções de base (pre-flight §0.5 em cada uma)

| # | Ação | Natureza | Pré-requisito |
|---|---|---|---|
| **A1** | Corrigir a entry **Dom Manuel** na base: Tipo 02 área 113,50 → **116,38 m²**; registrar o modelo de preço correto (13.400 média ponderada, curva centrada no 8º, escada T0–T4 +2% simples) | Edição `gerar_planilha.py` → regenerar planilha | Pre-flight §0.5 |
| **A2** | **Deduplicar o U_RAW do Renaissance Conceito** (44 → 22 únicas) — corrige o % vendido (58% → ~79%) e a Composição | Edição de YAML → regenerar | Pre-flight §0.5 |
| A3 | *(opcional)* Re-parsear os SKUs sintéticos do Zion para a numeração real, habilitando a curva de andar | Edição de YAML | Depende de re-extração da tabela |

### Bloco C — Correção do relatório (rev.2 → rev.3) — *rápido*

Absorver o modelo da Parte 0: corrigir §0/§2.1 (13.400 = média ponderada), remover o "+R$ 2,7 M" de §2.2 e reescrever a recomendação de inclinação como decisão de sell-through, recalibrar §2.4 (teto da tabela R$ 14.979/m², sem zona morta), e adotar os quatro rótulos de micro-região. **É mecânico — pronto para executar assim que houver OK** (ver "Decisões", abaixo).

### Bloco B — Fechamento de lacunas de dado

| # | Ação | Prioridade |
|---|---|---|
| **B1** | **LIV Residence** — capturar a tabela comercial atual (corretor Alfa / site / re-extração) | **Crítica** |
| B2 | Refresh das tabelas defasadas: **Vernazza** (fev) e **ORO** (jan) | Alta |
| B3 | **Reserva Península** e **Mount Solaro** — capturar tabelas (fecham a referência-teto da Península) | Média |
| B4 | Registrar o **andar físico real** (offset de pódio) por unidade nas próximas extrações e retro-checar os concorrentes já extraídos | Alta — habilita a comparação por faixa de andar |
| B5 | **Entre Rios** — extração por unidade + confirmar o "0% vendido" | Média |

### Bloco D — Construção da versão final + instrumento

| # | Ação | Natureza |
|---|---|---|
| D1 | Definir a **estrutura do estudo final** (ver seções na Parte 3) — incluindo a seção "leitura comercial / validação" reservada ao Planejamento Comercial | Construção nova |
| D2 | Montar a **tabela comparativa no formato do piloto**: uma linha por degrau T0–T4, R$/m² e ticket por **faixa de andar** (baixa/médio/alto), mais a linha de vagas | Construção nova |
| D3 | Construir o **instrumento**: aba dedicada no HTML do IM + exportação PDF, no modelo do relatório de viabilidade | Construção nova |

**Decisão de escopo — frente de demanda (kickoff 5.3).** Recomendo tratar a demanda (perfil e tamanho do público-alvo) como **módulo separado / Fase 2**, não travando a entrega do estudo de oferta. Motivo: o estudo de oferta (comparáveis, benchmark, posicionamento de tabela) está com ~80% do dado pronto e responde à pergunta imediata do Planejamento Comercial (a tabela se sustenta?). A demanda exige fontes e método distintos (dados demográficos, renda, CRM/leads) e não deve atrasar a validação da tabela.

### Ordem sugerida

1. **A1 + C** (rápidos, destravam o relatório correto) →
2. **B1** (LIV — lacuna crítica) + **A2** (bug Renaissance) →
3. **B2–B5** (refresh e fechamento de lacunas) →
4. **D1–D3** (versão final + instrumento).

---

## Parte 3 — Proposta de padrão repetível

**Nome proposto: EME — Estudo de Mercado de Empreendimento.** Um procedimento único, disparável, que qualquer empreendimento roda ao entrar na fase de definição do planejamento comercial.

### O que dispara a fase
Um empreendimento atinge o **pré-lançamento (F0)** e precisa de tabela comercial definida. O Planejamento Comercial aciona o IM com um pedido de EME.

### Insumos exigidos (do Planejamento Comercial para o IM)
Parâmetros do empreendimento: tipologias e áreas privativas, **modelo de preço** (média ponderada T0, curva de andar, escada de degraus), tratamento de vagas, cronograma (lançamento/entrega), nº de unidades e mix por pavimento. Sem esses insumos, o EME não roda — a leitura errada do modelo na rev.2 mostra o custo de partir de parâmetros não confirmados.

### O que o EME entrega (do IM para o Planejamento Comercial)
Um **relatório padronizado** + a **aba no HTML** + a **exportação PDF**, com a estrutura fixa:

| Seção | Conteúdo | Responsável |
|---|---|---|
| 0 | Objeto e modelo de preço do empreendimento | IM |
| 1 | Conjunto competitivo nos **4 rótulos**: direta · indireta · referência-teto · referência de produto | IM |
| 2 | Tabela comparativa — 1 linha por degrau T0–T4, R$/m² e ticket por **faixa de andar**, linha de vagas | IM |
| 3 | Curvas de andar (prêmio %/pavimento praticado) | IM |
| 4 | Síntese de posicionamento (preço, inclinação, velocidade, teto/elasticidade) | IM |
| 5 | Lacunas de dado e plano de refresh | IM |
| 6 | **Leitura comercial / validação** — a tabela se sustenta? ajustes? | **Planejamento Comercial** |

### Onde vive no método do IM
- Como um **comando novo no PADRAO** — proponho `§5.x "estuda [empreendimento]"`, paralelo aos comandos existentes (`analisa`, `atualiza`), formalizando insumos, saídas e a estrutura de seções acima.
- O estudo de cada empreendimento vive numa **pasta dedicada** e ganha uma **aba própria no HTML** do IM.
- A base de comparáveis continua sendo a Planilha Mestre / U_RAW / Composição — o EME é um *consumidor* da base, não a altera (exceto correções pontuais, que seguem o §0.5).

### Como se conecta ao Planejamento Comercial
Handoff bidirecional: o **PC envia** os parâmetros de preço; o **IM devolve** o benchmark de oferta; o **PC preenche** a seção 6 (leitura comercial). A divisão do kickoff (item 6) fica formalizada: IM = dados/comparáveis/instrumento; PC = leitura comercial/decisão.

### Os 4 rótulos de micro-região como padrão
Adotar como classificação fixa de qualquer EME — substitui o "Camada 1/2/3" da rev.2:

1. **Concorrência direta** — mesma microlocalização do empreendimento.
2. **Concorrência indireta** — microrregião equivalente.
3. **Referência-teto** — região-prêmio adjacente (ex.: Península para um projeto de Ponta d'Areia).
4. **Referência de produto** — regiões distintas com produto de área comparável.

---

## Decisões que preciso de você

1. **OK para executar A1 + Bloco C já?** São rápidos, mecânicos e destravam um relatório correto (rev.3) e a base alinhada. Sigo o pre-flight §0.5 em A1.
2. **Demanda — Fase 2 separada** (minha recomendação) ou dentro do escopo da versão final agora?
3. **Anexar o relatório-piloto** `Relatorio_Analise_Concorrencia_Dom_Manuel.docx` a esta conversa (ou dar acesso à pasta `06.Dom Manuel`) — preciso dele para que a versão final do IM espelhe o formato.
4. **Confirmar os 4 rótulos de micro-região** e o nome **EME** como padrão repetível.

---

*Documento de planejamento — resposta ao Kickoff de 25/05/2026. Modelo de preço recalculado e conferido. Nenhuma alteração de base ou de relatório executada nesta etapa.*
