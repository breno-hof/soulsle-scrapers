import scrapy
from ..utils.spider_utils import loop_selectors, sanitize_values, sanitize_value

class DarkSouls3WikiSpider(scrapy.Spider):
  name = "darksouls3_wiki"
  start_urls = ["https://darksouls3.wiki.fextralife.com/Bosses"]

  bad_values = ["(King of the Storm)",  "(Nameless King)", "(Boss)"]

  image_url_selectors = [
    "tr:nth-child(2) > td > img::attr(src)",
    "tr:nth-child(2) > td > a > img::attr(src)",
    "tr:nth-child(2) > td > div > img::attr(src)"
  ]

  drops_selectors = [
    "tr:nth-child(6) > td:nth-child(2) > a::text",
    "tr:nth-child(5) > td:nth-child(2) > a::text"
  ]

  stronger_vs_selectors = [
    "td:nth-child(5)::text",
    "td:nth-child(5) > p::text"
  ]

  weaker_to_selectors = [
    "td:nth-child(4)::text",
    "td:nth-child(4) > p::text",
  ]

  def parse(self, response):
    table_rows = response.css('.wiki_table tbody > tr')

    for row in table_rows:
      href = row.css('td:nth-child(1) > a::attr(href)').get()
      full_url = response.urljoin(href)

      name = row.css('td:nth-child(1) > a::text').get()
      areas = row.css('td:nth-child(2) > a::text').getall()

      if areas == []:
        areas = row.css('td:nth-child(2) > p:nth-child(1) > a::text')

      stronger_vs = loop_selectors(html=row, selectors=self.stronger_vs_selectors)
      weaker_to = loop_selectors(html=row, selectors=self.weaker_to_selectors)

      yield scrapy.Request(full_url, callback=self.parse_image_url, meta={
        'name': sanitize_value(value=name, bad_values=self.bad_values),
        'areas': areas,
        'stronger_vs': sanitize_values(stronger_vs, bad_values=self.bad_values),
        'weaker_to': sanitize_values(weaker_to, bad_values=self.bad_values),
      })
  
  def parse_image_url(self, response):
    table = response.css('#infobox > div > table > tbody')

    image_url = loop_selectors(html=table, selectors=self.image_url_selectors)
    drops = loop_selectors(html=table, selectors=self.drops_selectors)

    yield {
      'name': response.meta['name'],
      'image_url': image_url,
      'areas':  response.meta['areas'],
      'drops': drops,
      'stronger_vs': self.split_conditional(value=response.meta["stronger_vs"]),
      'weaker_to': self.split_conditional(value=response.meta["weaker_to"]),
      'game': 'Dark Souls 3'
    }
  
  def split_conditional(self, value):
    if type(value) == list:
      value = ''.join(value)

    if ',' in value:
      return value.split(',')
    
    return value.split('/')
