import scrapy
from ..utils.spider_utils import loop_selectors

class DarkSoulsWikiSpider(scrapy.Spider):
  name = "darksouls_wiki"
  start_urls = ["https://darksouls.wiki.fextralife.com/Area+Bosses", "https://darksouls.wiki.fextralife.com/Mini+Bosses", "https://darksouls.wiki.fextralife.com/Expansion+Bosses"]
  
  areas_selectors = [
    "tr:nth-child(3) > td:nth-child(2) > a::text",
    "tr:nth-child(3) > td:nth-child(3) > a::text",
    "tr:nth-child(3) > td > a::text",
    "tr:nth-child(3) > td:nth-child(2) > span > a::text",
    "tr:nth-child(2) > td:nth-child(2) > a::text",
    "tr:nth-child(3) > td:nth-child(2)::text"
  ]

  drops_selectors = [
    "#wiki-content-block > div:nth-child(17) > div:nth-child(1) > ul > li > a:nth-child(1)::text",
    "#wiki-content-block > ul > li > span > a::text",
    "#wiki-content-block > ul > li > a::text",
    "#wiki-content-block > div.hpwidget > ul > li > a::text",
    "#wiki-content-block > div:nth-child(11) > div:nth-child(1) > ul > li > a::text",
    "#wiki-content-block > div.row > div:nth-child(1) > ul > li > a::text",
    "#wiki-content-block > div:nth-child(7) > table > tbody > tr > td:nth-child(2) > a::text"
  ]

  resistances_selectors = [
    "#wiki-content-block > div:nth-child(15) > table > tbody",
    "#wiki-content-block > div:nth-child(13) > table > tbody",
    "#wiki-content-block > div:nth-child(11) > table > tbody",
    "#wiki-content-block > div:nth-child(14) > table > tbody",
    "#wiki-content-block > div.hpwidget > div:nth-child(7) > table > tbody",
    "#wiki-content-block > div:nth-child(12) > table > tbody"
  ]

  def parse(self, response):
    for link in response.css('#wiki-content-block > div > h3 > a'):
      href = link.css('::attr(href)').get()

      full_url = response.urljoin(href)
      yield scrapy.Request(full_url, callback=self.parse_boss)
  
  def parse_boss(self, response):
    table = response.css('#infobox .wiki_table')
    name = table.css('h2::text').get()

    if name == None:
      name = table.css('tbody > tr:nth-child(1) > th::text').get()
    
    if name == None:
      name = table.css('thead > tr > th > h3::text').get()

    image_url = table.css('tbody > tr:nth-child(2) > td img::attr(src)').get()
    
    if image_url == None:
      image_url = table.css('tbody > tr:nth-child(1) > td img::attr(src)').get()

    areas = loop_selectors(html=table, selectors=self.areas_selectors)

    if areas[0] == "237":
      areas = ["New Londo Ruins "]
    
    if areas[0] == "184 ~":
      areas = ["Crystal Cave"]
    
    if areas[0] == "281 ~":
      areas = ["Multiple"]

    drops = loop_selectors(html=response, selectors=self.drops_selectors)
    stronger_vs = loop_selectors(html=response, selectors=self.resistances_selectors)
    
    if image_url == '/file/Dark-Souls/tumblr_lxlmomDlzY1qgjlhf.jpg':
      name = table.css("tbody > tr:nth-child(1) > th > h3::text").get()
      areas = ["Anor Londo"]

    yield {
      'name': name.strip(),
      'image_url': image_url,
      'areas': areas,
      'drops': drops,
      'stronger_vs': stronger_vs,
      # 'weaker_to': weaker_to,
      'game': 'Dark Souls'
    }
