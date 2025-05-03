import scrapy

class EldenRingWikiSpider(scrapy.Spider):
  incremental_id = 0
  name = "eldenring_wiki"
  start_urls = ["https://eldenring.wiki.fextralife.com/Bosses"]
  bad_hrefs = ["Stormfoot Catacombs", "Sage's Cave", "Impaler's Catacombs", 
               "Liurnia Northeast", "Liurnia Southwest", "Liurnia North", 
               "Liurnia South", "Caelid", "Dragonbarrow", "Sainted Hero's Grave"]
  areas_selectors = [
    "tbody > tr:nth-child(3) > td:nth-child(2) a.wiki_link::text",
    "tbody > tr:nth-child(3) > td:nth-child(2)::text",
    "tbody > tr:nth-child(4) > td > p > strong > a::text",
    "tbody > tr:nth-child(4) > td > p > a:nth-child(1)::text",
    "tbody > tr:nth-child(4) > td > strong > a::text"
  ]
  drops_selectors = [
    "tbody > tr:nth-child(4) > td:nth-child(2) > a::text",
    "tbody > tr:nth-child(4) > td > p > a::text",
    "tbody > tr:nth-child(4) > td > a:nth-child(9)::text",
    "tbody > tr:nth-child(5) > td > a::text",
    "tbody > tr:nth-child(5) > td > p > a::text",
    "tbody > tr:nth-child(3) > td:nth-child(2) > a::text"
  ]
  stronger_vs_selectors = [
    "tbody > tr:nth-child(6) > td:nth-child(1) > div:nth-child(2) > a::text",
    "tbody > tr:nth-child(5) > td:nth-child(1) > div > a::text",
    "tbody > tr:nth-child(7) > td:nth-child(1) > div > a::text",
    "tbody > tr:nth-child(6) > td:nth-child(1) > div > a::text",
    "tbody > tr:nth-child(6) > td:nth-child(1) > div > a:nth-child(1) > span::text",
    "tbody > tr:nth-child(6) > td:nth-child(1) > div::text",
    "tbody > tr:nth-child(5) > td:nth-child(1) > div > a > span::text",
    "tbody > tr:nth-child(8) > td:nth-child(1) > div > a::text"
  ]
  weaker_to_selectors = [
    "tbody > tr:nth-child(6) > td:nth-child(2) > div > a::text",
    "tbody > tr:nth-child(5) > td:nth-child(2) > div > a::text",
    "tbody > tr:nth-child(7) > td:nth-child(2) > div > a::text",
    "tbody > tr:nth-child(6) > td:nth-child(2) > div > a > span::text",
    "tbody > tr:nth-child(6) > td:nth-child(2) > div::text",
    "tbody > tr:nth-child(5) > td:nth-child(2) > div > a > span::text",
    "tbody > tr:nth-child(8) > td:nth-child(2) > div > a::text",
    "tbody > tr:nth-child(5) > td:nth-child(2) > div > span > a::text",
    "tbody > tr:nth-child(5) > td:nth-child(3) > div > span > a::text"
  ]

  def parse(self, response):
    for link in response.css('div.tabcurrent  div.row ul li a.wiki_link'):
      text = link.css('::text').get()
      href = link.css('::attr(href)').get()

      if text not in self.bad_hrefs:
        full_url = response.urljoin(href)
        yield scrapy.Request(full_url, callback=self.parse_boss)
  
  def parse_boss(self, response):
    table = response.css('#infobox .wiki_table')
    name = table.css('h2::text').get()
    image_url = table.css('tbody > tr:nth-child(2) > td img::attr(src)').get()
    
    if image_url == None:
      image_url = table.css('tbody > tr:nth-child(1) > td img::attr(src)').get()

    areas = self.loop_selectors(html=table, selectors=self.areas_selectors)
    drops = self.loop_selectors(html=table, selectors=self.drops_selectors)
    stronger_vs = self.loop_selectors(html=table, selectors=self.stronger_vs_selectors)
    weaker_to = self.loop_selectors(html=table, selectors=self.weaker_to_selectors)
    
    self.incremental_id += 1
    yield {
      'id': self.incremental_id,
      'name': name.strip(),
      'image_url': image_url,
      'areas': areas,
      'drops': drops,
      'stronger_vs': stronger_vs,
      'weaker_to': weaker_to,
      'game': 'Elden Ring'
    }

  def loop_selectors(self, html, selectors):
    for selector in selectors:
      value = html.css(selector).getall()
      value = [item.strip() for item in value if item.strip()]

      if value != []:
        break
    
    return value