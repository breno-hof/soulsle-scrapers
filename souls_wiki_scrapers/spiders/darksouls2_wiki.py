import scrapy
from ..utils.spider_utils import cell_values, clean_text, table_records

class DarkSouls2WikiSpider(scrapy.Spider):
  name = "darksouls2_wiki"
  # The comparison table on /Bosses is lazy-loaded from this subpage
  start_urls = ["https://darksouls2.wiki.fextralife.com/Subcontent:Bosses_3_Bosses_Comparison_Table"]

  def parse(self, response):
    for record in table_records(response.css('.mw-parser-output table')):
      href = record['name'].css('a::attr(href)').get()

      if href == None:
        continue

      yield response.follow(href, callback=self.parse_image_url, meta={
        'name': clean_text(record['name']),
        'areas': cell_values(record['location']),
        'drops': cell_values(record['soul dropped']),
        'stronger_vs': cell_values(record['resistance']),
        'weaker_to': cell_values(record['weakness'])
      })

  def parse_image_url(self, response):
    yield {
      'name': response.meta['name'],
      'image_url': response.css('#infobox table img::attr(src)').get(),
      'areas':  response.meta['areas'],
      'drops': response.meta['drops'],
      'stronger_vs': response.meta['stronger_vs'],
      'weaker_to': response.meta['weaker_to'],
      'game': 'Dark Souls 2'
    }
