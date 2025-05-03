import scrapy
from ..utils.spider_utils import loop_selectors

class BloodborneWikiSpider(scrapy.Spider):
  name = "bloodborne_wiki"
  start_urls = ["https://bloodborne.wiki.fextralife.com/Bosses", "https://bloodborne.wiki.fextralife.com/Chalice+Dungeon+Bosses", "https://bloodborne.wiki.fextralife.com/The+Old+Hunters+Bosses"]
  
  bad_hrefs = ["/Defiled+Chalice", "/Pthumeru+Ihyll+Root+Chalice"]

  areas_selectors = [
    "tbody > tr:nth-child(6) > td:nth-child(3) > a::text",
    "tbody > tr:nth-child(5) > td:nth-child(3) > a::text",
    "tbody > tr:nth-child(4) > td:nth-child(3) > a::text",
    "tbody > tr:nth-child(5) > td:nth-child(3)::text"
  ]

  drops_selectors = [
    "tbody > tr:nth-child(6) > td:nth-child(4) > a::text",
    "tbody > tr:nth-child(5) > td:nth-child(4) > a::text",
    "tbody > tr:nth-child(4) > td:nth-child(4) > a::text",
    "tbody > tr:nth-child(5) > td:nth-child(4)::text"
  ]

  def parse(self, response):
    for link in response.css('div.tabcurrent  div.row ul li a.wiki_link'):
      href = link.css('::attr(href)').get()

      if href not in self.bad_hrefs:
        full_url = response.urljoin(href)
        yield scrapy.Request(full_url, callback=self.parse_boss)
  
  def parse_boss(self, response):
    table = response.css('#infobox .wiki_table')
    name = table.css('h2::text').get()
    
    if name == None:
      name = table.css('tbody > tr:nth-child(1) > th > h2 > span').get()

    image_url = table.css('tbody > tr:nth-child(2) > td img::attr(src)').get()
    
    if image_url == None:
      image_url = table.css('tbody > tr:nth-child(1) > td img::attr(src)').get()

    areas = loop_selectors(html=table, selectors=self.areas_selectors)
    drops = loop_selectors(html=table, selectors=self.drops_selectors)
    
    yield {
      'name': name.strip(),
      'image_url': image_url,
      'areas': areas,
      'drops': drops,
      'stronger_vs': [],
      'weaker_to': [],
      'game': 'Bloodborne'
    }