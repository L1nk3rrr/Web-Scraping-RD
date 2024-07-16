# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from utils.str_utils import remove_special_quotes


class QuotesPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['text'] = remove_special_quotes(adapter.get('text', ''))
        return item
