"""
Bonus 3 — Statistiques sur books.csv (ou books.json).

Usage :
    python stats.py books.csv
    python stats.py books.json
"""

import json
import sys
from pathlib import Path

import pandas as pd


def load_books(path: str) -> pd.DataFrame:
    path = Path(path)
    if path.suffix == ".json":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return pd.DataFrame(data)
    return pd.read_csv(path)


def main():
    if len(sys.argv) != 2:
        print("Usage : python stats.py <books.csv|books.json>")
        sys.exit(1)

    df = load_books(sys.argv[1])
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["star_rating"] = pd.to_numeric(df["star_rating"], errors="coerce")

    print(f"Nombre de livres récupérés     : {len(df)}")
    print(f"Prix moyen                     : {df['price'].mean():.2f}")

    plus_cher = df.loc[df["price"].idxmax()]
    moins_cher = df.loc[df["price"].idxmin()]
    print(f"Livre le plus cher              : {plus_cher['title']} ({plus_cher['price']:.2f})")
    print(f"Livre le moins cher              : {moins_cher['title']} ({moins_cher['price']:.2f})")

    top_category = df["category"].value_counts().idxmax()
    print(f"Catégorie la plus représentée   : {top_category} ({df['category'].value_counts().max()} livres)")

    print(f"Note moyenne                   : {df['star_rating'].mean():.2f}")
    print(f"Livres notés 5 étoiles          : {(df['star_rating'] == 5).sum()}")


if __name__ == "__main__":
    main()
