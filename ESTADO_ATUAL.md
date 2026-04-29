# ESTADO ATUAL — Inteligência de Mercado DOM

> **Para Claude (toda sessão):** este é o **primeiro arquivo a ler** antes de qualquer ação. Confirma a base de trabalho. Se a invariante 0.3 do PADRAO falhar contra os números aqui, **PARAR**.

**Última atualização:** 28/04/2026
**Versão Planilha vigente:** v6.5
**Versão PADRAO vigente:** v3.5
**Versão script `gerar_planilha.py`:** 6.5 (DATE_STR: 28/04/2026)

---

## Snapshot da carteira

| Métrica | Valor |
|---|---:|
| Total de empreendimentos no E_RAW | **46** |
| Total de empreendimentos na v6.5.xlsx (aba Empreendimentos) | **46** |
| Drift script ↔ planilha | **0** ✅ |
| Incorporadoras monitoradas (lista fechada) | **16** |
| Incorporadoras com ≥1 empreendimento mapeado | 16 (todas) |
| Schema aba Empreendimentos | **24 colunas** |
| Schema aba Incorporadoras | **15 colunas** |
| VGV total mapeado | **R$ 1,31 bi** |

### Distribuição por incorporadora (v6.5)

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

## Comando one-liner (confirmar versão vigente antes de qualquer ação)

```bash
cd 00_ESTUDO_CONSOLIDADO/ && ls -1 Planilha_Mestre_Panorama_v*.xlsx | sort -V | tail -1
```

Nunca confiar em `ls` sem `sort -V` — `v4.5` aparece depois de `v4.16` em ordem lexicográfica.

---

## Mudanças estruturais recentes (consultar PADRAO §0–§4 para regras)

- **v6.0** (27/04/2026) — coluna **Status** removida (era col 7). 25 → 24 colunas. Filtro "ativo no ciclo" no HTML também eliminado.
- **v6.1** (27/04/2026) — **Tipologia** virou enum estruturado (Studio/1D/2D/3D/4D/Lote). Texto livre antigo migrado para Observações com prefixo `Tipologia detalhada:`.
- **v6.2** (27/04/2026) — pin no mapa só com endereço completo (Rua/Av./Plus Code).
- **v6.3** (27/04/2026) — **mapa removido** do HTML por decisão Rafael (`tem_endereco_completo()` e `geocode_bairro()` permanecem em `build_panorama.py` para retorno futuro).
- **v6.4** (27/04/2026) — Tipo "Misto" removido, **Loteamento** formalizado como 3ª categoria de Tipo (junto com Vertical/Horizontal). Distinção crítica: R$/m² em Loteamento é m² de **terreno**.
- **v6.5** (28/04/2026) — **The View atualizado** (tabela 28/04 v3 → 93 aptos disp., ticket_min cai p/ R$540k). **Bossa enriquecido** (arquiteto Nasser Hissa, vizinhança Lote 07/08 com The View). **Fix estrutural:** BASE e SKILL_ASSETS agora derivados via `pathlib.Path(__file__)` (script auto-suficiente em qualquer sessão). Logo DOM copiado para `_PADRAO_FASE_1/assets/`. PADRAO bumpado para v3.5 (adição §0.4 Bootstrap + §0.5 Pre-flight).

---

## Bugs latentes conhecidos (a tratar)

*(nenhum — bug do BASE hardcoded foi corrigido em v6.5)*

---

## Armadilhas comuns (lições aprendidas)

1. **Glob recursivo amplo trunca silenciosamente.** Usar `Glob` com pattern específico (`Planilha_Mestre_Panorama_v*.xlsx`) e/ou `sort -V | tail -N`. Nunca tirar conclusão de listagem que mostre o aviso `Results are truncated`.

2. **Filtros de leitura de .xlsx por prefixo de nome são frágeis.** A v6.x tem footer "DOM Incorporação • Inteligência de Mercado" e legenda "Linhas DOURADAS = ...". Filtrar entries por `startswith("DOM Inco")` mata as 4 entries reais da DOM Incorporação. **Filtrar pelo padrão da linha completa** (presença de `•`, comprimento >50 chars, etc.) ou usar lista whitelist do `INCORPORADORAS`.

3. **Versão `v4.5` aparece depois de `v4.16` em ordem lexicográfica.** Sempre `sort -V` para versão semântica.

4. **NFD vs NFC em paths macOS:** pasta "Inteligência" é NFD (`e` + combining circumflex U+0302). Python que cria pastas com acentos pode gerar pasta-fantasma NFC se não usar a forma certa. A v6.5 do `gerar_planilha.py` usa `pathlib.Path(__file__).resolve().parent.parent` que herda automaticamente a forma do filesystem real.

5. **Bossa e The View são vizinhos** (Quadra 02 da Av. dos Holandeses, Calhau — Lotes 07 e 08 respectivamente). Lançamentos simultâneos de Mota Machado e Delman no mesmo período (04/2026) com posicionamentos diferentes: Bossa = 4-suítes 191m² Luxo; The View = Studio-3D 36-86m² Médio-alto/Alto. Vale acompanhar como cada um performa frente ao outro.

---

## O que mantém este arquivo atualizado

`publish.sh` (idealmente) deve regenerar este arquivo em cada rodada — ainda não implementado. Por enquanto, **toda vez que VERSION ou schema mudar no script, atualizar este arquivo manualmente**.

*Quando Claude rodar `5.1 — atualiza o estudo` ou `5.5 — adicionei arquivos de [incorporadora]`, regenera este ESTADO_ATUAL.md como parte do workflow.*
