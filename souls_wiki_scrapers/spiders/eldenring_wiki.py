import scrapy
from ..utils.spider_utils import clean_text, dedupe

class EldenRingWikiSpider(scrapy.Spider):
  name = "eldenring_wiki"
  start_urls = ["https://eldenring.wiki.fextralife.com/Bosses"]

  game_name = 'Elden Ring'

  def parse(self, response):
    for href in response.css('#tabber-Boss_List_by_Location ul li a::attr(href)').getall():
      yield response.follow(href, callback=self.parse_boss)

  def parse_boss(self, response):
    infobox = response.css('.er-boss-infobox')
    name = clean_text(infobox.css('.er-boss-name'))

    if not name:
      return

    yield {
      'name': name,
      'image_url': infobox.css('.er-boss-image img::attr(src)').get(),
      'areas': self.link_texts(infobox.css('.er-boss-location-label')),
      'drops': self.link_texts(infobox.css('.er-boss-location-drops')),
      'stronger_vs': self.link_texts(infobox.css('.er-boss-strong-panel .er-boss-affinity-list')),
      'weaker_to': self.link_texts(infobox.css('.er-boss-weak-panel .er-boss-affinity-list')),
      'game': self.game_name
    }

  def link_texts(self, selector):
    return dedupe([text.strip() for text in selector.css('a::text').getall() if text.strip()])
