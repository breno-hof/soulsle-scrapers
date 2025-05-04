# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from typing import List

@dataclass
class SoulsWikiScrapersItem:
    name: str
    image_url: str
    areas: List[str]
    drops: List[str]
    stronger_vs: List[str]
    weaker_to: List[str]
    game: str
