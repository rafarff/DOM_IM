# Prompt — Deep Research: datas de início de comercialização (São Luís/MA)

**Instruções de uso:** copie tudo abaixo da linha "────" e cole em uma plataforma de IA com capacidade de pesquisa web profunda (Perplexity Pro / ChatGPT com browsing / Claude com web search / Gemini com Deep Research). Espere o relatório e me devolva em formato Markdown. Rode uma consulta separada para cada incorporadora, se for mais efetivo.

────

# TAREFA

Você é um analista de inteligência de mercado imobiliário. Preciso que estime a **data de início de comercialização** (mês/ano) de cada empreendimento listado abaixo, localizado em **São Luís, Maranhão, Brasil**.

## Definição crítica de "início de comercialização"

**Use esta definição exata.** A data que eu quero é o mês em que existiu a **primeira evidência concreta de comercialização**, não o evento oficial de lançamento. Considere que:

- Incorporadoras costumam usar rótulos comerciais como *"breve lançamento"*, *"pré-lançamento"*, *"lançamento oficial"* — esses são artefatos de marketing. A comercialização efetiva pode começar **meses antes** do evento oficial.
- **Data da tabela de preços NÃO é data de lançamento.** Tabelas são reemitidas mensalmente pela incorporadora para se proteger contra desatualização de preços. Uma tabela de ABR/2026 apenas prova que havia vendas em abril/2026 — não diz quando começaram.
- **Data da entrega menos 36 meses (T-36)** é um estimador sistemático razoável para verticais, e 24-36 meses para horizontais.
- **Memorial de Incorporação em cartório** é o piso legal absoluto — vendas não podem iniciar antes.

## Hierarquia de evidência (mais forte → mais fraca)

1. **Memorial de Incorporação** registrado em Cartório de Registro de Imóveis (RI) — procurar número do registro + data
2. **Book/folder promocional** — data de criação do arquivo digital ou menção pública de distribuição
3. **T-36** calculado a partir da data de entrega prevista
4. **Menção em imprensa local de MA** com data específica — fontes: Imirante, O Estado do Maranhão, MaHoje, Frisson, O Imparcial
5. **Post datado em redes sociais** da incorporadora (Instagram, Facebook) mencionando lançamento

## Fontes brasileiras prioritárias para consulta

- Sites oficiais das incorporadoras (buscar no Google com nome + "São Luís")
- Cartórios de Registro de Imóveis de São Luís (1º RI e 2º RI)
- Imprensa MA: imirante.com, oestadoma.com, mahoje.com.br, frissonmag.com.br
- Imobiliárias parceiras: Habittare, ZIAG Imóveis, Ferreira Imóveis, Brasil Brokers MA
- Instagram da incorporadora: procurar pelo primeiro post sobre o empreendimento
- Portais nacionais: VivaReal, ZAP Imóveis, ImóvelWeb, QuintoAndar

## Empreendimentos — priorizados por criticidade

### PRIORIDADE ALTA — sem nenhuma data estimada (pendentes)

| # | Empreendimento | Incorporadora | Bairro | Tipo | Segmento |
|---|---|---|---|---|---|
| 1 | Vila Coimbra | Castelucci | Araçagi | Horizontal | Alto |
| 2 | Village Del Ville II | Canopus | São Luís (bairro a confirmar) | Horizontal | — |
| 3 | Village Prime Eldorado | Canopus | Jardim Eldorado | Horizontal | — |
| 4 | Village Reserva II | Canopus | São Luís (bairro a confirmar) | Horizontal | — |
| 5 | Reserva Península | Sá Cavalcante | Ponta d'Areia | Vertical | Alto |
| 6 | Giardino Residenza | Alfa Engenharia | Ponta do Farol | Vertical | — |
| 7 | Monte Meru | Berg Engenharia | Ponta d'Areia | Vertical | Alto |
| 8 | Mount Solaro | Berg Engenharia | São Luís (bairro a confirmar) | Vertical | — |
| 9 | Villagio Treviso | Treviso Engenharia | São Luís (bairro a confirmar) | Horizontal | — |
| 10 | Villa di Carpi | Castelucci | Cohatrac | Horizontal | — |
| 11 | Varandas Grand Park | Franere | São Luís (bairro a confirmar) | Horizontal | — |
| 12 | Lagoon Residence | Lua Nova | Santo Amaro | Vertical | — |
| 13 | Villa Adagio | Lua Nova | São Luís (bairro a confirmar) | Horizontal | — |
| 14 | Ilha Parque Residence | Sá Cavalcante | Maranhão Novo | Horizontal | Médio |

