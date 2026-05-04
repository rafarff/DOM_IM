# PADRÃO FASE 1 — Inteligência de Mercado DOM
**Versão:** 7.0 (atualizada em 03/05/2026)
**Status:** 🟢 APROVADO pelo Rafael

> **v7.0 — granularidade de planta em §3.7 (Composição):** a aba Composição passa a ter **1 linha por (empreend × tipologia × planta)** ao invés de (empreend × tipologia). Razão: ticket dita absorção mais do que tipologia — uma planta de 100m² 3D e uma de 125m² 3D têm públicos-alvo muito distintos (R$ 400k de diferença de ticket = mudança de público-alvo). Schema da aba sobe de 11 → **12 colunas** (entram: `Planta` e `Área (m²)` única + `Total planta`; sai: `Área mín/máx`). **Invariante de 3 níveis:** `Σ Total planta = Total tipologia` ⊕ `Σ Total tipologia = E_RAW.Total`. §3.6 (Total) permanece intocada — continua sendo a âncora ortogonal a §3.7. Hierarquia §3.7.A mantém 5 níveis; sub-regras nível 5 emitem 1 planta por tipologia (não inventa plantas). Validação nova §3.7.C.6: `Σ Total planta = Total tipologia` por (empreend × tipologia). Label da planta usa nome do book quando declarado (Botticelli, Tipo A, Loft 68); senão a área serve de identificador.

> **v6.2 — virada estrutural §3.7:** Composição vira **obrigatória** com **invariante Σ C_RAW = E_RAW.Total** pra todo empreend. com Total apurado. Hierarquia §3.7 ganha **nível 5 estimativa_distribuição** (sub-regras 5.1–5.4). Princípio inviolável: §3.6 (Total) e §3.7 (Composição) são **processos ortogonais e sequenciais** — Total é a âncora; Composição se conforma ao Total, **nunca o contrário**. Reconciliação automática: estimativas (nível 5) se ajustam pro Total fechar; fontes fortes (níveis 1–4) que não fechem com Total geram WARN orientando a continuar buscando Composição (Total não muda). Multi-torre: regra (A) consolidação — torres viram entries únicas (Vernazza, Giardino).

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
2.1. Dicionário de dados — aba Composição (12 colunas, v7.0+)
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
| Composição (v7.0+) | 1 linha por empreend × tipologia × planta | Visão analítica granular (preço médio por planta REAL — ticket dita absorção, não tipologia) |
| Incorporadoras | 1 linha por incorp. | Agregados por incorp. |

A aba Empreendimentos é a fonte primária. A aba Composição enriquece com detalhe quando a tabela do empreendimento foi processada. Nem todo empreend. tem entry em Composição (gap esperado é parte do roadmap, não inconsistência).

## 2.1. Aba Composição — 12 colunas (v7.0+)

| # | Campo | Tipo | Regra |
|---|---|---|---|
| 1 | Incorporadora | Enum §4.1 | Mesmo nome usado na aba Empreendimentos |
| 2 | Empreendimento | Texto | Mesmo nome usado na aba Empreendimentos |
| 3 | Tipologia | Enum §4.6 | Studio / 1D / 2D / 3D / 4D / Lote — coluna agrupadora (GROUP BY natural) |
| 4 | **Planta** | Texto | Label do book quando declarado ("Botticelli", "Tipo A", "Loft 68"); senão vazio (área serve de identificador) |
| 5 | **Área (m²)** | Decimal | Valor único da planta (não range). Plantas espelho mesma área = mesma entry |
| 6 | Total tipologia | Calculado runtime | Σ Total planta dessa tipologia (gold; visualmente destacado) |
| 7 | **Total planta** | Inteiro | Quantidade total de unidades dessa planta no empreend. (Σ por tipologia = col 6) |
| 8 | Disponíveis | Inteiro | Estoque dessa planta (Σ por tipologia ≤ Total tip) |
| 9 | Ticket mín (R$) | Moeda | Mantém range — variação por andar/posição/vista é legítima dentro de uma planta |
| 10 | Ticket máx (R$) | Moeda | idem |
| 11 | R$/m² médio | Calculado | ticket_médio / área (área única simplifica) |
| 12 | Origem | Enum §3.7.A | `tabela_local`, `tabela_local_imagem`, `book`, `informado_manualmente`, `estimativa_distribuição_*` |

**Regra de inferência tipologia × área (SLZ-padrão):** quando tabela não declara explicitamente a tipologia por unidade, usar:
- < 40m² → Studio
- 40-55m² → 1D
- 55-75m² → 2D
- 75-95m² → 3D
- ≥ 95m² → 4D

