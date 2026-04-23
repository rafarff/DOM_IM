# DOM · Inteligência de Mercado — Panorama de Lançamentos Grande São Luís

Dashboard interativo com o panorama de empreendimentos residenciais em comercialização na Grande São Luís (MA), mantido pela DOM Incorporação para acompanhamento competitivo.

**🌐 Acesso:** https://USUARIO.github.io/REPO/ *(ajustar após publicação no GitHub Pages)*

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

## Fluxo de atualização manual

```bash
# 1. Dropar novos arquivos em 01.Inteligência Mercado/ (raiz)
# 2. Abrir Cowork/Claude, pedir: "organiza os novos arquivos e atualiza o estudo"
# 3. Quando a planilha estiver atualizada:
cd "/caminho/para/Inteligência de Mercado - DOM"
./publish.sh "Atualização semanal DD/MM/AAAA"

# Em ~1-2 minutos o GitHub Pages está atualizado.
```

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
