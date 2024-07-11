import psycopg2
import requests
import json


connect = {
    'database': 'n48group',
    'user': 'postgres',
    'host': 'localhost',
    'password': '112',
    'port': 5432
}

product_url = requests.get('https://dummyjson.com/products')
product_list = product_url.json()['products']

class CManager:
    def __init__(self):
        self.connect = psycopg2.connect(**connect)

    def __enter__(self):
        self.cur = self.connect.cursor()
        return self.connect, self.cur

    @staticmethod
    def create_table():
        table_query = '''CREATE TABLE products(
                id SERIAL PRIMARY KEY,
                title VARCHAR(300) NOT NULL,
                description TEXT NOT NULL,
                category VARCHAR(300) NOT NULL,
                price REAL,
                discountPercentage REAL,
                rating REAL,
                stock INT,
                tags TEXT,
                sku VARCHAR(300) NOT NULL,
                weight INT
        );'''
        return table_query

    @staticmethod
    def add_information():
        query = '''INSERT INTO products(title, description, category, price, discountPercentage, rating, stock, tags, sku, weight)
                   VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        return query

    @staticmethod
    def select_query():
        select_query = '''SELECT * FROM products;'''
        return select_query

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cur:
            self.cur.close()
        if self.connect:
            self.connect.close()

# ========================================================
product_manager = CManager()

with product_manager as (conn, cur):
    while True:
        choice: str = input('create table => 1\nadd data => 2\ngit all products=> 3\nexit => q\n....: ')
        if choice == '1':
            table = CManager.create_table()
            cur.execute(table)
            conn.commit()
            print("created table")
        elif choice == '2':
            query = CManager.add_information()
            for product in product_list:
                tags = ', '.join(product['tags'])
                cur.execute(query, (product['title'], product['description'], product['category'], product['price'],
                                    product['discountPercentage'], product['rating'], product['stock'], tags,
                                    product['sku'], product['weight']))
                conn.commit()
            print("add information")
        elif choice == '3':
            products = CManager.select_query()
            cur.execute(products)
            rows = cur.fetchall()
            for row in rows:
                print(row)
        elif choice == 'q':
            print("exit")
            break
        else:
            print("error")


















    

