Em casos especiais (mono-tipologia declarada, áreas em fronteira), classificação manual prevalece.

**Bucketização em plantas (v7.0):** depois de aplicar tipologia, agrupar unidades por área arredondada (1 casa decimal). Cada bucket = 1 planta. Quando o book/tabela declara nome explícito da planta (Botticelli, Tipo A, Coluna 1), usar como label; senão o label fica vazio e a área é o identificador. Plantas com mesma tipologia + mesma área dentro do mesmo empreend. = mesma entry (soma das unidades).

**O que muda no dashboard com a aba Composição:** a Seção 3 (Análise por Tipologia) faz GROUP BY tipologia natural. A Seção Bairro ganha bubble (bairro × tipologia × planta), expondo absorção por ticket real (3D 100m² em Calhau vs 3D 125m² em Calhau). Limitação: cobertura depende de quais empreend. tiveram tabela processada (roadmap dos Lotes).

## 2bis. Aba Incorporadoras — 15 colunas (v7.0+: aba DERIVADA)

> **v11.2 (R2 — 03/05/2026):** aba Incorporadoras passa a ser **100% derivada em runtime**. Apenas 3 campos são metadados estáveis (vão pra `incorporadoras_meta.yaml`). Os 11 demais campos por incorporadora são GROUP BY na aba Empreendimentos. Aba xlsx continua idêntica visualmente — só a fonte mudou.

| # | Campo | Tipo | Origem v11.2 |
|---|---|---|---|
| 1 | Incorporadora | Enum §4.1 | ID — chave do agrupamento |
| 2 | Nº empreend. mapeados | Inteiro | **DERIVADO** — `COUNT(*) WHERE Inc=X` |
| 3 | VGV total estimado (R$) | Soma §3.2 | **DERIVADO** — `SUM(VGV)` |
| 4 | VGV lançado 2024 | Subconjunto §3.4 | **DERIVADO** — `SUM(VGV) WHERE year_lancamento=2024` |
| 5 | VGV lançado 2025 | Subconjunto §3.4 | **DERIVADO** |
| 6 | VGV lançado 2026 | Subconjunto §3.4 | **DERIVADO** |
| 7 | Segmentos de atuação | Lista §4.2 | **DERIVADO** — `DISTINCT segmento`, ordenado |
| 8 | Bairros de atuação | Lista de bairros | **DERIVADO** — `DISTINCT bairro` |
| 9 | Ticket médio carteira | Média simples | **DERIVADO** — `AVG((tk_min+tk_max)/2)` |
| 10 | R$/m² médio carteira | Média | **DERIVADO** — `AVG(rs_m2)` |
| 11 | % carteira com fonte local | `empreend_com_A / total × 100` | **DERIVADO** — pelos campos Origem do E_RAW |
| 12 | Site oficial | URL | **METADADO ESTÁVEL** — `incorporadoras_meta.yaml` |
| 13 | Instagram | `@handle` ou URL | **METADADO ESTÁVEL** — idem |
| 14 | Posicionamento de marca | Texto curto | **METADADO ESTÁVEL** — idem |
| 15 | Última atualização | DD/MM/AAAA | Global — `DATE_STR` do script |

**Como editar metadados de uma incorporadora (v11.2+):** abrir `_PADRAO_FASE_1/incorporadoras_meta.yaml`, editar os 3 campos (`site`, `instagram`, `posicionamento`). Não há mais I_META no script. Os 11 derivados se atualizam automaticamente quando E_RAW muda.

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

## 3.7.0 U_RAW (Unidades) — fonte primária do sistema (v11.3+, R3)

> **Princípio (Rafael 03/05/2026):** "se fosse começar do zero faria por unidade". A **unidade individual** (apartamento) é o **átomo natural** do sistema. Quando a fonte permite (tabela_local, tabela_local_imagem), a Composição (§3.7) **deriva** automaticamente do U_RAW via bucketização por planta. Aba "Unidades" na xlsx expõe esse átomo.

### Schema U_RAW (9 colunas)

1 linha por (incorporadora, empreendimento, apto):

| # | Campo | Tipo | Notas |
|---|---|---|---|
| 1 | Incorporadora | enum §4.1 | |
| 2 | Empreendimento | str | |
| 3 | Apto | str | "402", "1505", "Casa 12" — identificador |
| 4 | Tipologia | enum §4.6 | Studio/1D/2D/3D/4D/Lote |
| 5 | Planta | str | label do book quando declarado (Botticelli, Coluna 01); senão vazio |
| 6 | Área (m²) | float | área única em m² |
| 7 | Status | str | 'disponível' / 'vendido' / 'reservado' (None se tabela não diferencia) |
| 8 | Ticket (R$) | float | preço à vista (ou cheio se à vista N/A) |
| 9 | Origem | enum §3.7.A | tabela_local, tabela_local_imagem, etc. |

