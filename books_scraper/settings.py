BOT_NAME = "books_scraper"

SPIDER_MODULES = ["books_scraper.spiders"]
NEWSPIDER_MODULE = "books_scraper.spiders"

# Site d'entraînement : on respecte robots.txt et on reste raisonnable
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 0.5
CONCURRENT_REQUESTS_PER_DOMAIN = 8
USER_AGENT = "books_scraper (+https://books.toscrape.com)"

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

ITEM_PIPELINES = {
    "books_scraper.pipelines.CleaningPipeline": 100,
    # Bonus 2 : télécharge automatiquement l'image de chaque livre
    "scrapy.pipelines.images.ImagesPipeline": 200,
}

# Dossier de stockage des images téléchargées (Bonus 2)
IMAGES_STORE = "images"
