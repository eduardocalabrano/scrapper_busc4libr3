import sqlite3
from datetime import date


con = sqlite3.connect("buscalibre_{}.db".format(date.today()))
cur = con.cursor()

def check_tables():
    cur.execute("CREATE TABLE IF NOT EXISTS category (name varchar(50) PRIMARY KEY, url varchar(200))")
    cur.execute("CREATE TABLE IF NOT EXISTS book_category (productId varchar(30) PRIMARY KEY, main_category varchar(50))")
    cur.execute("CREATE TABLE IF NOT EXISTS book_detail (productId varchar(30) PRIMARY KEY, book_name varchar(200), pricenow integer, pricebefore integer, format_text varchar(20), author varchar(50), editorial varchar(50), language varchar(10), pages integer, bookbinding varchar(20), isbn varchar(30), isbn13 varchar(30), scrapp_date date)")

def insert_categories(caturl, catname):
    try:
        string_query = "INSERT INTO category VALUES('{}', '{}')".format(catname, caturl)
        cur.execute(string_query)
        con.commit()
    except Exception as e:
        pass

def insert_book_x_category(productid, catname):
    try:
        string_query = "INSERT INTO book_category VALUES('{}', '{}')".format(productid, catname)
        cur.execute(string_query)
        con.commit()
    except Exception as e:
        pass

def insert_book_detail(book_dict):
    print(book_dict)
    try:
        string_query = "INSERT INTO book_detail VALUES('{}', '{}', {}, {}, '{}', '{}', '{}', '{}', {}, '{}', '{}', '{}', '{}')".format(
            book_dict['productId'],
            book_dict['bookname'],
            int(book_dict['pricenow']),
            int(book_dict['pricebefore']),
            book_dict['format_text'],
            book_dict['autor_text'],
            book_dict['editorial_text'],
            book_dict['language_text'],
            int(book_dict['pages']),
            book_dict['binding'],
            book_dict['isbn'],
            book_dict['isbn13'],
            book_dict['scrapp_date']
        )
        cur.execute(string_query)
        con.commit()
    except Exception as e:
        pass


