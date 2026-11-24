import scrapy
from ..utils.spider_utils import cell_values, clean_text, field_values, infobox_fields, sanitize_value, table_records

class DarkSouls3WikiSpider(scrapy.Spider):
  name = "darksouls3_wiki"
  start_urls = ["https://darksouls3.wiki.fextralife.com/Bosses"]

  bad_values = ["(King of the Storm)",  "(Nameless King)", "(Boss)"]

  def parse(self, response):
    for table in response.css('.mw-parser-output > table.wikitable'):
      for record in table_records(table):
        href = record['boss'].css('a::attr(href)').get()

        if href == None:
          continue

        yield response.follow(href, callback=self.parse_image_url, meta={
          'name': sanitize_value(value=clean_text(record['boss']), bad_values=self.bad_values),
          'areas': cell_values(record['location']),
          'stronger_vs': cell_values(record['resistance'], bad_values=self.bad_values),
          'weaker_to': cell_values(record['weakness'], bad_values=self.bad_values),
        })

  def parse_image_url(self, response):
    table = response.css('#infobox table')

    yield {
      'name': response.meta['name'],
      'image_url': table.css('img::attr(src)').get(),
      'areas':  response.meta['areas'],
      'drops': field_values(infobox_fields(table), ['drops']),
      'stronger_vs': response.meta['stronger_vs'],
      'weaker_to': response.meta['weaker_to'],
      'game': 'Dark Souls 3'
    }
