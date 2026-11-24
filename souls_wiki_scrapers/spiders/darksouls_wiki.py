import scrapy
from ..utils.spider_utils import clean_text, dedupe, field_values, infobox_fields

class DarkSoulsWikiSpider(scrapy.Spider):
  name = "darksouls_wiki"
  start_urls = ["https://darksouls.wiki.fextralife.com/Area_Bosses", "https://darksouls.wiki.fextralife.com/Mini_Bosses", "https://darksouls.wiki.fextralife.com/Expansion_Bosses"]

  # Bosses whose infobox has no location
  fixed_areas = {
    "Dragon Slayer Ornstein and Executioner Smough": ["Anor Londo"]
  }

  def parse(self, response):
    for href in response.css('.mw-parser-output > div.row a::attr(href)').getall():
      if not href.startswith('/File:'):
        yield response.follow(href, callback=self.parse_boss)

  def parse_boss(self, response):
    table = response.css('#infobox table')
    name = clean_text(table.css('tr:first-child > th'))

    if not name:
      return

    fields = infobox_fields(table)
    areas = self.fixed_areas.get(name) or field_values(fields, ['location'])

    yield {
      'name': name,
      'image_url': table.css('img::attr(src)').get(),
      'areas': areas,
      'drops': self.parse_drops(response),
      'stronger_vs': [],
      'weaker_to': [],
      'game': 'Dark Souls'
    }

  def parse_drops(self, response):
    # Drops are listed under a "... Drops" heading, either directly or inside a div.row
    content = response.css('.mw-parser-output')
    lists = content.xpath('./h3[contains(., "Drops")]/following-sibling::*[1][self::ul]')

    if lists == []:
      lists = content.xpath('./div[contains(@class, "row")][.//*[contains(text(), "Drops")]]//ul')

    drops = [item.css('a::text').get() for item in lists.css('li')]
    return dedupe([drop.strip() for drop in drops if drop and drop.strip()])