Campos **Andar / Posição / Data_status** ficam fora do MVP — entram quando análises pedirem.

### Cobertura U_RAW vs C_RAW (híbrido)

- **Empreend. com origem nível 1-2** (tabela_local / tabela_local_imagem): viver em `unidades/<inc>__<emp>.yaml`. Composição é **derivada runtime** via `compute_c_raw_from_u_raw()`.
- **Empreend. com origem nível 3-5** (book / informado_manualmente / estimativa): continua em `composicao/<inc>__<emp>.yaml` direto, agregado por planta. Não há info por unidade individual nessas fontes.
- **Validação:** entries derivadas de U_RAW e entries lidas de composicao/ não podem coexistir pro mesmo (inc, emp). Script garante isso (filtra composicao/ excluindo empreend. presentes em U_RAW).

### Aba Unidades na xlsx (v11.3+)

Nova aba "Unidades" (4ª aba) renderiza U_RAW completo. Filtros nativos do Excel permitem:
- Filtrar por bairro/incorporadora/tipologia/planta
- Sortear por área/ticket
- Status colorido (verde = disponível, laranja = reservado, vermelho = vendido)
- Cross-check de C_RAW: `Σ U_RAW.disp por (inc, emp, tip, planta) == C_RAW.Disp` (invariante derivada)

### Roadmap de cobertura

- **Lote 1 v11.3 (entregue):** 6 empreend. / 212 unidades. Parsers Delman/Treviso Altos/Alfa.
- **Lote 2 (próximo):** ~17 empreend. com tabela texto restantes — Wave, Quartier 22, Sky, Azimuth (Delman); Bossa, Al Mare, Entre Rios, Reserva SM (Mota Machado); Vernazza N, Vernazza S (Treviso); Renaissance, Sanpaolo, Novo Anil (Monteplan); ORO (Niágara); Le Noir (Hiali); Vila Coimbra (Castelucci); Monte Meru (Berg).
- **Lote 3 (visão imagem):** Zion, Dom Lucas, Dom José (3 empreend. com tabela em PDF imagem — exige re-aplicação de visão multimodal).
- **Total alcançável:** ~26 empreend. de 44 da carteira (59% — limitado por disponibilidade de tabela detalhada).

---

## 3.7 Determinação da Composição por Tipologia × Planta (v7.0 — granularidade fina)

> **Princípio inviolável:** §3.6 (Total) e §3.7 (Composição) são processos **ortogonais e sequenciais**. Total é a âncora. Composição se conforma ao Total, **nunca o contrário**. Empreendimentos sem Total apurado por §3.6 entram em `pendencias_TOTAL.md` antes de qualquer processamento de Composição.

### Invariante (v7.0 — hierarquia de 3 níveis, obrigatória)

> Para todo empreendimento com `Total Unidades` preenchido em E_RAW:
> 1. `Σ C_RAW.Total_planta agrupado por (inc, emp, tip) = Total tipologia` (validação §3.7.C.6, NOVA v7.0)
> 2. `Σ Total tipologia agrupado por (inc, emp) = E_RAW.Total` (validação §3.7.C.4, mantida de v6.2)
>
> Reconciliação automática (mantém comportamento v6.2):
> - Se Composição estiver em **níveis 1–4** (fonte real) e Σ ≠ Total → **WARN** orientando "continuar buscando Composição" (Total não se mexe).
> - Se Composição estiver em **nível 5** (estimativa) e Σ ≠ Total → estimativa **se ajusta automaticamente** pra fechar com Total (sobra/déficit é redistribuído na tipologia majoritária; nível 5 sempre emite 1 planta por tipologia, então o ajuste é trivial).
> - Total nunca é alterado por reconciliação. Se Total estiver errado, isso é problema de §3.6, não de §3.7.

Quando se processa empreendimento (comandos §5.1, §5.5), depois de preencher `Total Unidades` (§3.6), deve-se popular a **aba Composição** (1 linha por empreend × tipologia) seguindo este processo.

### A. Hierarquia de fontes (5 níveis — v6.2)

