# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import os
from itemadapter import ItemAdapter
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class SoulsWikiScrapersPipeline:
  def __init__(self):
    self.connection = None
    self.cursor = None

  def open_spider(self, spider):
    self.connection = psycopg2.connect(
      host=os.getenv('SOULSBORNE_HOST', 'localhost'),
      database=os.getenv('SOULSBORNE_DB', 'nome_da_base'),
      user=os.getenv('SOULSLE_USER', 'seu_usuario'),
      password=os.getenv('SOULSLE_PASSWORD','sua_senha')
    )
    self.cursor = self.connection.cursor()

  def close_spider(self, spider):
    self.cursor.close()
    self.connection.close()

  def process_item(self, item, spider):
    try:
      self.cursor.execute(
        """
        INSERT INTO soulsborne_bosses (name, image_url, areas, drops, stronger_vs, weaker_to, game)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (name, game) DO NOTHING;
        """,
        (
            item['name'],
            item['image_url'],
            item['areas'],
            item['drops'],
            item['stronger_vs'],
            item['weaker_to'],
            item['game']
        )
      )
      self.connection.commit()
    except Exception as ex:
      print(ex)
      self.connection.rollback()
    return item
