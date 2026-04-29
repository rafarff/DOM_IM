# ESTADO ATUAL — Inteligência de Mercado DOM

> **Para Claude (toda sessão):** este é o **primeiro arquivo a ler** antes de qualquer ação. Confirma a base de trabalho. Se a invariante 0.3 do PADRAO falhar contra os números aqui, **PARAR**.

**Última atualização:** 29/04/2026
**Versão Planilha vigente:** v6.6
**Versão PADRAO vigente:** v3.5
**Versão script `gerar_planilha.py`:** 6.6 (DATE_STR: 29/04/2026)

---

## Snapshot da carteira

| Métrica | Valor |
|---|---:|
| Total de empreendimentos no E_RAW | **46** |
| Total de empreendimentos na v6.6.xlsx (aba Empreendimentos) | **46** |
| Drift script ↔ planilha | **0** ✅ |
| Incorporadoras monitoradas (lista fechada) | **16** |
| Incorporadoras com ≥1 empreendimento mapeado | 16 (todas) |
| Schema aba Empreendimentos | **24 colunas** |
| Schema aba Incorporadoras | **15 colunas** |
| VGV total mapeado | **R$ 1,45 bi** (subiu R$ 137M na v6.6) |
| Preço calculável | 27/46 (subiu de 24 na v6.5) |

### Distribuição por incorporadora (v6.6)

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
- **v6.1** (27/04/2026) — **Tipologia** virou enum estruturado (Studio/1D/2D/3D/4D/Lote).
- **v6.2** (27/04/2026) — pin no mapa só com endereço completo (depois revertido).
- **v6.3** (27/04/2026) — **mapa removido** do HTML por decisão Rafael.
- **v6.4** (27/04/2026) — Tipo "Misto" removido, **Loteamento** formalizado.
- **v6.5** (28/04/2026) — The View atualizado, Bossa enriquecido. Fix BASE/SKILL_ASSETS via pathlib relativo. PADRAO v3.5 (bootstrap §0.4 + pre-flight §0.5).
- **v6.6** (29/04/2026) — Logo HTML 60→90px. **+Coluna "% Vendido" na Tabela A** com tooltip rico de origem (PADRAO §3.3). Auditoria de gaps tabela vs E_RAW (4 gaps reais). Preenchidos 3: Renaissance Conceito (105 unid, R$1.038-1.565k, ~79% vendido), Sanpaolo (~99% vendido, 1 unid restante), Reserva São Marcos (R$977k-1.317k, áreas 67-104m² extraídas do BOOK). Zion Ponta d'Areia ficou pendente (PDFs em imagem, OCR ilegível).

---

## Bugs latentes / pendências conhecidas

### 🟡 Zion Ponta d'Areia (Ergus) — tabela em imagem

9 PDFs arquivados em `03_ERGUS/ZION_PONTA_D_AREIA_122023/TABELA/`, todos baseados em imagem. `pdftotext` retorna apenas elementos decorativos. OCR via tesseract testado — resultado ilegível (tabelas com mapas decorativos).

**Próximas ações possíveis (em ordem de custo crescente):**
1. Pedir ao corretor da Ergus tabela em formato texto/Excel
2. OCR mais robusto (Google Vision, Adobe)
3. Manual: ler a tabela em PDF e digitar os dados-chave (rápido, ~10 min)

### 🟡 13 empreend. com gap só de % Vendido

Têm tickets/áreas, faltam contar unidades disponíveis em tabelas já arquivadas. Trabalho menor, separado pra v6.7 ou rodada futura.

---

## Armadilhas comuns (lições aprendidas)

1. **Glob recursivo amplo trunca silenciosamente.** Usar pattern específico e/ou `sort -V | tail -N`.

2. **Filtros por prefixo de nome são frágeis.** Footer "DOM Incorporação • Inteligência de Mercado" tem mesmo prefixo das 4 entries reais da DOM Incorporação. **Filtrar pelo padrão da linha completa**, não por nome.

3. **Versão `v4.5` aparece depois de `v4.16` em ordem lexicográfica.** Sempre `sort -V`.

4. **NFD vs NFC em paths macOS.** A v6.5 do `gerar_planilha.py` usa `pathlib.Path(__file__).resolve().parent.parent` que herda automaticamente a forma do filesystem real.

5. **Bossa e The View são vizinhos** (Quadra 02 da Av. dos Holandeses, Calhau — Lotes 07 e 08). Lançamentos simultâneos com posicionamentos opostos (luxo vs médio-alto).

6. **Tabelas em PDF imagem não são triviais.** pdftotext só extrai texto. Para tabelas geradas como imagem (caso Ergus/Zion), precisa OCR robusto ou solicitação ao corretor.

7. **`p.write_text` precisa ser explícito.** Patches em memória não vão pro disco sem o save final — fácil de esquecer em scripts longos.

---

## O que mantém este arquivo atualizado

`publish.sh` (idealmente) deve regenerar este arquivo em cada rodada — ainda não implementado. Por enquanto, **toda vez que VERSION ou schema mudar, atualizar este arquivo manualmente**.
