# PADRÃO FASE 1 — Inteligência de Mercado DOM
**Versão:** 5.2 (atualizada em 02/05/2026)
**Status:** 🟢 APROVADO pelo Rafael

> **ATENÇÃO — Claude:** este documento é um CONTRATO. Toda vez que o Rafael
> disser qualquer um dos 5 comandos (§5), LEIA ESTE ARQUIVO E O SCRIPT
> `gerar_planilha.py` ANTES de executar qualquer ação. **Antes de QUALQUER
> alteração de dado, executar o protocolo de §0 (sanity check de drift).**
> Não improvise regras fora deste padrão. Para qualquer mudança estrutural,
> **peça aprovação explícita** antes de alterar este arquivo.

---

## Sumário
0. Invariantes operacionais (5 regras invioláveis)
1. Dicionário de dados — aba Empreendimentos (24 colunas)
2. Aba Empreendimentos vs Aba Composição — relação canônica
2.1. Dicionário de dados — aba Composição (10 colunas, v8.0+)
2bis. Dicionário de dados — aba Incorporadoras (15 colunas)
3. Regras de cálculo (fórmulas congeladas)
4. Enumerações fixas
5. Comandos padronizados (5 gatilhos)
6. Hierarquia de fontes
7. Output e naming
8. Estado e versionamento (git)

---

## 0. Invariantes operacionais (5 regras invioláveis)

Estas regras existem porque já tivemos perda de dados entre sessões. **São absolutas.**

### 0.1 Fonte da verdade ÚNICA: `gerar_planilha.py`
Toda informação de empreendimento mora dentro do `E_RAW` em `_PADRAO_FASE_1/gerar_planilha.py`. **Não é permitido editar `.xlsx` ou `index.html` diretamente.** Estes são *outputs* derivados — qualquer edição neles é sobrescrita na próxima rodada do script.

### 0.2 Commit em pacote: script + xlsx + html
Ao regerar a planilha, os 3 arquivos são commitados juntos via `publish.sh`:
- `_PADRAO_FASE_1/gerar_planilha.py` (source-of-truth)
- `Planilha_Mestre_Panorama_vX.Y.xlsx` (output Excel — ver §8 sobre tracking)
- `index.html` (output HTML)

Commit isolado de qualquer um dos 3 sem os outros = drift potencial. Mensagem de commit segue o padrão `vX.Y — descrição curta`.

### 0.3 Sanity check de drift no início de cada sessão
Antes de fazer qualquer alteração de dado, Claude executa:
1. `git status` em `00_ESTUDO_CONSOLIDADO/` — se houver `.py` modificado e não commitado, **PARAR** e avisar Rafael que existe drift de sessão anterior.
2. Contar `len(E_RAW)` e comparar com o número de linhas da última `.xlsx` commitada. Se script gera **menos** empreendimentos que a `.xlsx`, **PARAR** e alertar.
3. Só prossegue depois de Rafael confirmar.

### 0.4 Bootstrap obrigatório (primeira leitura de toda sessão)

Adicionado em **v3.5 (28/04/2026)** após incidente de truncamento silencioso de Glob (Claude confundiu v4.5 com a vigente, quando real era v6.4).

Antes de qualquer ação em qualquer comando (§5), Claude DEVE ler **`ESTADO_ATUAL.md`** na raiz do `00_ESTUDO_CONSOLIDADO/`. Esse arquivo declara:
- Versão Planilha vigente
- Versão PADRAO vigente
- len(E_RAW) e schema (nº de colunas)
- Distribuição da carteira (sanity numérica)
- Bugs latentes conhecidos
- Armadilhas comuns (p.ex.: filtros `startswith` que matam entries reais)

Se contagens em `ESTADO_ATUAL.md` divergirem do que Claude observa em `gerar_planilha.py` ou na .xlsx vigente: **PARAR** e alertar Rafael (provável drift entre sessões).

**Comando one-liner para descobrir versão vigente** (executar antes de confiar em qualquer Glob amplo):
```bash
cd 00_ESTUDO_CONSOLIDADO/ && ls -1 Planilha_Mestre_Panorama_v*.xlsx | sort -V | tail -1
```
Nunca usar `ls` simples para identificar "última versão" — `v4.5` ordena depois de `v4.16` em ordem lexicográfica.

### 0.5 Pre-flight obrigatório (antes de qualquer write/move)

