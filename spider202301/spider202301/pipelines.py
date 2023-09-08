# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import openpyxl
import pymysql as pymysql
# 钩子函数 主动调用 无须手动
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
class Excel_Spider202301Pipeline:

    def __init__(self):
        self.wb=openpyxl.Workbook()
        self.ws=self.wb.active
        self.ws.title="top250"
        self.ws.append(('标题','评分','主题'))

    def close_spider(self,spider):
        self.wb.save("movie_data.xlsx")

    # 处理数据
    def process_item(self, item, spider):
        title=item.get('title','')
        rank=item.get('rank','')
        subject=item.get('subject','')
        self.ws.append((title,rank,subject))
        return item

class Db_Spider202301Pipeline:
    def __init__(self):
        self.conn=pymysql.connect(host="localhost",
                                  port=3306,
                                  user="root",
                                  password="123456",
                                  database="spider",
                                  charset="utf8mb4")
        self.cursor=self.conn.cursor()

    def close_spider(self,spider):
        self.conn.commit()
        self.conn.close()
    def process_item(self,item,spider):
        title = item.get('title', '')
        rank = item.get('rank', 0)
        subject = item.get('subject', '')
        self.cursor.execute(
            'insert into tb_top_movie (title,rating,subject) values (%s,%s,%s)',
            (title,rank,subject)
        )
        return item

