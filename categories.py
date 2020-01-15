from typing import NamedTuple, List

import db


class Category(NamedTuple):
    """Categories structure"""
    codename: str
    name: str
    inside_budget: bool
    aliases: List[str]


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        """Returns list of categories"""
        categories = db.fetchall(
            "category", "codename name inside_budget aliases".split()
        )
        categories = self._fill_aliases(categories)
        return categories

    def _fill_aliases(self, categories) -> List[Category]:
        categories_result = []
        for index, category in enumerate(categories):
            aliases = category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category["codename"])
            aliases.append(category["name"])
            categories_result.append(Category(
                codename=category['codename'],
                name=category['name'],
                inside_budget=category['inside_budget'],
                aliases=aliases
            ))
        return categories_result

    def get_all_categories(self) -> List[Category]:
        """Return reference book of all categories with aliases"""
        return self._categories

    def get_category(self, category_name: str) -> Category:
        """Returns category by its aliases"""
        found = None
        for category in self._categories:
            for alias in category.aliases:
                if category_name in alias:
                    found = category
        return found