Antes de criar arquivo, mover arquivo, regenerar planilha, ou alterar `gerar_planilha.py`/`PADRAO.md`, Claude apresenta **relatório pre-flight** ao Rafael:

1. **Base atual:** versão Planilha + versão PADRAO + nº empreendimentos
2. **Deltas planejados:** entries +/-, arquivos a mover (origem → destino), regras a alterar
3. **Verificações já realizadas:** invariante 0.3 (sync script ↔ xlsx), bootstrap §0.4
4. **Pendências/riscos:** bugs latentes que possam afetar o ciclo
5. **Aguardar OK explícito do Rafael.** Só prossegue após confirmação.

Exceções (não exigem pre-flight): leitura de arquivos, criação no `outputs/` sandbox, comandos de análise sem persistência (§5.2 "analisa", §5.3 "o que mudou?", §5.4 "oportunidades").

---

## 1. Aba Empreendimentos — 25 colunas (v5.0+)

| # | Campo | Tipo | Formato / Regra | Obrig. |
|---|---|---|---|---|
| 1 | Incorporadora | Enum §4.1 | Nome exato da lista | ✅ |
| 2 | Empreendimento | Texto | Nome comercial | ✅ |
| 3 | Endereço | Texto | `Rua, Nº, Bairro, São Luís - MA` ou Plus Code. Pin no mapa só com endereço completo (§v3.2). Se desconhecido: `Endereço não localizado, BAIRRO, São Luís - MA` | ✅ (formato) |
| 4 | Bairro | Texto | Bairro oficial | ✅ |
| 5 | **Tipo** | **Enum §4.5** | **Vertical / Horizontal / Misto** | ✅ |
| 6 | Segmento | Enum §4.2 | Classificado por R$/m² calculado, não por ticket | ✅ |
| 7 | Nº total unidades | Inteiro | Da memorial/book/web | ⚠️ |
| 8 | **Origem total unid.** | Enum §4.7 | **v9.0+:** indica de onde veio o total da col 7 | ✅ |
| 9 | Mês lançamento | Data MM/AAAA | Se estimado, sufixar `⚠ T-36` | ✅ |
| 10 | Mês entrega | Data MM/AAAA | | ⚠️ |
| 11 | Área mín (m²) | Decimal | | ⚠️ |
| 12 | Área máx (m²) | Decimal | | ⚠️ |
| 13 | Tipologia média (m²) | Calculado | `(área_min + área_max) / 2` | 🔄 |
| 14 | Tipologia | Enum §4.6 | Combinação curta: `Studio`, `1D`, `2D`, `3D`, `4D`, `Lote` (separar por `;` se múltiplas). Ex: `Studio; 2D; 3D` | ✅ |
| 15 | Ticket mín (R$) | Moeda | | ⚠️ |
| 16 | Ticket máx (R$) | Moeda | | ⚠️ |
| 17 | Preço médio R$/m² | Calculado | §3.1 | 🔄 |
| 18 | VGV estimado (R$) | Calculado | §3.2 | 🔄 |
| 19 | % Vendido | Calculado | §3.3. Inverso do estoque (1 − estoque%). Sem coloração condicional. | 🔄 |
| 20 | Origem preços | Enum §4.4 | | ✅ |
| 21 | Origem estoque | Enum §4.4 | | ✅ |
| 22 | Origem lançamento | Enum §4.4 | | ✅ |
| 23 | Link fonte principal | URL | Obrigatório se origem ≠ tabela_local | ⚠️ |
| 24 | Data última verificação | Data DD/MM/AAAA | | ✅ |
| 25 | Observações | Texto livre | Números absolutos do estoque, datas da tabela usada | opcional |

> **v3.0 (27/04/2026):** coluna **Status** removida (antes col 7). Motivo: classificação muito subjetiva e parcialmente derivada de outros campos (estoque, data). §4.3 (enum de Status) e função `reclassificar_status` no script foram removidas. 25 → 24 colunas. **Adicionalmente:** o filtro "ativo no ciclo" no HTML foi eliminado — o Panorama mostra TODOS os 45 empreendimentos mapeados, sem distinção de fase comercial.

