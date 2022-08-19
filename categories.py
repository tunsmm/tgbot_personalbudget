from typing import Dict, List

import db


class Categories:
    def __init__(self):
        self.__categories = self.__load_categories()

    def __load_categories(self) -> List[Dict]:
        categories = db.fetchall(
            "category", "codename name is_base_expense aliases".split()
        )
        self.__fill_aliases(categories)
        return categories

    def __fill_aliases(self, categories) -> List[Dict]:
        for index, category in enumerate(categories):
            aliases = category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category["codename"])
            aliases.append(category["name"])
            categories[index]["aliases"] = aliases

    def get_all_categories(self) -> List[Dict]:
        return self._categories

    def get_category(self, category_name: str) -> str:
        finded = None
        other_category = None
        for category in self.__categories:
            if category["codename"] == "other":
                other_category = category
            for alias in category['aliases']:
                if category_name in alias:
                    finded = category
        if not finded:
            finded = other_category
        return finded
