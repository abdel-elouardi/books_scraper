# books_scraper

Crawler Scrapy pour le site d'entraînement [books.toscrape.com](https://books.toscrape.com/).

## Objectif

Parcourir automatiquement l'ensemble du catalogue (~1000 livres, pagination
découverte dynamiquement — aucune URL n'est écrite en dur), suivre la page de
détail de chaque livre, nettoyer les données et les exporter en CSV ou JSON.

Pour chaque livre :

| Champ              | Source    |
|---------------------|-----------|
| title               | catalogue |
| price               | catalogue |
| star_rating         | catalogue |
| in_stock            | catalogue |
| thumbnail_url       | catalogue |
| detail_url          | catalogue |
| upc                 | détail    |
| description         | détail    |
| number_available    | détail    |
| category            | détail    |
| image_url           | détail    |

## Installation

```bash
python -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer le spider

```bash
scrapy crawl books
```

## Exporter les données

```bash
scrapy crawl books -O books.csv
scrapy crawl books -O books.json
```

## Filtrer par catégorie (Challenge)

```bash
scrapy crawl books -a category=travel -O travel.csv
```
Seuls les livres de la catégorie demandée sont alors conservés dans l'export
(la comparaison ignore la casse).

## Statistiques (Bonus 3)

Une fois l'export terminé :

```bash
python stats.py books.csv
```

Affiche : nombre de livres, prix moyen, livre le plus cher/le moins cher,
catégorie la plus représentée, note moyenne, nombre de livres 5 étoiles.

## Structure du crawler

```
START
  │
  ▼
Catalogue (parse) ──follow──► Page détail (parse_book_detail) ──► BookItem
  │                                                                   │
  ├── pagination "next" détectée automatiquement                     ▼
  ▼                                                            CleaningPipeline
Catalogue (page suivante)                                       (prix, stock,
  │                                                               note, texte)
  ▼                                                                   │
  ... jusqu'à ce qu'il n'y ait plus de "next"                         ▼
  │                                                            ImagesPipeline
  ▼                                                          (téléchargement
 END                                                          local des images)
                                                                       │
                                                                       ▼
                                                                 CSV / JSON
```

## Nettoyage des données (pipeline)

`CleaningPipeline` (dans `pipelines.py`) convertit les champs bruts :

- `"£51.77"` → `51.77` (float)
- `"In stock (22 available)"` → `22` (int)
- note (`star-rating Three`) → `3` (int), déjà résolue dans le spider
- description : espaces/retours à la ligne superflus supprimés
- les URLs d'image et de page de détail sont construites avec
  `response.urljoin()` : toujours absolues, jamais relatives

## Téléchargement des images (Bonus 2)

`ImagesPipeline` de Scrapy est activée dans `settings.py` et utilise le champ
`image_urls` renseigné par le spider. Les images sont enregistrées dans le
dossier `images/` à la racine du projet, aux côtés d'un champ `images`
(chemin local, checksum) ajouté automatiquement à chaque item.

## Organisation du projet

```
books_scraper/
├── scrapy.cfg
├── books_scraper/
│   ├── __init__.py
│   ├── items.py          # BookItem
│   ├── middlewares.py
│   ├── pipelines.py       # CleaningPipeline
│   ├── settings.py
│   └── spiders/
│       ├── __init__.py
│       └── books.py       # spider "books"
├── stats.py                # Bonus 3
├── README.md
└── requirements.txt
```
