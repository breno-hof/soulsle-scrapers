import scrapy
from ..utils.spider_utils import clean_text, field_values, infobox_fields

class BloodborneWikiSpider(scrapy.Spider):
  name = "bloodborne_wiki"
  start_urls = ["https://bloodborne.wiki.fextralife.com/Bosses", "https://bloodborne.wiki.fextralife.com/Chalice_Dungeon_Bosses", "https://bloodborne.wiki.fextralife.com/The_Old_Hunters_Bosses"]

  bad_hrefs = ["Headstone", "Chalice", "Subcontent:", "File:", "redlink", "/The_Old_Hunters", "/The_Hunter%27s_Dream"]

  def parse(self, response):
    panels = response.css('.tabber__panel')
    links = panels[0].css('a::attr(href)').getall() if panels else []
    links += response.css('.mw-parser-output > ul li a::attr(href)').getall()

    for href in links:
      if not any(bad_href in href for bad_href in self.bad_hrefs):
        yield response.follow(href, callback=self.parse_boss)

  def parse_boss(self, response):
    table = response.css('#infobox table')
    name = clean_text(table.css('tr:first-child > th'))
    fields = infobox_fields(table)

    # Skip linked pages that aren't bosses (items, areas, ...)
    if not name or 'location' not in fields:
      return

    yield {
      'name': name,
      'image_url': table.css('img::attr(src)').get(),
      'areas': self.parse_areas(response, fields),
      'drops': field_values(fields, ['drops']),
      'stronger_vs': [],
      'weaker_to': [],
      'game': 'Bloodborne'
    }

  def parse_areas(self, response, fields):
    # Since the wiki migration many infobox locations are stale legacy links
    # (a.wiki_link, e.g. "Lower Hintertomb Chalice"), so prefer the "Locations" section
    section = response.css('.mw-parser-output').xpath('./h3[contains(., "Location")]/following-sibling::*[1][self::ul]')
    # The link title is the page name; link texts are sometimes split ("L" + "ower Hintertomb Chalice")
    area = section.css('li:first-child a::attr(title)').get()

    if area and area.strip():
      return [area.replace('(page does not exist)', '').strip()]

    if fields['location'].css('a.wiki_link'):
      return []

    return field_values(fields, ['location'])
