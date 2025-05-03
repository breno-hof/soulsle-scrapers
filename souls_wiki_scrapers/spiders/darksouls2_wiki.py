import scrapy
from ..utils.spider_utils import sanitize_values

class DarkSouls2WikiSpider(scrapy.Spider):
  name = "darksouls2_wiki"
  start_urls = ["https://darksouls2.wiki.fextralife.com/Bosses"]

  def parse(self, response):
    table_rows = response.css('.wiki_table tbody > tr')

    for row in table_rows:
      href = row.css('td:nth-child(1) > a::attr(href)').get()
      full_url = response.urljoin(href)

      yield response.follow(full_url, callback=self.parse_image_url, meta={
        'name': row.css('td:nth-child(1) > a::text').get(),
        'areas': row.css('td:nth-child(3) > a::text').getall(),
        'drops': row.css('td:nth-child(4) > a::text').getall(),
        'stronger_vs': row.css('td:nth-child(5)::text').get().split(','),
        'weaker_to': row.css('td:nth-child(6)::text').get().split(',')
      })
  
  def parse_image_url(self, response):
    image_url = response.css('#infobox > div > table > tbody > tr:nth-child(2) > td > img::attr(src)').get()

    if image_url == None:
      image_url = response.css('#infobox > div > table > tbody > tr:nth-child(2) > td > a > img::attr(src)').get()
    
    yield {
      'name': response.meta['name'],
      'image_url': image_url,
      'areas':  response.meta['areas'],
      'drops': response.meta['drops'],
      'stronger_vs': sanitize_values(response.meta['stronger_vs']),
      'weaker_to': sanitize_values(response.meta['weaker_to']),
      'game': 'Dark Souls 2'
    }