> **v3.2 → v3.3 (27/04/2026) — Mapa removido temporariamente:** a feature de mapa interativo (Leaflet + pins por endereço) foi removida do HTML em 27/04/2026 por decisão do Rafael — pins aproximados por bairro estavam confundindo mais do que ajudando. As funções `tem_endereco_completo()` e `geocode_bairro()` permanecem no `build_panorama.py` para futuro retorno. **Regra preservada:** quando o mapa voltar, pin aparece SÓ com endereço completo (Rua/Avenida/Travessa/Praça com nº/quadra OU Plus Code). Pendência "endereço" continua aparecendo na Tabela B até atualização manual via book/corretor.

> **v2.0 (25/04/2026):** coluna **Tipo** (Vertical/Horizontal/Misto) formalizada como col. 5. Antes existia em sessões anteriores mas não estava no PADRAO — daí o drift que perdeu a classificação na v4.17.

> **v2.1 (27/04/2026) — Convenção de área em Horizontais:** quando `Tipo=Horizontal` (casas/sobrados/lotes), as colunas **Área mín/máx (m²)** referem-se SEMPRE à **área CONSTRUÍDA** da unidade. Terreno (geralmente variável por lote) vai para **Observações**, no formato `terreno N–M m²`. Motivo: o cálculo de R$/m² em §3.1 só faz sentido contra a área construída — misturar com terreno distorce a média. Regra detectada com Dom Lucas em 27/04/2026: área máx estava 145,78 (terreno) quando a casa é 100,35 m² construída uniforme.

## 2. Aba Empreendimentos vs Aba Composição — relação canônica

**v4.0 (02/05/2026)** — a Planilha Mestre ganhou uma terceira aba: **Composição**. As três abas têm papéis distintos e devem ser alimentadas em conjunto:

| Aba | Granularidade | Papel |
|---|---|---|
| Empreendimentos | 1 linha por empreend. | Visão por empreend. (KPIs, VGV, % vendido agregado, tipologia como string concatenada) |
| Composição (v8.0+) | 1 linha por empreend × tipologia | Visão analítica (preço médio por tipologia REAL, não inferido) |
| Incorporadoras | 1 linha por incorp. | Agregados por incorp. |

A aba Empreendimentos é a fonte primária. A aba Composição enriquece com detalhe quando a tabela do empreendimento foi processada. Nem todo empreend. tem entry em Composição (gap esperado é parte do roadmap, não inconsistência).

## 2.1. Aba Composição — 10 colunas (v8.0+)

| # | Campo | Tipo | Regra |
|---|---|---|---|
| 1 | Incorporadora | Enum §4.1 | Mesmo nome usado na aba Empreendimentos |
| 2 | Empreendimento | Texto | Mesmo nome usado na aba Empreendimentos |
| 3 | Tipologia | Enum §4.6 | Studio / 1D / 2D / 3D / 4D / Lote |
| 4 | Nº Unidades | Inteiro | Quantidade de unidades disponíveis dessa tipologia |
| 5 | Área mín (m²) | Decimal | |
| 6 | Área máx (m²) | Decimal | |
| 7 | Ticket mín (R$) | Moeda | |
| 8 | Ticket máx (R$) | Moeda | |
| 9 | R$/m² médio | Calculado | Σ(ticket_unidade) / Σ(área_unidade) das unidades dessa tipologia |
| 10 | Origem | Enum §3.7.A | `tabela_local`, `tabela_local_imagem`, `book`, `informado_manualmente` |

**Regra de inferência tipologia × área (SLZ-padrão):** quando tabela não declara explicitamente a tipologia por unidade, usar:
- < 40m² → Studio
- 40-55m² → 1D
- 55-75m² → 2D
- 75-95m² → 3D
- ≥ 95m² → 4D

Em casos especiais (mono-tipologia declarada, áreas em fronteira), classificação manual prevalece.

**O que muda no dashboard com a aba Composição:** a Seção 3 (Análise por Tipologia) deixa de mostrar agregados "mono-tipologia only" e passa a mostrar dados precisos por tipologia. Limitação: cobertura depende de quais empreend. tiveram tabela processada (roadmap dos Lotes).

## 2bis. Aba Incorporadoras — 15 colunas

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
Interpretação executiva (analítica, não estrutural): ≥85% = últimas unidades; 60–85% = em absorção; <60% = estoque amplo.

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

## 3.6 Determinação do Nº total de unidades (v5.1+)

Toda vez que se atualiza ou cria entry no E_RAW (ou se processa tabela/book novo via comandos §5.1 ou §5.5), o "Nº total unidades" (col 7) e a "Origem total unid." (col 8) **devem** ser preenchidos seguindo a hierarquia abaixo. Aplicar do nível 1 até achar fonte; só descer ao próximo se o anterior não tem informação.