| # | Fonte | Origem (col 12 da aba Composição) |
|---|---|---|
| 1 | **Tabela detalhada em `/TABELA/`** com texto extraível (linhas apto-área-preço) | `tabela_local` |
| 2 | **Tabela em PDF imagem** → leitura via visão multimodal Claude (`pdftoppm` + Read tool) | `tabela_local_imagem` |
| 3 | **Book** com plantas/contagens declarando unidades por tipologia | `book` |
| 4 | **Informado manualmente** (Rafael, corretor, reunião) | `informado_manualmente` |
| 5 | **Estimativa por distribuição** — quando temos Total+Tipologia em E_RAW mas nenhuma fonte detalhada (sub-regras 5.1–5.4) | `estimativa_distribuição` (com sufixo de sub-regra) |

**v6.2:** o nível 5 substitui o antigo "nada se aplica". Composição vira **obrigatória** sempre que Total estiver apurado. A estimativa carrega **flag visual** no dashboard (alpha reduzido / borda tracejada) — você nunca confunde com dado real.

### A.1 Sub-regras do nível 5 (estimativa_distribuição) — v6.2

**5.1 — Mono-tipologia declarada** (Tipologia em E_RAW tem 1 valor único)
- 1 entry C_RAW: tipologia única, unidades = Total
- Área = média declarada em E_RAW (`(area_min+area_max)/2`); se vazia, usar **mediana da carteira** pra essa tipologia (calculada em runtime de C_RAW existente)
- Origem: `estimativa_distribuição_mono`
- Ex: Quartier 22 (Tipologia="3D", Total=30) → 1 entry: 30 unid 3D, área 99m²

**5.2 — Multi-tipologia COM áreas declaradas** (Tipologia="2D; 3D" e área min/max preenchidos em E_RAW)
- Distribuição: **uniforme entre tipologias** (50/50 se 2 tipologias, 33/33/33 se 3, etc. — sobra cai na 1ª)
- Áreas: **menor área declarada** → tipologia menor; **maior área declarada** → tipologia maior; intermediárias = mediana da carteira
- Origem: `estimativa_distribuição_multi_com_area`
- Ex: Ilha Parque (Tipologia="2D; 3D", Total=120, área 64–85) → 60u 2D 64m² + 60u 3D 85m²

**5.3 — Multi-tipologia SEM áreas** (Tipologia="Studio; 1D; 2D" e área não declarada)
- Distribuição: **uniforme**
- Áreas: **mediana da carteira** por tipologia (calculada em runtime — NUNCA hardcoded; ver tabela em runtime no log do script)
- Origem: `estimativa_distribuição_multi_sem_area`

**5.4 — Sem tipologia** (Tipologia="—" mas Total preenchido)
- 1 entry C_RAW com tipologia="—", unidades = Total, área = não preenchida
- Análises por tipologia **ignoram** entries "—"; análises agregadas (Total, VGV, % vendido) usam normalmente
- Origem: `estimativa_distribuição_sem_tipologia`
- Ex: Cond. Prime Cohama (Total=22, Tipologia="—") → 22 unid "—"

**Bloqueado** (não cabe em nenhuma sub-regra): empreend. **sem Total apurado** entram em `pendencias_TOTAL.md`. NÃO criar C_RAW especulativo.

### B. Workflow obrigatório de extração (v7.0)

1. **Verificar Total apurado** (§3.6 já aplicado) — se não, parar e ir pra §3.6 primeiro
2. **Tentar fonte primária** (níveis 1–4): identificar formato da tabela/book → escolher parser correto (catálogo §3.7.1)
3. **Rodar parser** → lista de tuplas `(apto, area, ticket)`
4. **Validar não-duplicação** — algumas tabelas listam aptos em múltiplos planos de pagamento (ex: Renaissance Conceito tem SFH e FDC, ambas listam mesmas unidades). Deduplicar por nº do apto.
5. **Aplicar regras de tipologia:**
   - Se mono-tipologia (E_RAW col 14 tem 1 valor único): todas unidades vão pra essa categoria, ignora heurística por área
   - Se multi-tipologia (col 14 tem `;`): aplicar heurística §2.1 por área de cada unidade
   - Se tipologia "Lote" (loteamento): todas vão pra `Lote`
6. **(NOVO v7.0) Bucketizar em plantas:** `bucketizar_plantas([(apto, area, ticket), ...])` agrupa por área arredondada (1 casa decimal). Cada bucket = 1 planta candidata. Saída: `[(label, area, n_unid_disp, ticket_min, ticket_max), ...]`. Label preenchido só se book/tabela declarou explicitamente (Botticelli, Tipo A, Coluna 1); senão vazio.
7. **Compor entries C_RAW**: 1 linha por (incorporadora, empreendimento, tipologia, planta).
   - `Total planta` = quantidade total de unidades dessa planta (vendidas + disponíveis quando inferível; senão = disp)
   - `Disponíveis` = unidades em estoque (inferidas da tabela)
   - `Área` = valor único da planta
   - `Ticket min/max` = mantém range (variação por andar/posição é legítima)
   - `R$/m² médio` = ticket_médio / área (área única simplifica)
