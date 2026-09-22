import re

from itemadapter import ItemAdapter


class CleaningPipeline:
    """Nettoie et convertit les champs bruts d'un BookItem.

    - price            : "£51.77"                  -> 51.77 (float)
    - number_available : "In stock (22 available)"  -> 22 (int)
    - star_rating       : garanti sous forme d'int (ou None)
    - description       : espaces/retours à la ligne superflus supprimés
    """

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        price = adapter.get("price")
        if price:
            cleaned = re.sub(r"[^\d.]", "", price)
            adapter["price"] = float(cleaned) if cleaned else None

        number_available = adapter.get("number_available")
        if number_available:
            match = re.search(r"(\d+)", number_available)
            adapter["number_available"] = int(match.group(1)) if match else 0

        star_rating = adapter.get("star_rating")
        if star_rating is not None:
            adapter["star_rating"] = int(star_rating)

        description = adapter.get("description")
        if description:
            adapter["description"] = " ".join(description.split())

        return item


# Bonus 2 : le téléchargement d'images est géré par
# scrapy.pipelines.images.ImagesPipeline, activée dans settings.py.
# Elle utilise le champ "image_urls" renseigné par le spider et remplit
# automatiquement le champ "images" (chemin local, checksum, url).