### Hierarquia obrigatória (7 níveis)

| # | Critério | Onde buscar | Origem (§4.7) |
|---|---|---|---|
| 1 | **Memorial registrado** | Rodapé legal de tabela / book técnico (matrícula + cartório) | `memorial` |
| 2 | **Book ou site oficial** declarando explícito ("X apartamentos") | Material institucional, página do empreend. no site da incorporadora | `book` ou `site_oficial` |
| 3 | **Descrição arquitetônica** (header/rodapé de tabela: "N torres × M pavtos × P aptos/andar") | Texto da própria tabela ou book técnico | `tabela_local_completa` ou `tabela_local_parcial` (ver detecção abaixo) |
| 4 | **Numeração dos aptos** | Aptos na tabela: max do range (ex: 1414 ⇒ 14 pavtos × 14 aptos). Atenção a gaps significativos | `tabela_local_parcial` |
| 5 | **Extração visual de imagens do book** | Plantas de implantação, mapas, fachadas com elevação completa | `book` (registrar nas obs: "extração visual da pág X") |
| 6 | **Informado manualmente pelo Rafael** | WhatsApp, reunião, ligação, declaração direta | `informado_manualmente` |
| 7 | **Nada se aplica** | Deixar `total = None`, origem = `N/A`. **NÃO INVENTAR.** | `N/A` |

### Detecção tabela completa vs parcial (regra automática)

- Se `# unidades listadas == total calculado pela descrição` → `tabela_local_completa` (típico pré-lançamento, todos disponíveis).
- Se `# listadas < total calculado` → `tabela_local_parcial` (algumas vendidas não aparecem na tabela).
- **Exceção Niágara:** formato agrupa N aptos por linha (ex: "POSIÇÃO LAGOA - APTOS 102, 104, 106 E 108"). **Não permite inferir vendidas.** Marcar `tabela_local_completa` + nota explícita nas observações sobre a limitação.

### Registro obrigatório nas Observações (col 25)

Sempre que origem ≠ `book` ou `memorial` (= total foi inferido por descrição/numeração/cross-check ou imagem), registrar **inline** nas observações:
- **Método:** descrição arquitetônica / numeração / extração visual / cross-check
- **Cálculo:** ex: `"192 = 13×14 + 14º pavto×10"`, ou `"41 inferido pela numeração max das casas (Casa 02 a Casa 41)"`
- **Confiança:** alta / média / baixa

Exemplo de registro: `"Total 192 = 13 pavtos×14 + 14º pavto×10 (extraído da descrição da tabela 28/04). Confiança: alta."`

### Validação automática (gerar_planilha.py)

Quando origem = `tabela_local_completa`, o script compara `Σ unidades em C_RAW` vs `total declarado`. Se diferir > **5%** (THRESHOLD_PCT), emite WARN no console:

```
⚠ VALIDAÇÃO §3.6: <empreend>: total=X mas Σ C_RAW=Y (Z% diff)
```

Não bloqueia geração. Operador deve revisar:
- Origem está errada? Pode ser `tabela_local_parcial`.
- C_RAW está incompleto? Faltam linhas.
- Tabela tem unidades fora de oferta (ex: cobertura especial não listada)?

### Checklist de aplicação ao processar tabela nova

Antes de marcar a entry como atualizada:

1. ☐ Identifiquei origem do total seguindo a hierarquia §3.6 (1→7)?
2. ☐ Marquei a origem na col 8?
3. ☐ Preenchi total na col 7 (ou deixei `None` se nível 7)?
4. ☐ Detectei se tabela é completa ou parcial?
5. ☐ Registrei método/cálculo/confiança nas Observações?
6. ☐ Rodei o script e validação §3.6 passou (ou WARN justificado)?

---

## 3.7 Determinação da Composição por Tipologia (v5.2+)

Quando se processa tabela/book novo de empreendimento (comandos §5.1, §5.5), além de preencher `Nº total unidades` (§3.6), deve-se popular a **aba Composição** (1 linha por empreend × tipologia) seguindo este processo.

### A. Hierarquia de fontes (5 níveis)

