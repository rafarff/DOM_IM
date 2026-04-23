# PADRÃO FASE 1 — Inteligência de Mercado DOM
**Versão:** 1.2 (atualizada em 14/04/2026)
**Status:** 🟢 APROVADO pelo Rafael

> **ATENÇÃO — Claude:** este documento é um CONTRATO. Toda vez que o Rafael
> disser qualquer um dos 5 comandos (§5), LEIA ESTE ARQUIVO E O SCRIPT
> `gerar_planilha.py` ANTES de executar qualquer ação. Não improvise regras
> fora deste padrão. Para qualquer mudança estrutural, **peça aprovação
> explícita** antes de alterar este arquivo.

---

## Sumário
1. Dicionário de dados — aba Empreendimentos (24 colunas)
2. Dicionário de dados — aba Incorporadoras (17 colunas)
3. Regras de cálculo (fórmulas congeladas)
4. Enumerações fixas
5. Comandos padronizados (5 gatilhos)
6. Hierarquia de fontes
7. Output e naming

---

## 1. Aba Empreendimentos — 24 colunas

| # | Campo | Tipo | Formato / Regra | Obrig. |
|---|---|---|---|---|
| 1 | Incorporadora | Enum §4.1 | Nome exato da lista | ✅ |
| 2 | Empreendimento | Texto | Nome comercial | ✅ |
| 3 | Endereço | Texto | `Rua, Nº, Bairro, São Luís - MA`. Se não souber: `Não localizado` | ✅ (formato) |
| 4 | Bairro | Texto | Bairro oficial | ✅ |
| 5 | Segmento | Enum §4.2 | Classificado por R$/m² calculado, não por ticket | ✅ |
| 6 | Status | Enum §4.3 | Status comercial (não físico) | ✅ |
| 7 | Nº total unidades | Inteiro | Da memorial/book/web | ⚠️ |
| 8 | Mês lançamento | Data MM/AAAA | Se estimado, sufixar `⚠ T-36` | ✅ |
| 9 | Mês entrega | Data MM/AAAA | | ⚠️ |
| 10 | Área mín (m²) | Decimal | | ⚠️ |
| 11 | Área máx (m²) | Decimal | | ⚠️ |
| 12 | Tipologia média (m²) | Calculado | `(área_min + área_max) / 2` | 🔄 |
| 13 | Tipologia (dorms) | Texto | Ex: `2Q (1 suíte) a 3Q (1 suíte)` | ⚠️ |
| 14 | Ticket mín (R$) | Moeda | | ⚠️ |
| 15 | Ticket máx (R$) | Moeda | | ⚠️ |
| 16 | Preço médio R$/m² | Calculado | §3.1 | 🔄 |
| 17 | VGV estimado (R$) | Calculado | §3.2 | 🔄 |
| 18 | % Vendido | Calculado | §3.3. Inverso do estoque (1 − estoque%). Sem coloração condicional. | 🔄 |
| 19 | Origem preços | Enum §4.4 | | ✅ |
| 20 | Origem estoque | Enum §4.4 | | ✅ |
| 21 | Origem lançamento | Enum §4.4 | | ✅ |
| 22 | Link fonte principal | URL | Obrigatório se origem ≠ tabela_local | ⚠️ |
| 23 | Data última verificação | Data DD/MM/AAAA | | ✅ |
| 24 | Observações | Texto livre | Números absolutos do estoque, datas da tabela usada | opcional |

## 2. Aba Incorporadoras — 17 colunas

| # | Campo | Tipo |
|---|---|---|
| 1 | Incorporadora | Enum §4.1 |
| 2 | Nº empreend. mapeados | Inteiro |
| 3 | VGV total estimado (R$) | Soma §3.2 |
| 4 | VGV lançado 2024 | Subconjunto §3.4 |
| 5 | VGV lançado 2025 | Subconjunto §3.4 |
| 6 | VGV lançado 2026 | Subconjunto §3.4 |
| 7 | Segmentos de atuação | Lista §4.2 |
| 8 | Bairros de atuação | Lista de bairros |
| 9 | Ticket médio carteira | Média simples |
| 10 | R$/m² médio carteira | Média ponderada por unidades |
| 11 | % carteira com fonte local | `empreend_com_A / total × 100` |
| 12 | Site oficial | URL |
| 13 | Instagram | `@handle` ou URL |
| 14 | Posicionamento de marca | Texto curto |
| 15 | Última atualização | DD/MM/AAAA |

> **v4.2 (14/04/2026):** removidas colunas RI e Capital aberto — irrelevantes para o universo de incorporadoras de São Luís, todas de capital fechado.

---

## 3. Regras de cálculo (congeladas)