### PRIORIDADE MÉDIA — com estimativa fraca (validar ou corrigir)

| # | Empreendimento | Incorporadora | Data atual (fraca) | Bairro |
|---|---|---|---|---|
| 15 | Residencial Ana Vitória | Castelucci | 06/2023 (estimado) | Araçagy |
| 16 | Nexus Renascença | Ergus | 06/2023 (estimado) | Renascença |
| 17 | Condomínio Prime Cohama | MB Engenharia | 06/2023 (estimado) | Cohama |

### PRIORIDADE BAIXA — bônus, validar estimativa por book

| # | Empreendimento | Incorporadora | Data atual | Origem atual |
|---|---|---|---|---|
| 18 | Connect Península | Alfa Engenharia | 07/2024 | book (data do PDF) |
| 19 | LIV Residence | Alfa Engenharia | 07/2023 | book (data do PDF) |
| 20 | Legacy Residence | Alfa Engenharia | 07/2024 | book (data do PDF) |

## Formato de resposta obrigatório

Para cada empreendimento, me devolva uma linha no formato Markdown abaixo:

```
### [Nome do empreendimento] — [Incorporadora]
- **Data estimada**: MM/AAAA
- **Fonte principal**: [URL ou descrição]
- **Tipo de fonte**: memorial | book | imprensa | post redes sociais | site oficial | outra
- **Confiança**: alta | média | baixa
- **Evidência textual** (cite trecho): "..."
- **Notas**: qualquer contexto adicional relevante (ex: contradições entre fontes, status atual no mercado)
```

Se não conseguir encontrar **nenhuma evidência confiável** para um empreendimento, responda:

```
### [Nome] — [Incorporadora]
- **Data estimada**: não localizada
- **Tentativas**: [liste os termos/URLs que tentou]
- **Notas**: sugestão de próximo passo (ex: "contatar corretor", "buscar em cartório")
```

## Regras importantes

1. **Não invente datas.** Se só tem "lançamento 2024" num site, diga "somente ano confirmado (2024), mês incerto" — não chute o mês.
2. **Priorize fontes brasileiras em português.** Os competidores são locais de MA.
3. **Cite sempre a URL ou fonte específica.** Não basta dizer "segundo a imprensa" — preciso do link.
4. **Cuidado com projetos homônimos em outras cidades.** Vários nomes usados em São Luís também existem em outras capitais (ex: Vernazza em Londrina, ES). Sempre confirme "São Luís/MA" no contexto.
5. **Se tiver dúvida entre "pré-lançamento" e "lançamento oficial"**, use a data do **pré-lançamento** — é quando a comercialização efetivamente começa.

## Contexto adicional sobre as incorporadoras

- **Canopus** — especialista em condomínios horizontais tipo "Village" em São Luís
- **Sá Cavalcante** — histórico em empreendimentos grandes no segmento médio (Maranhão Novo)
- **Berg Engenharia** — alto padrão em Ponta d'Areia
- **Treviso Engenharia** — inspiração italiana, verticais alto padrão (nome Vernazza é deles)
- **Alfa Engenharia** — foco em Ponta d'Areia e Ponta do Farol, alto e luxo
- **Castelucci** — horizontais em Araçagi e Cohatrac
- **Lua Nova** — Santo Amaro e bairros médios
- **Franere** — construtora de médio-grande porte em MA
- **MB Engenharia** — médio padrão, Cohama

────

# FIM DO PROMPT