| # | Fonte | Origem (col 10 da aba Composição) |
|---|---|---|
| 1 | **Tabela detalhada em `/TABELA/`** com texto extraível (linhas apto-área-preço) | `tabela_local` |
| 2 | **Tabela em PDF imagem** → leitura via visão multimodal Claude (`pdftoppm` + Read tool) | `tabela_local_imagem` |
| 3 | **Book** com plantas/contagens declarando unidades por tipologia | `book` |
| 4 | **Informado manualmente** (Rafael, corretor, reunião) | `informado_manualmente` |
| 5 | **Nada se aplica** | NÃO criar entry em C_RAW. Empreend. fica sem composição (gap explícito do roadmap). |

### B. Workflow obrigatório de extração

1. **Identificar formato** da tabela/book → escolher parser correto (catálogo §3.7.1)
2. **Rodar parser** → lista de tuplas `(apto, area, ticket)`
3. **Validar não-duplicação** — algumas tabelas listam aptos em múltiplos planos de pagamento (ex: Renaissance Conceito tem SFH e FDC, ambas listam mesmas unidades). Deduplicar por nº do apto.
4. **Aplicar regras de tipologia:**
   - Se mono-tipologia (E_RAW col 14 tem 1 valor único): todas unidades vão pra essa categoria, ignora heurística por área
   - Se multi-tipologia (col 14 tem `;`): aplicar heurística §2.1 por área de cada unidade
   - Se tipologia "Lote" (loteamento): todas vão pra `Lote`
5. **Compor entries C_RAW**: 1 linha por (incorporadora, empreendimento, tipologia)
   - Áreas min/max = min/max das áreas das unidades dessa tipologia
   - Tickets min/max = min/max dos tickets
   - R$/m² médio = `Σ(ticket_unidade) / Σ(área_unidade)` (média ponderada)
6. **Registrar nas Observações** do empreendimento (col 25 do E_RAW): parser usado + data extração + confiança

### 3.7.1 Catálogo de parsers por incorporadora

Cada incorporadora tem layout próprio de tabela. Catálogo identificado em SLZ:

| Incorporadora | Formato típico | Empreend. canônico | Notas |
|---|---|---|---|
| **Delman** | `APTO PREÇO ÁREA ...` (com ou sem R$) | The View, Wave, Sky, SD7P, Landscape, Quartier 22, Azimuth | Pattern: `^\s*(\d{3,4})\s+(?:R\$\s*)?[\d\.]+,\d{2}\s+[\d,]+` |
| **Mota Machado** | `APTO VAGAS ÁREA ... VALOR_TOTAL` | Bossa, Entre Rios, Reserva SM, Al Mare | Último valor da linha = ticket total. Inclui parcelas intermediárias |
| **Treviso Vernazza** | `UNIDADE POSIÇÃO ÁREA ATO ... VALOR_TOTAL` | Vernazza Norte, Vernazza Sul | Prefix `N-` ou `S-` antes do número |
| **Treviso Altos** | `APTO VALOR SITUAÇÃO ÁREA VAGAS ATO` | Altos do São Francisco | Coluna SITUAÇÃO ("DISPONIVEL") em formato texto |
| **Monteplan** | `<PREFIX> APTO L INVEST` (áreas em rodapé "Torre X = Ym²") | Renaissance Conceito, Sanpaolo | **Atenção: tabelas SFH+FDC duplicam aptos** — deduplicar |
| **Castelucci** | `Casas X a Y / Casa N + TERRENO + R$ VALOR + ÁREA_CONSTRUÍDA` | Vila Coimbra | Range "Casas X a Y" expande pra (Y-X+1) unidades |
| **Niágara** | `POSIÇÃO X - APTOS A, B, C, D - N VAGAS  ÁREA  VALOR_VENDA` | ORO Ponta d'Areia | **1 linha = N aptos**. Tabela NÃO permite inferir vendidas (formato agrupa) |
| **Hiali** | `APTO ÁREA À VISTA SINAL ...` | Le Noir | Pattern simples |

Quando aparecer empreendimento de incorporadora não catalogada acima, **adicionar parser nova ao catálogo** ao invés de improvisar.

### C. Validações automáticas (gerar_planilha.py)

Implementadas em v9.3 — rodam antes de salvar a xlsx:

1. **Anti-duplicação:** se mesma `(incorporadora, empreendimento, tipologia)` aparece 2× em C_RAW → **ERROR** (não bloqueia geração mas registra alerta forte)
2. **Heurística vs Tipologia declarada:** se empreend é mono-tipologia em E_RAW (ex: Tipologia="4D") mas C_RAW tem categoria diferente (ex: 3D) → **WARN** com sugestão
3. **Cobertura:** se empreend tem pasta `/TABELA/*.pdf` arquivada mas **zero entries** em C_RAW → **WARN** ("processar este lote pra fechar gap")

