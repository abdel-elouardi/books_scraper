import re

import scrapy

from books_scraper.items import BookItem

RATING_WORDS = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


class BooksSpider(scrapy.Spider):
    """Parcourt tout le catalogue de books.toscrape.com et suit chaque
    page de détail pour construire un jeu de données structuré.

    Usage :
        scrapy crawl books -O books.csv
        scrapy crawl books -O books.json
    """

    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        """Détecte tous les livres de la page catalogue, puis suit
        chaque page de détail et la pagination — sans jamais écrire
        d'URL de page en dur.
        """
        for book in response.css("article.product_pod"):
            relative_url = book.css("h3 a::attr(href)").get()
            detail_url = response.urljoin(relative_url)

            rating_class = book.css("p.star-rating::attr(class)").get("") or ""
            rating_word = rating_class.replace("star-rating", "").strip()
            star_rating = RATING_WORDS.get(rating_word)

            thumbnail_relative = book.css("div.image_container img::attr(src)").get()
            thumbnail_url = response.urljoin(thumbnail_relative)

            stock_text = " ".join(
                book.css("p.instock.availability::text").getall()
            )

            catalogue_data = {
                "title": book.css("h3 a::attr(title)").get(),
                "price": book.css("p.price_color::text").get(),
                "star_rating": star_rating,
                "in_stock": "in stock" in stock_text.lower(),
                "thumbnail_url": thumbnail_url,
                "detail_url": detail_url,
            }

            yield response.follow(
                detail_url,
                callback=self.parse_book_detail,
                meta={"catalogue_data": catalogue_data},
            )

        # Pagination : on suit le bouton "next" tant qu'il existe,
        # sans jamais construire les URLs des 50 pages nous-mêmes.
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_book_detail(self, response):
        """Complète chaque livre avec les informations de sa page de détail
        et nettoie les données brutes avant de retourner l'Item.
        """
        catalogue_data = response.meta["catalogue_data"]

        table_data = {}
        for row in response.css("table.table.table-striped tr"):
            key = row.css("th::text").get()
            value = row.css("td::text").get()
            table_data[key] = value

        breadcrumb_links = response.css("ul.breadcrumb li a::text").getall()
        category = breadcrumb_links[-1] if breadcrumb_links else None

        image_relative = response.css("div.item.active img::attr(src)").get()
        image_url = response.urljoin(image_relative) if image_relative else None

        description = response.css("#product_description ~ p::text").get()
        if description:
            description = " ".join(description.split())

        # --- Nettoyage des données (section 7 du cahier des charges) ---
        price_raw = catalogue_data["price"]
        price = float(re.sub(r"[^\d.]", "", price_raw)) if price_raw else None

        availability_raw = table_data.get("Availability")
        match = re.search(r"(\d+)", availability_raw) if availability_raw else None
        number_available = int(match.group(1)) if match else 0

        item = BookItem()
        item["title"] = catalogue_data["title"]
        item["price"] = price
        item["star_rating"] = catalogue_data["star_rating"]
        item["in_stock"] = catalogue_data["in_stock"]
        item["thumbnail_url"] = catalogue_data["thumbnail_url"]
        item["detail_url"] = catalogue_data["detail_url"]

        item["upc"] = table_data.get("UPC")
        item["description"] = description
        item["number_available"] = number_available
        item["category"] = category
        item["image_url"] = image_url

        yield item