8. **Reconciliação invariante 3 níveis:**
   - `Σ Total planta agrupado por tip = Total tipologia` (validação §3.7.C.6)
   - `Σ Total tipologia = E_RAW.Total` (validação §3.7.C.4 mantida)
   - Se não bater e fonte é nível 1–4, WARN "buscar mais Composição"; **não cria entry estimativa em paralelo**.
9. **Fallback nível 5** (apenas se nenhuma fonte 1–4 está disponível): aplicar sub-regra 5.1/5.2/5.3/5.4 conforme árvore de decisão. v7.0 emite **1 planta por tipologia** (não inventa plantas) — label vazio, área = média declarada ou mediana da carteira. A estimativa **automaticamente fecha com Total** (invariante).
10. **Registrar nas Observações** do empreendimento (col 25 do E_RAW): origem usada (nível e sub-regra) + data extração + confiança + plantas detectadas (ex: "Renaissance: 2 plantas — Botticelli 82m² 3D 15u + Leonardo 110m² 4D 7u")

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
| **Alfa Engenharia** *(v10.1+)* | `COLUNA(S) NN - YYY,YYm²` (header) + `<unidade> <vagas> <valores...> <ticket>` (linhas) | Giardino Fiore, Giardino Luce | Área no header de cada bloco de coluna |
| **Berg Engenharia** *(v10.1+)* | `APARTAMENTO DE Y,YYM2 + TIPO N + <apto> <valores...> <preço total>` | Monte Meru | Cada bloco de tipo (TIPO 3, TIPO 4) tem header próprio |
| **Monteplan Anil** *(v10.1+)* | `<bloco>-<apto> L INVEST` (idêntico Sanpaolo, áreas no rodapé) | Residencial Novo Anil | Múltiplos blocos (A1-B4) com áreas uniformes 53,94m² |

Quando aparecer empreendimento de incorporadora não catalogada acima, **adicionar parser nova ao catálogo** ao invés de improvisar.

### C. Validações automáticas (gerar_planilha.py) — v7.0 reforçadas

Rodam antes de salvar a xlsx:

1. **Anti-duplicação:** se mesma `(incorporadora, empreendimento, tipologia, planta)` aparece 2× em C_RAW → **ERROR** (não bloqueia geração mas registra alerta forte). v7.0: chave inclui planta — duas plantas com mesma área e mesmo label = mesma entry.
2. **Heurística vs Tipologia declarada:** se empreend é mono-tipologia em E_RAW (ex: Tipologia="4D") mas C_RAW tem categoria diferente (ex: 3D) → **WARN** com sugestão
3. **Cobertura:** se empreend tem pasta `/TABELA/*.pdf` arquivada mas **zero entries** em C_RAW → **WARN** ("processar este lote pra fechar gap")
4. **(v6.2) Invariante Σ Total tipologia = E_RAW.Total:** para todo empreend. com Total apurado, verificar a soma. Resultado:
   - Σ = Total exato → ✓ fechado
   - Σ ≠ Total e origem **forte** (níveis 1–4) → **WARN**: "Composição incompleta. Buscar mais fonte (book/tabela). Total NÃO se ajusta."
   - Σ ≠ Total e origem **estimativa** (nível 5) → ajuste automático: redistribuição na tipologia majoritária pra fechar
   - Σ ≠ Total e origens **mistas** (ex: parte tabela_local + parte estimativa) → trata estimativa como buffer pra fechar; fontes fortes ficam intactas
5. **(v6.2) Cobertura obrigatória:** todo empreend. com Total apurado **deve** ter C_RAW (mínimo 1 entry, mesmo "—"). Se faltar → **ERROR** "Composição obrigatória v7.0".
6. **(NOVA v7.0) Invariante Σ Total planta = Total tipologia:** para cada chave `(inc, emp, tip)` em C_RAW, verificar `Σ Total_planta = Total tipologia` (computado pela §3.7.C.4 mesma chave). Resultado:
   - Σ = Total tipologia exato → ✓ fechado
   - Σ ≠ Total tipologia → **WARN**: "Plantas não fecham com tipologia. Verificar bucketização ou completar plantas faltantes." Estimativas nível 5 (1 planta por tip) sempre fecham por construção.