### 3.1 Preço médio R$/m²
Padrão (quando temos min/max):
```
ticket_médio = (ticket_min + ticket_max) / 2
área_média   = (área_min + área_max) / 2
preço_m²     = ticket_médio / área_média
```
Ideal (quando temos tabela completa com todas unidades):
```
preço_m² = Σ(preço_unidade) / Σ(área_unidade)
```

### 3.2 VGV estimado por empreendimento
```
VGV = ticket_médio × unidades_totais
```
Quando não há ticket mas há outro empreendimento da mesma incorporadora no mesmo segmento/bairro, usar preço_m² como proxy:
```
VGV = preço_m²_proxy × área_média × unidades_totais
```

### 3.3 % Vendido (método hierárquico)
**Ordem de busca de `unidades_disponíveis`:**
1. 🥇 **Tabela PDF vigente** → linhas sem marca "VENDIDA"
2. 🥈 **Site oficial / simulador** → unidades listadas no configurador
3. 🥉 **Portal agregador** (Ziag, MGF, Chaves na Mão, QuintoAndar) → anúncios únicos
4. 4️⃣ **Input do corretor** → quando Rafael passar

**Em Observações sempre registrar:** número absoluto + fonte + data.
Exemplos: `"101 de 144 vendidas — Tabela Fev/2026"` | `"vendido=79% via Ziag 14/04/26"`

```
vendido_% = (unidades_totais − unidades_disponíveis) / unidades_totais × 100
         = 1 − estoque_%
```
**Sem coloração condicional** — coluna apresenta apenas o número percentual.
Interpretação executiva: **≥85% = últimas unidades; 60–85% = em absorção; <60% = estoque amplo** (usado pelo Status §4.3, não como formatação da célula).

### 3.4 VGV por ano (aba Incorporadoras)
```
VGV_ano_X = Σ(VGV do empreendimento) onde mês_lançamento.ano == X
```
Apenas anos 2024, 2025, 2026. Empreendimentos com lançamento estimado (⚠ T-36) entram no ano estimado.

### 3.5 Lançamento estimado (quando desconhecido)
```
mês_lançamento_estimado = mês_entrega - 36 meses
flag = "⚠ T-36"
```
*Regra T-36:* ciclo médio estimado de construção (obra) no segmento médio-alto/alto de SL: 36 meses entre lançamento comercial e entrega. Substituir por data real assim que: tabela datada, data no book, release/imprensa, **post do Instagram marcando lançamento**, **treinamento de corretor** (forte sinal), campanha de teaser.

---

## 4. Enumerações fixas

### 4.1 Incorporadoras monitoradas (14 — lista fechada)
Mota Machado, Berg Engenharia, Alfa Engenharia, Lua Nova, Delman, Treviso, Ergus, Monteplan, Franere, Canopus, Niágara, MB Engenharia, Sá Cavalcante, **Castelucci**.

> Adicionar/remover: só com aprovação explícita do Rafael; atualizar este arquivo.

### 4.2 Segmento (por R$/m² médio calculado — São Luís, 2026)
| Segmento | Faixa R$/m² | Observação |
|---|---|---|
| Popular | < R$ 6.000 | MCMV, faixas 2-3 |
| Médio | R$ 6.000 – R$ 9.000 | |
| Médio-alto | R$ 9.000 – R$ 13.000 | |
| Alto | R$ 13.000 – R$ 18.000 | Maior concentração atual em Ponta d'Areia |
| Luxo | > R$ 18.000 | Wave, Sky, Azimuth, Quartier 22 |

⚠️ Valores calibráveis após migração inicial dos dados. Revisar em cada update anual.

### 4.3 Status (6 níveis — comercial, não físico)
| Status | Critério |
|---|---|
| Pré-lançamento | Teaser ativo, sem tabela pública |
| Lançamento | Tabela ativa, < 6 meses de venda |
| Em comercialização | Tabela ativa, > 6 meses, % vendido < 60% |
| Últimas unidades | % vendido ≥ 85% |
| Entregue | Habite-se emitido |
| Esgotado | % vendido = 100% ou retirado do site/tabela |

### 4.4 Origens (valores permitidos)
**Origem preços:** `tabela_local` | `site_oficial` | `agregador` | `imprensa` | `estimativa`
**Origem estoque:** `tabela_local` | `site_oficial` | `agregador` | `corretor` | `estimativa`
**Origem lançamento:** `book` | `release` | `treinamento_corretor` | `site_oficial` | `imprensa` | `estimativa_T-36`

---

## 5. Comandos padronizados (5 gatilhos)

