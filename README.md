books_scraper
Crawler Scrapy pour le site d'entraînement books.toscrape.com.

Objectif :
Parcourir automatiquement l'ensemble du catalogue (~1000 livres, pagination
découverte dynamiquement — aucune URL n'est écrite en dur), suivre la page de
détail de chaque livre, nettoyer les données et les exporter en CSV ou JSON.
Champs récupérés pour chaque livre :
Dans le catalogue : title, price, star_rating, in_stock, thumbnail_url, detail_url
Sur la page de détail : upc, description, number_available, category, image_url

Installation :
python -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install -r requirements.txt

Lancer le spider :
scrapy crawl books

Exporter les données :
scrapy crawl books -O books.csv
scrapy crawl books -O books.json

Structure du crawler :
START
  │
  ▼
Catalogue (parse) ──follow──► Page détail (parse_book_detail) ──► BookItem
  │                                                                   │
  ├── pagination "next" détectée automatiquement                     ▼
  ▼                                                            nettoyage des
Catalogue (page suivante)                                     données inline
  │                                                            (prix, stock,
  ▼                                                             note, texte)
  ... jusqu'à ce qu'il n'y ait plus de "next"                        │
  │                                                                   ▼
  ▼                                                             CSV / JSON
 END

 Nettoyage des données :
 Effectué directement dans parse_book_detail (spiders/books.py) :
"£51.77" → 51.77 (float)
"In stock (22 available)" → 22 (int)
note (star-rating Three) → 3 (int), résolue dès le parsing du catalogue
description : espaces / retours à la ligne superflus supprimés
les URLs d'image et de détail sont construites avec response.urljoin() :
toujours absolues, jamais relatives

Organisation du projet :
books_scraper/
├── scrapy.cfg
├── books_scraper/
│   ├── __init__.py
│   ├── items.py          # BookItem
│   ├── middlewares.py
│   ├── pipelines.py       # squelette par défaut (non utilisé)
│   ├── settings.py
│   └── spiders/
│       ├── __init__.py
│       └── books.py       # spider "books"
├── README.md
└── requirements.txt