### D. Multi-torre (consolidação — v6.2 regra A)

Empreendimentos lançados como **múltiplas torres da mesma marca/lançamento comercial** (ex: Vernazza Torre Norte + Sul, Giardino Residenza Torre Fiore + Luce) são consolidados em **1 entry única** em E_RAW e C_RAW.

**Critérios de consolidação:**
- Mesma incorporadora
- Mesmo bairro / mesmo endereço / mesmo segmento
- Nome compartilha "stem" (ex: "Vernazza", "Giardino Residenza")
- Lançamento comercial percebido como unitário (não 2 lançamentos distintos)

**Procedimento:**
- Empreendimento (nome): usar o stem (ex: "Vernazza Residenza" no lugar de "Vernazza Torre Norte")
- Total: soma das torres
- Composição: união (mesma tipologia entre torres → soma; tipologias distintas → entries separadas)
- Endereço, Bairro, Segmento, Tipo: idênticos entre torres (validar). Se divergem, NÃO consolidar.
- Mês lançamento: o **mais antigo** das torres
- Mês entrega: o **mais tardio** das torres
- Áreas/tickets: min/max combinado
- Observações: registrar consolidação ("Consolidado de Torre Norte 120u + Torre Sul 60u — v6.2")

**O que NÃO consolidar:**
- Empreend. distintos da mesma incorporadora em bairros diferentes (ex: Berg "Mount Solaro" + "Monte Meru" são lançamentos separados)
- Empreend. com mesmo nome-base mas marcas comerciais diferentes (ex: Renaissance Conceito SFH + FDC eram **planos de pagamento** da mesma torre, não torres distintas — esses já foram tratados em v9.2 como entry única)

### D. Registro nas Observações

Sempre que extrair Composição, anexar nas obs do empreend (col 25):
- **Parser usado:** ex: "parser Delman", "parser Mota Machado"
- **Data:** ex: "extração 02/05/2026"
- **Tipo de fonte:** ex: "tabela 04/2026", "pdf imagem via visão", "book pág 15"
- **Confiança:** alta / média / baixa

Exemplo: `"Composição extraída via parser Delman da tabela 28/04 v3 — 93 unid em 4 tipologias. Confiança: alta."`

### Checklist de aplicação ao popular Composição (v7.0)

1. ☐ Identifiquei origem da composição seguindo §3.7.A?
2. ☐ Escolhi parser correto do catálogo §3.7.1?
3. ☐ Deduplicei por nº de apto (caso Monteplan SFH+FDC)?
4. ☐ Apliquei heurística OU mono-tipologia conforme §3.7.B item 5?
5. ☐ **(v7.0) Bucketizei em plantas** por área arredondada (§3.7.B item 6)?
6. ☐ **(v7.0) Preenchi label de planta** quando book/tabela declara nome (Botticelli, Tipo A, Coluna N)?
7. ☐ **(v7.0) Total planta** preenchido por planta + Disp separado de Total planta?
8. ☐ Calculei R$/m² médio como ticket_médio / área?
9. ☐ Registrei parser/data/confiança/plantas detectadas nas Observações?
10. ☐ Rodei script e as **6 validações §3.7.C** passaram (incluindo nova C.6)?

---

## 3.8 Determinação de Unidades Vendidas / % Vendido (v5.3+)

A col 19 da aba Empreendimentos (`% Vendido`) é calculada **automaticamente** pelo script combinando informações de §3.6 (Total) e §3.7 (Composição). Schema do E_RAW armazena internamente o ESTOQUE (% disponível, decimal 0-1); a xlsx mostra `1 - estoque` como `% Vendido`.

### Fórmula

```
disponíveis_empreend = Σ unidades em C_RAW (mesmo inc, emp)
estoque              = disponíveis / total
% vendido (xlsx)     = 1 - estoque
unidades_vendidas    = total - disponíveis
```

### Hierarquia de aplicação (cálculo automático §3.8)

| Caso | Condição | Ação |
|---|---|---|
| 1 | `% Vendido` já preenchido manualmente | Manter, marcar origem `informado_manualmente`. Validar contra cálculo (WARN se diff > 5%) |
| 2 | Empreend. é Niágara (formato agrupa) | Marcar origem `nao_determinavel`. Total fica `None` no xlsx (lista de busca) |
| 3 | `Origem total = tabela_local_completa` AND soma C_RAW = total | estoque = 1.0 (pré-lançamento). Origem `tabela_local_completa_zero` |
| 4 | `total > 0` AND `soma C_RAW > 0` | Calcular automaticamente (estoque = soma/total). Origem `calculado_automatico` |
| 5 | Sem dados base | estoque = `None`. Origem `N/A`. **Vira lista de busca pra obter info.** |