### D. Registro nas Observações

Sempre que extrair Composição, anexar nas obs do empreend (col 25):
- **Parser usado:** ex: "parser Delman", "parser Mota Machado"
- **Data:** ex: "extração 02/05/2026"
- **Tipo de fonte:** ex: "tabela 04/2026", "pdf imagem via visão", "book pág 15"
- **Confiança:** alta / média / baixa

Exemplo: `"Composição extraída via parser Delman da tabela 28/04 v3 — 93 unid em 4 tipologias. Confiança: alta."`

### Checklist de aplicação ao popular Composição

1. ☐ Identifiquei origem da composição seguindo §3.7.A?
2. ☐ Escolhi parser correto do catálogo §3.7.1?
3. ☐ Deduplicei por nº de apto (caso Monteplan SFH+FDC)?
4. ☐ Apliquei heurística OU mono-tipologia conforme §3.7.B item 4?
5. ☐ Calculei R$/m² médio como média ponderada?
6. ☐ Registrei parser/data/confiança nas Observações?
7. ☐ Rodei script e as 3 validações §3.7.C passaram?

---

## 4. Enumerações fixas

### 4.1 Incorporadoras monitoradas (16 — lista fechada)
Mota Machado, Berg Engenharia, Alfa Engenharia, Lua Nova, Delman, Treviso, Ergus, Monteplan, Franere, Canopus, Niágara, MB Engenharia, Sá Cavalcante, **Castelucci**, **Hiali**, **DOM Incorporação**.

> **v2.0 (25/04/2026):** +Hiali (Le Noir), +DOM Incorporação (própria — para benchmarking interno: Dom Lucas, Dom José, e parcerias com MB em Dom Antônio + Edifício Dom Ricardo).
> Adicionar/remover: só com aprovação explícita do Rafael; atualizar este arquivo.

### 4.2 Segmento (por R$/m² médio calculado — São Luís, 2026)
| Segmento | Faixa R$/m² | Observação |
|---|---|---|
| Popular | < R$ 6.000 | MCMV, faixas 2-3 |
| Médio | R$ 6.000 – R$ 8.000 | |
| Médio-alto | R$ 8.000 – R$ 10.000 | Casas 100-155m² horizontais (Eldorado, Cohatrac) |
| Alto | R$ 10.000 – R$ 15.000 | Faixa principal SLZ — Calhau/Ponta d'Areia |
| Luxo | > R$ 15.000 | Bossa, The View, Vernazza, Giardino, Wave, Sky, Azimuth, Quartier 22 |

⚠️ **v2.2 (27/04/2026):** faixas recalibradas para refletir o mercado real de SLZ. Antes (v2.0): Médio 6-9k, Médio-alto 9-13k, Alto 13-18k, Luxo >18k. Detectado que muitos empreend. de alto padrão (R$ 14-17k) ficavam em Alto pela classificação antiga, contradizendo o posicionamento de marca. Revisar em cada update anual ou se o mercado mover.

### 4.3 ~~Status~~ — REMOVIDO em v3.0
> A coluna Status foi removida na v3.0 (27/04/2026). Justificativa: classificação ambígua entre tempo de venda e estoque, parcialmente derivada de outros campos. O filtro "ativo no ciclo" foi também eliminado — Panorama mostra todos os empreendimentos mapeados sem filtro de fase. Análise de absorção segue via % Vendido (col 18).

### 4.4 Origens (valores permitidos)
**Origem preços:** `tabela_local` | `site_oficial` | `agregador` | `imprensa` | `estimativa`
**Origem estoque:** `tabela_local` | `site_oficial` | `agregador` | `corretor` | `estimativa`
**Origem lançamento:** `book` | `release` | `treinamento_corretor` | `site_oficial` | `imprensa` | `estimativa_T-36`

### 4.5 Tipo (3 categorias)
| Tipo | Definição | Exemplos |
|---|---|---|
| Vertical | Edifício multifamiliar (apartamentos) | The View, Bossa, Quartier 22 |
| Horizontal | Condomínio de casas, sobrados (unidades construídas) | Dom Lucas, Dom José, Dom Antônio |
| Loteamento | Loteamento ou condomínio de terrenos (sem unidades construídas) | Golden Green Beach, Villagio Treviso |

