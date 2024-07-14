import sqlite3


class SqLitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('crypto.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
                create table if not exists crypto (
                    name text,
                    price text,
                    write_date DEFAULT (datetime('now','localtime'))
                )
            """
        )
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute(
            """
                insert into crypto (name, price) values (?, ?)
            """, (item['name'], item['price'])
        )
        self.connection.commit()
        return item