### Coluna 26 (E_RAW) "Origem % Vendido"

Schema E_RAW cresce de 25 → 26 colunas. Visualmente na xlsx aparece como col 20 (após "% Vendido" col 19).

Enum válido (subset do §4.7 com adições próprias):

| Valor | Significado |
|---|---|
| `calculado_automatico` | Aplicado pelo script via fórmula §3.8 |
| `informado_manualmente` | Valor passado pelo Rafael via WhatsApp/reunião |
| `tabela_local_completa_zero` | Origem total = `tabela_local_completa` AND soma C_RAW = total → 0% vendido (pré-lançamento) |
| `nao_determinavel` | Caso Niágara — formato da tabela não permite inferir vendidas |
| `N/A` | Sem dado base (sem total OU sem composição) — **lista de busca de info** |

### Validação automática (gerar_planilha.py)

Quando há valor manual E é possível calcular (total + soma C_RAW), comparar:
- Se `|estoque_manual - estoque_calc| > 0.05` (5%) → **WARN** no console.

### Convenção interna vs visual

**Atenção:** o E_RAW armazena `estoque` (% disponível), NÃO `% vendido`. A xlsx faz a inversão `1 - estoque`. Ao preencher manualmente, lembrar dessa convenção:

| Valor no E_RAW | Significado | % Vendido na xlsx |
|---:|---|---:|
| 0.0 | Esgotado (0% disponível) | 100% |
| 0.5 | Metade disponível | 50% |
| 1.0 | Todos disponíveis (pré-lançamento) | 0% |

Em 02/05/2026 detectamos 2 entries com inversão de convenção (Zion, Vernazza Norte) — corrigidas pela validação §3.8 ao rodar o cálculo pela primeira vez.

### Checklist de aplicação ao popular % Vendido

1. ☐ Identifiquei caso na hierarquia §3.8 (1 a 5)?
2. ☐ Se manual, lembrei que E_RAW armazena estoque (não vendido)?
3. ☐ Rodei o script — validação §3.8 passou (ou WARN justificado)?
4. ☐ Empreend. com origem `N/A` foram listados no roadmap pra busca?

---

## 3.9 Determinação do Mês de Lançamento (v5.4+)

A col 9 da aba Empreendimentos (`Mês lançamento`) precisa formato `MM/AAAA` (PADRAO §1) e origem (col 22 `Origem lançamento`). A regra T-36 (§3.5) calcula estimativa quando temos a entrega; §3.9 formaliza a hierarquia completa de fontes.

### Hierarquia de fontes (8 níveis)

| # | Fonte | Origem (§4.4) |
|---|---|---|
| 1 | **Release oficial / imprensa datada** (Imirante, Diego Emir, etc, com data explícita) | `imprensa` |
| 2 | **Tabela arquivada datada** (rodapé legal: "TABELA/MÊS: ABRIL/2026", validade) | `tabela_local` |
| 3 | **Book com data de lançamento** declarada explícita | `book` |
| 4 | **Site oficial** com página do empreendimento e data de lançamento | `site_oficial` |
| 5 | **Instagram oficial** — post de lançamento (data do post = data) | `instagram_oficial` |
| 6 | **Treinamento de corretor** (corretor passou data confirmada de lançamento comercial) | `treinamento_corretor` |
| 7 | **Informado manualmente** (Rafael, sem documento) | `informado_manualmente` |
| 8 | **Estimativa T-36** (`mês_lançamento = mês_entrega - 36 meses`) — só quando temos entrega declarada e nada nas posições 1-7 | `estimativa_T-36` |
| 9 | **Nada se aplica** | `Mês lançamento = None`. Origem `N/A`. **NÃO INVENTAR.** |

### Regra T-36 (§3.5, mantida)

Quando origem = `estimativa_T-36`:
- `mês_lançamento_estimado = mês_entrega - 36 meses`
- Sufixo obrigatório no campo: `MM/AAAA ⚠ T-36` (ex: `06/2025 ⚠ T-36`)
- Substituir assim que: tabela datada, data no book, release/imprensa, post de Instagram marcando lançamento, treinamento de corretor (forte sinal), campanha de teaser.

### Validação automática (gerar_planilha.py)

Quando origem = `estimativa_T-36` E `data_verif > 180 dias` atrás → **WARN** no console:

```
⚠ §3.9: <empreend>: origem=estimativa_T-36 há X dias — buscar fonte real
```

Não bloqueia, mas força revisão periódica das estimativas T-36 antigas.