> **v3.4 (27/04/2026):** Tipo "Misto" removido (não havia entries usando) e **Loteamento** formalizado como 3ª categoria — antes ficava equivocadamente em Horizontal. Diferenciação importante: R$/m² em Loteamento é **m² de terreno** (não construído), não comparável com Vertical/Horizontal. Análise por Tipo no dashboard usa essa distinção.

⚠️ Esta classificação é fundamental para análise de oportunidades — bairros como Eldorado/Cohatrac concentram horizontal, enquanto Ponta d'Areia/Calhau dominam vertical alto.

### 4.6 Tipologia (dormitórios) — enum padronizado v3.1
| Código | Significado |
|---|---|
| Studio | Studio (1 ambiente, sem dormitório separado) |
| 1D | 1 dormitório (quarto-sala / 1 suíte) |
| 2D | 2 dormitórios (suítes ou comuns — não distinguimos) |
| 3D | 3 dormitórios |
| 4D | 4 dormitórios |
| Lote | Loteamento / terreno em condomínio (sem dormitório, ainda categoria válida) |
| — | Sem dado (precisa book/tabela) |

**Regras:**
- Múltiplas tipologias num mesmo empreendimento: separar por `; ` (ex: `Studio; 1D; 2D`)
- **Suíte conta como dormitório** — não distinguimos suíte vs comum no código curto. Detalhes (master, closet, banheiro duplo, etc.) ficam nas **Observações** com prefixo `Tipologia detalhada: ...`
- **HTML mostra o código curto** + ícone ℹ que abre tooltip com a descrição detalhada (extraída das Observações)

⚠️ **v3.1 (27/04/2026):** Antes da v3.1, col 13 era texto livre ("Tipologia (dorms)") com formato heterogêneo. Agora é enum estruturado. Valores antigos foram migrados para Observações com prefixo `Tipologia detalhada:` para preservar info qualitativa.

### 4.7 Origem total unidades (v9.0+) — NOVO

Coluna 8 da aba Empreendimentos. Indica a origem da informação do "Nº total unidades" (col 7).

| Valor | Significado |
|---|---|
| `tabela_local_completa` | Tabela mostra TODAS as unidades (vendidas + disponíveis). Soma da Composição **deve** bater com o total. |
| `tabela_local_parcial` | Tabela mostra SÓ unidades disponíveis. Total veio de outra fonte. Diferença = unidades vendidas. |
| `book` | Total declarado no material institucional/book (inclui extração visual de imagens — registrar nas obs) |
| `memorial` | Memorial de incorporação |
| `site_oficial` | Site da incorporadora |
| `treinamento_corretor` | Corretor passou |
| `imprensa` | Release ou notícia |
| `informado_manualmente` | **v9.2+**: total fornecido manualmente pelo Rafael (WhatsApp, reunião, ligação, etc) |
| `N/A` | Sem dado — NÃO inventar |

> **v9.2 (02/05/2026):** removido valor `estimativa` do enum. A política agora é **não inventar totais**: se nenhum nível da hierarquia §3.6 se aplica, marcar `N/A` com total `None`.

**Validação automática:** quando origem = `tabela_local_completa`, o `gerar_planilha.py` compara `Nº total unidades` (col 7) com `Σ unidades em C_RAW` para o empreend. Se diferir > 5%, log WARN no stdout (não bloqueia).

**Por que existe:** quando a tabela da incorporadora lista 93 unidades disponíveis (caso The View), elas representam **só os disponíveis**, não o total. Sem essa coluna, a soma da Composição era ambígua. v9.0 formaliza isso. Empreendimentos com `tabela_local_parcial` requerem busca complementar (book/site/memorial) para fechar o total.

---

## 5. Comandos padronizados (5 gatilhos)

### 5.1 "atualiza o estudo"
Passo-a-passo obrigatório:
1. Ler este PADRAO.md primeiro
2. **Executar §0.3 — sanity check de drift** (parar se script ≠ última xlsx)
3. Varrer `/01.Inteligência Mercado/XX_*/` por arquivos novos
4. Para cada uma das 16 incorporadoras (excl. DOM Incorporação que é nossa, mas inclui-la para tracking interno): pesquisa web obrigatória nesta ordem:
   a. **Instagram oficial** (últimos ~20 posts — buscar lançamentos, tabelas, teasers)
   b. **Site oficial** (empreendimentos atuais, atualizações de tabela)
   c. 1 portal agregador (Ziag ou MGF)
   d. 1 busca de notícias (Imirante/Diego Emir)