### 5.1 "atualiza o estudo"
Passo-a-passo obrigatório:
1. Ler este PADRAO.md primeiro
2. Varrer `/01.Inteligência Mercado/XX_*/` por arquivos novos
3. Para cada uma das 14 incorporadoras: pesquisa web obrigatória nesta ordem:
   a. **Instagram oficial** (últimos ~20 posts — buscar lançamentos, tabelas, teasers)
   b. **Site oficial** (empreendimentos atuais, atualizações de tabela)
   c. 1 portal agregador (Ziag ou MGF)
   d. 1 busca de notícias (Imirante/Diego Emir)
4. Aplicar regras §3 para recalcular campos 12, 16, 17, 18
5. Reclassificar Segmento (§4.2) e Status (§4.3) com base nos valores novos
6. Gerar planilha chamando `gerar_planilha.py`
7. Escrever mini-changelog no final do chat (o que mudou, novas linhas, alertas)

### 5.2 "analisa [incorporadora]"
1. Ler este PADRAO.md
2. Ler SÓ a pasta da incorporadora citada
3. Busca web direcionada nesta ordem: **Instagram (prioridade) → site oficial → imprensa → portal agregador**. No Instagram, revisar últimos ~20 posts + stories destacados.
4. Produzir ficha única (1 página) cobrindo as 10 dimensões do system prompt:
   - Portfólio | Segmento e padrão | Localização/bairros | Tipologia | Preço | Velocidade de vendas | Parceiros | Posicionamento de marca | Pontos fortes/fracos | Movimentos recentes
5. NÃO gerar planilha (análise específica, não atualização geral)

### 5.3 "o que mudou?"
1. Abrir última planilha (`Planilha_Mestre_Panorama_v[max].xlsx`)
2. Abrir a versão anterior
3. Listar apenas diferenças:
   - Novos empreendimentos
   - Mudanças de ticket, R$/m² ou estoque
   - Mudanças de status
4. Retornar bullet list (sem planilha nova)

### 5.4 "oportunidades"
1. Ler planilha atual
2. Cruzar dados para encontrar:
   - Gap segmento × bairro (ex: "nenhum luxo no Renascença")
   - Faixas de ticket pouco disputadas
   - Tipologias ausentes (ex: "nenhum 4Q no Calhau")
   - Bairros com 0-1 concorrente
3. Retornar lista priorizada de 5 oportunidades com: descrição, racional quantitativo, movimento DOM sugerido

### 5.5 "adicionei arquivos de [incorporadora]"
1. Ler SÓ os arquivos novos na pasta indicada
2. Atualizar SÓ as linhas da incorporadora citada
3. Regerar planilha com versão minor bumpada (ex: v2.0 → v2.1)
4. Reportar diff daquela incorporadora

---

## 6. Hierarquia de fontes (6 níveis)

1. **Arquivo local** — `/01.Inteligência Mercado/XX_INCORPORADORA/` (book, tabela, memorial)
2. **Canais oficiais da incorporadora (paridade)** — usar em conjunto; Instagram tem prioridade para movimentos recentes:
   - **Instagram oficial** `@handle` — releases, teasers, stories, posts de lançamento, eventos. **Tipicamente mais atualizado que o site.** Para lançamentos recentes (<90 dias) o Instagram é a fonte primária.
   - **Site oficial** — `/empreendimentos`, `/blog` — tabelas fixas, plantas, materiais institucionais.
3. **Portais agregadores SLZ** — Ziag, Imeu, MGF Imóveis, Chaves na Mão, QuintoAndar
4. **Fontes complementares** — ReclameAqui, diário oficial (licenças de obras/SPE)
5. **Imprensa local** — Imirante, Diego Emir, O Estado, G1 MA
6. **Estimativa** — aplicar regras §3 com flag de incerteza

**Regra de conflito:** quando Instagram e site divergem, Instagram prevalece para informações de <90 dias (lançamentos, campanhas, eventos); site prevalece para informações consolidadas (plantas, tabela cheia).

> `Link fonte principal` (col. 22) é obrigatório quando Origem preços ≠ `tabela_local`.

---

## 7. Output e naming

**Arquivo único:** `Planilha_Mestre_Panorama_vX.Y.xlsx`
**Local:** `/00_ESTUDO_CONSOLIDADO/`

**Regra de ordenação das linhas (aba Empreendimentos):**
1. **Mês de lançamento DECRESCENTE** (mais recente primeiro)
2. Desempate: Incorporadora (A–Z)
3. Desempate final: Empreendimento (A–Z)

Empreendimentos sem data de lançamento vão para o fim da lista.

**Regra de versão:**
- `X` muda com alteração estrutural (nova coluna, nova aba, mudança em §1-§4)
- `Y` muda com nova carga de dados sem mudança estrutural

Arquivos antigos mantidos (histórico). Ao regerar, criar novo vY+1, não sobrescrever.

---

*Qualquer mudança neste padrão requer aprovação explícita do Rafael.
Claude não altera este arquivo por iniciativa própria.*