### Coluna 22 (E_RAW) "Origem lançamento" — enum atualizado v5.4

Valores válidos:

| Valor | Significado |
|---|---|
| `imprensa` | Release/notícia datada |
| `tabela_local` | Rodapé/header de tabela arquivada |
| `book` | Book/material institucional |
| `site_oficial` | Site da incorporadora |
| `instagram_oficial` | Post de lançamento no @ oficial |
| `treinamento_corretor` | Corretor passou |
| `informado_manualmente` | Rafael declarou sem documento |
| `estimativa_T-36` | Calculado por entrega-36m (deve evoluir pra fonte real) |
| `N/A` | Sem dado base |

### Checklist de aplicação

1. ☐ Identifiquei origem mais alta possível na hierarquia §3.9?
2. ☐ Mês está em formato `MM/AAAA` (PADRAO §1)?
3. ☐ Se T-36, sufixei `⚠ T-36` no valor?
4. ☐ Origem preenchida na col 22?
5. ☐ Rodei script — validação §3.9 passou ou WARN justificado?
6. ☐ Empreend. com `T-36` antigos foram revisitados?

---

## 3.10 Determinação do Bairro / Região (v6.0+)

A col 4 da aba Empreendimentos (`Bairro`) representa a **REGIÃO SENSO COMUM** (como o mercado se refere ao local), não necessariamente o bairro oficial do CEP. Bairro oficial fica implícito no campo `Endereço` (col 3, formato completo "Rua, Nº, Bairro, São Luís - MA").

### Por que essa escolha

Em SLZ, alguns empreendimentos têm **divergência** entre bairro oficial (escritura/CEP) e a região comercializada no marketing. Para análise competitiva (heatmaps, % vendido por região, R$/m² por área), o que importa é a **região de mercado** — onde o público-alvo busca o imóvel. O book/material de marketing reflete essa região.

### Hierarquia de fontes

| # | Fonte | Origem (col 5 nova) |
|---|---|---|
| 1 | **Book / material de marketing** declarando explícito | `book` |
| 2 | **Site oficial / página do empreendimento** | `site_oficial` |
| 3 | **Imprensa / release** mencionando localização de mercado | `imprensa` |
| 4 | **Treinamento de corretor** | `treinamento_corretor` |
| 5 | **Informado manualmente** (Rafael) | `informado_manualmente` |
| 6 | **Endereço oficial** (do CEP/escritura — fallback) | `endereco_oficial` |
| 7 | **Sem dado** | Bairro = `None` (raro). Origem = `N/A`. |

### Coluna 5 (xlsx) "Origem Bairro" — nova v10.0

Schema E_RAW cresce 26 → 27 colunas. Visualmente na xlsx aparece logo após "Bairro" (pos 5).

### Quando o material de marketing não declara região explícita

Usar o bairro oficial do CEP (origem `endereco_oficial`). Não é demérito — é o caso comum quando não há divergência.

### Validação automática (gerar_planilha.py)

- Se `Bairro` tem valor mas `Origem Bairro = None` → WARN ("preencher origem por §3.10")
- Se `Bairro = "São Luís"` ou `"Não identificado"` → WARN ("bairro genérico, refinar")

### Checklist de aplicação

1. ☐ Identifiquei o bairro/região no nível mais alto possível da hierarquia §3.10?
2. ☐ Preenchi origem na col 5 (xlsx) / col 27 (E_RAW)?
3. ☐ Endereço completo (col 3) tem o bairro oficial pra referência?
4. ☐ Quando book diz "Calhau" mas endereço diz "Loteamento Calhau", priorizei book?

### Cenários canônicos

- **The View**: book = "Calhau", endereço = "Calhau" → Bairro `Calhau`, origem `book`.
- **Bossa**: book = "Calhau", endereço = "Loteamento Calhau" → Bairro `Calhau`, origem `book` (book prevalece).
- **Empreend. apenas com endereço, sem material de marketing** → Bairro do CEP, origem `endereco_oficial`.

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
**Origem lançamento:** `imprensa` | `tabela_local` | `book` | `site_oficial` | `instagram_oficial` | `treinamento_corretor` | `informado_manualmente` | `estimativa_T-36` | `N/A` (v5.4: hierarquia §3.9)
**Origem Composição (v6.2):** `tabela_local` | `tabela_local_imagem` | `book` | `informado_manualmente` | `estimativa_distribuição_mono` | `estimativa_distribuição_multi_com_area` | `estimativa_distribuição_multi_sem_area` | `estimativa_distribuição_sem_tipologia` (hierarquia §3.7.A)

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