5. Aplicar regras §3 para recalcular campos calculados
6. Reclassificar Segmento (§4.2) com base no R$/m² novo
7. Gerar planilha chamando `gerar_planilha.py`
8. Executar `publish.sh` (regera HTML + commita pacote)
9. Escrever mini-changelog no final do chat (o que mudou, novas linhas, alertas)

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
   - Mudanças de Tipo ou Segmento
4. Retornar bullet list (sem planilha nova)

### 5.4 "oportunidades"
1. Ler planilha atual
2. Cruzar dados para encontrar:
   - Gap segmento × bairro (ex: "nenhum luxo no Renascença")
   - Gap **Tipo** × bairro (ex: "nenhum horizontal no Calhau")
   - Faixas de ticket pouco disputadas
   - Tipologias ausentes (ex: "nenhum 4Q no Calhau")
   - Bairros com 0-1 concorrente
3. Retornar lista priorizada de 5 oportunidades com: descrição, racional quantitativo, movimento DOM sugerido

### 5.5 "adicionei arquivos de [incorporadora]"
1. **Executar §0.3 — sanity check de drift**
2. Ler SÓ os arquivos novos na pasta indicada
3. Atualizar SÓ as linhas da incorporadora citada
4. Regerar planilha + HTML via `publish.sh` (versão minor bumpada, ex: v5.0 → v5.1)
5. Reportar diff daquela incorporadora

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
- `X` (major): mudança estrutural — nova coluna, nova aba, novo enum, mudança em §0–§4
- `Y` (minor): nova carga de dados, correções, novos empreendimentos, sem mudança estrutural

Arquivos antigos mantidos (histórico). Ao regerar, criar novo vY+1, não sobrescrever.

---

## 8. Estado e versionamento (git)

### 8.1 Política de tracking
| Arquivo | No git? | Motivo |
|---|---|---|
| `_PADRAO_FASE_1/gerar_planilha.py` | ✅ Sim | Source-of-truth |
| `_PADRAO_FASE_1/PADRAO.md` | ✅ Sim | Contrato |
| `build_panorama.py` | ✅ Sim | Gerador HTML |
| `publish.sh` | ✅ Sim | Workflow |
| `Planilha_Mestre_Panorama_vX.Y.xlsx` | ✅ Sim (atual) | **Mudança v2.0** — antes era gitignored, agora trackeado para drift detection |
| `index.html` | ✅ Sim | Output publicado (GitHub Pages) |
| Books, tabelas PDF nas pastas de incorporadoras | ❌ Não | Material de origem, fica local |

### 8.2 Mudança de política (v2.0)
A v1.x do PADRAO mantinha `.xlsx` no `.gitignore` ("planilha fica local"). **Reverte-se essa decisão** porque:
1. O dado já está commitado dentro do `E_RAW` no `gerar_planilha.py` — não há ganho de privacidade em ocultar a `.xlsx`.
2. Sem `.xlsx` no git, sessões diferentes não conseguem detectar drift entre script-fonte e output materializado.
3. O incidente da v4.16→v4.17 (perda de 12 empreendimentos) só foi detectável porque a `.xlsx` órfã sobreviveu localmente — em ambiente menos sortudo, teria sido perda silenciosa.

### 8.3 Mensagens de commit
Formato obrigatório: `vX.Y — <descrição curta de 1 linha>`.
Exemplos válidos: `v4.18 — Reconciliação +The View +Hiali`, `v5.0 — Coluna Tipo formalizada`.
Exemplos a EVITAR: `update`, `1`, `2`, `m`, `datas`.

### 8.4 Workflow de mudança
1. Toda alteração começa editando `gerar_planilha.py` (E_RAW ou I_META).
2. Rodar `publish.sh` — ele regenera xlsx + html, commita os 3 juntos, e dá push.
3. **Nunca** editar `.xlsx` ou `index.html` direto.
4. Para mudanças estruturais (nova coluna, novo enum), atualizar este PADRAO.md ANTES de mexer no script.

---

*Qualquer mudança neste padrão requer aprovação explícita do Rafael.
Claude não altera este arquivo por iniciativa própria.*
