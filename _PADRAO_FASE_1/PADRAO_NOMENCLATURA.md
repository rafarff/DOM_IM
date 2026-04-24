# Padrão de Nomenclatura — Inteligência de Mercado DOM

*Versão 1.0 · 23/04/2026*

Este documento define o padrão de **pastas e arquivos** da pasta de Inteligência de Mercado (`01.Inteligência Mercado/`). Ele existe para que qualquer pessoa do time consiga encontrar arquivos rapidamente e para automatizar a extração de dados.

## Estrutura de pastas (3 níveis)

```
01.Inteligência Mercado/
├── _INBOX/                           ← arquivos novos entram aqui primeiro
├── _NAO_CLASSIFICADO/                ← casos excepcionais
├── 00_ESTUDO_CONSOLIDADO/            ← repo Git (HTML público + scripts)
├── {NN_INCORPORADORA}/               ← pasta da incorporadora
│   ├── _Material_Geral/              ← material institucional (cartão virtual, portfólio)
│   └── {NOME_EMPREENDIMENTO_MMYYYY}/ ← pasta do empreendimento
│       ├── BOOK/                     ← books de vendas
│       ├── TABELA/                   ← tabelas de preços
│       └── OUTROS/                   ← qualquer outro material
```

## Nomenclatura de pastas

### Pasta da incorporadora — `NN_NOME`
- `NN` = número sequencial de 2 dígitos
- `NOME` = nome da incorporadora em MAIÚSCULAS, sem acento, underscore no lugar de espaço
- Exemplos: `01_ALFA_ENGENHARIA`, `06_MOTA_MACHADO`, `13_DOM_INCORPORACAO`

Incorporadoras atuais numeradas:

| # | Incorporadora | Pasta |
|---|---|---|
| 01 | Alfa Engenharia | `01_ALFA_ENGENHARIA` |
| 02 | Delman | `02_DELMAN` |
| 03 | Ergus | `03_ERGUS` |
| 04 | Treviso | `04_TREVISO` |
| 05 | Niágara | `05_NIAGARA` |
| 06 | Mota Machado | `06_MOTA_MACHADO` |
| 07 | Berg Engenharia | `07_BERG` |
| 08 | Lua Nova | `08_LUA_NOVA` |
| 09 | Monteplan | `09_MONTEPLAN` |
| 10 | Franere | `10_FRANERE` |
| 11 | Canopus | `11_CANOPUS` |
| 12 | MB Engenharia | `12_MB_ENGENHARIA` |
| 13 | DOM Incorporação | `13_DOM_INCORPORACAO` |
| 14 | Hiali | `14_HIALI` |
| 15 | Sá Cavalcante | `15_SA_CAVALCANTE` |
| 16 | Castelucci | `16_CASTELUCCI` |

### Pasta do empreendimento — `NOME_MMYYYY`
- `NOME` = nome do empreendimento em MAIÚSCULAS, sem acento, underscore no lugar de espaço
- `MMYYYY` = mês e ano de lançamento (6 dígitos, sem separador)
  - Se não houver data confirmada: `SEMDATA`
  - Se só o ano é conhecido: `XXYYYY`
- Exemplos: `EDIFICIO_BOSSA_042026`, `DOM_LUCAS_022026`, `VILLA_DI_CARPI_SEMDATA`

## Nomenclatura de arquivos

### Book — `BOOK_{NOME}_{MMYYYY}.pdf`
- `{NOME}` = mesmo nome normalizado usado na pasta
- `{MMYYYY}` = mês/ano de **criação do PDF** (indicador de quando o material começou a circular)
- Se houver múltiplas revisões no mesmo mês: sufixo `_R1`, `_R2`, `_v2`
- Exemplos:
  - `BOOK_EDIFICIO_BOSSA_042026.pdf`
  - `BOOK_AZIMUTH_072023_R1.pdf`
  - `BOOK_AZIMUTH_072023_R2.pdf` (revisão posterior no mesmo mês)

### Tabela — `TABELA_{NOME}_{MMYYYY}.pdf`
- `{MMYYYY}` = **data de vigência** declarada na tabela (não a data de criação do PDF)
- Exemplos:
  - `TABELA_LANDSCAPE_042026.pdf` (vigência abril/2026)
  - `TABELA_VERNAZZA_TORRE_NORTE_022026.pdf`

### Outros arquivos — pasta `OUTROS/`
Qualquer arquivo que não seja um book ou tabela vai para a subpasta `OUTROS/`, mantendo seu nome original. Exemplos:
- Plantas, folhetos promocionais
- Vídeos, imagens de render
- Cartões virtuais avulsos
- Informações técnicas da construtora

## Múltiplas torres / fases no mesmo empreendimento

Quando um empreendimento tem fases ou torres comercializadas separadamente (ex: Vernazza Torre Norte + Torre Sul), cada uma tem sua própria pasta:

```
04_TREVISO/
├── VERNAZZA_TORRE_NORTE_022025/
│   ├── BOOK/
│   ├── TABELA/
│   │   ├── TABELA_VERNAZZA_TORRE_NORTE_022026.pdf
│   │   └── TABELA_VERNAZZA_TORRE_NORTE_042026.pdf
│   └── OUTROS/
└── VERNAZZA_TORRE_SUL_022025/
    ├── BOOK/
    ├── TABELA/
    │   ├── TABELA_VERNAZZA_TORRE_SUL_022026.pdf
    │   └── TABELA_VERNAZZA_TORRE_SUL_042026.pdf
    └── OUTROS/
```

## Processo quando chega material novo

1. Rafael joga o arquivo no `_INBOX/`
2. Claude (Cowork) identifica incorporadora e empreendimento
3. Claude renomeia seguindo o padrão acima e move para a pasta correta:
   - Book → `{emp_folder}/BOOK/BOOK_{emp}_{data_criacao}.pdf`
   - Tabela → `{emp_folder}/TABELA/TABELA_{emp}_{vigencia}.pdf`
   - Outros → `{emp_folder}/OUTROS/{nome_original}`
4. Claude atualiza a Planilha Mestre
5. Claude regera o `index.html`
6. Rafael publica no GitHub via GitHub Desktop

## Regras de ouro

1. **Nunca colocar acentos** em nomes de pasta/arquivo (usar transliteração: "São" → "SAO", "Península" → "PENINSULA")
2. **Sempre MAIÚSCULAS com underscore** em pastas e arquivos principais
3. **A data na pasta é do LANÇAMENTO**, não da entrega
4. **A data no nome do BOOK é de CRIAÇÃO do PDF**
5. **A data no nome da TABELA é de VIGÊNCIA declarada**, não criação
6. Se nunca soubermos a data, use `SEMDATA` explicitamente (melhor que mentir)

---

*DOM Incorporação · Inteligência de Mercado · Fase 2*
