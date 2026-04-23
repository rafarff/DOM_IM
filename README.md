# DOM · Inteligência de Mercado — Panorama de Lançamentos Grande São Luís

Dashboard interativo com o panorama de empreendimentos residenciais em comercialização na Grande São Luís (MA), mantido pela DOM Incorporação para acompanhamento competitivo.

**🌐 Acesso:** https://rafarff.github.io/DOM_IM/

---

## O que tem aqui

- **`index.html`** — dashboard gerado (mapa Leaflet + KPIs + filtros + tabela). Abre direto no navegador, sem backend. Dados embutidos no próprio arquivo.
- **`build_panorama.py`** — script Python que lê a Planilha Mestre e regenera o `index.html`.
- **`publish.sh`** — one-liner para regenerar o HTML, comitar e dar push.

## O que NÃO está aqui (fica local)

Por decisão explícita, **não versionamos** neste repo:

- Planilha Mestre (`Planilha_Mestre_Panorama_vX.X.xlsx`)
- Books e tabelas em PDF das incorporadoras
- Pasta fonte `01.Inteligência Mercado/`

Esses arquivos ficam na máquina do Rafael. O GitHub serve só o HTML gerado.

## Fluxo de atualização (manual, sob demanda)

1. **Você dropa** PDFs novos (books, tabelas) dentro de `01.Inteligência Mercado/_INBOX/`
2. **Chama o Claude** no Cowork: _"organiza o que tem no INBOX e atualiza o estudo"_
3. **Claude faz**: identifica incorporadora, move PDF para subpasta correta, atualiza a Planilha Mestre, regenera `index.html`
4. **Você publica** via GitHub Desktop (commit + push) ou pelo terminal:
   ```bash
   cd "/caminho/para/01.Inteligência Mercado/00_ESTUDO_CONSOLIDADO"
   ./publish.sh "Atualização semanal DD/MM/AAAA"
   ```
5. Em 1-2 minutos o GitHub Pages está atualizado.

**Regra do _INBOX**: ao final de cada ciclo, a pasta deve ficar vazia. Se tem arquivo lá, é sinal de pendência.

## Estrutura de pastas (no computador do Rafael)

```
/mnt/
├── 01.Inteligência Mercado/              ← dados-fonte (não versionados)
│   ├── 00_ESTUDO_CONSOLIDADO/
│   │   └── Planilha_Mestre_Panorama_vX.X.xlsx
│   ├── 01_ALFA_ENGENHARIA/
│   ├── 02_DELMAN/
│   └── ...
│
└── Inteligência de Mercado - DOM/        ← repo Git (este)
    ├── build_panorama.py
    ├── index.html                        ← gerado
    ├── publish.sh
    ├── .gitignore
    └── README.md
```

## Incorporadoras monitoradas

Mota Machado, Berg Engenharia, Alfa Engenharia, Lua Nova, Delman, Treviso, Ergus, Monteplan, Franere, Canopus, Niágara, MB Engenharia. *(Sá Cavalcante e Castelucci aparecem como referência complementar.)*

## Dimensões analisadas por empreendimento

Portfólio · Segmento · Localização · Tipologia · Faixa de preço (VGV, ticket médio) · Velocidade de vendas · Parceiros · Posicionamento · Pontos fortes/fracos · Movimentos recentes.

---

*Versão v4.4 · Fase 2 — Dashboard Interativo*
