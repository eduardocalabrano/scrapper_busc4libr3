from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from datetime import date
import re
import os
from dotenv import load_dotenv
from database_insertions import *
import requests # to get image from the web
import shutil # to save it locally
import urllib.request

load_dotenv()

images_path = os.getenv('BOOK_IMG_PATH')

def store_image(picture_url, name):
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    response = requests.get(picture_url)
    if(response.status_code == 200):
        format_name = re.sub('[^a-zA-Z0-9 \n\.]', '', name)
        foldername = images_path+'\{}.jpg'.format(format_name[:30])
        with open(foldername, "wb") as f:
                f.write(response.content)

def book_detail(bookurl, productid):
    bookdetail_dict = {
        "productId" : productid,
        "bookurl" : bookurl,
    }
    try:
        html_bookdetail = urlopen(bookurl)
    except HTTPError as e:
        print(e)
    else:
        info = BeautifulSoup(html_bookdetail.read(),"html.parser")
        concat_detail = ""
        detail_zone = info.find("div", {"class":"row product-info"}).find("div", {"class":"marcador"})
        general_info_zone = info.find("div", {"class":"row product-info"}).find("div", {"id":"data-info-libro"})
        bookname = general_info_zone.find("p", {"class":"tituloProducto"}).get_text()
        bookname = bookname.replace('\n', '')
        bookdetail_dict["bookname"] = bookname
        tariff_zone = general_info_zone.find("div", {"class":"box-precio-compra"})
        concat_detail = "{};{}".format(productid, bookname)
        url_img = detail_zone.find("div", {"class":"imagen"}).img
        url_img = url_img.attrs.get("data-src", url_img.attrs.get("src", None))
        if(url_img):
            store_image(url_img, bookname)
        ficha = detail_zone.find("div", {"class":"ficha font-weight-light font-size-small color-text"})
        exists_format = ficha.find("div",{"class":"box"})

        #Precio ahora
        pricenow = tariff_zone.find("p",{"class":"precioAhora"})
        if pricenow is not None:
            pricenow = pricenow.get_text()
            pricenow = pricenow.replace('$', '').replace('.', '').replace('\n', '').replace(" ", "").strip()
            concat_detail = "{};{}".format(concat_detail, pricenow)
        else:
            pricenow = ''
            concat_detail = "{};".format(concat_detail)
        bookdetail_dict["pricenow"] = pricenow

        #Precio antes
        pricebefore = tariff_zone.find("p",{"class":"precioAntes"})
        if pricebefore is not None:
            pricebefore = pricebefore.get_text()
            pricebefore = pricebefore.replace('$', '').replace('.', '').replace('\n', '').replace(" ", "").strip()
            concat_detail = "{};{}".format(concat_detail, pricebefore)
        else:
            pricebefore = ''
            concat_detail = "{};".format(concat_detail)
        bookdetail_dict["pricebefore"] = pricebefore

        #Formato del libro
        if exists_format is not None:
            if(exists_format.get_text() == 'Formato'):
                format_text = ficha.find("div",{"class":"col-xs-7"}).find("div",{"class":"box"}).get_text()
                format_text = format_text.replace('\n', '').strip()
                concat_detail = "{};{}".format(concat_detail, format_text)
        else:
            format_text = ''
            concat_detail = "{};".format(concat_detail)
        bookdetail_dict["format_text"] = format_text

        #Autor
        autor_text = ficha.find("div",{"id":"metadata-autor"}).a
        if autor_text is not None:
            autor_text = autor_text.get_text()
            autor_text = autor_text.replace('\n', '').strip()
            concat_detail = "{};{}".format(concat_detail, autor_text)
        else:
            autor_text = ''
            concat_detail = "{};".format(concat_detail)
        bookdetail_dict["autor_text"] = autor_text

        #Editorial
        editorial_text = ficha.find("div",{"id":"metadata-editorial"}).a
        if editorial_text is not None:
            editorial_text = editorial_text.get_text()
            editorial_text = editorial_text.replace('\n', '').strip()
            concat_detail = "{};{}".format(concat_detail, editorial_text)
        else:
            editorial_text = ''
            concat_detail = "{};".format(concat_detail)
        bookdetail_dict["editorial_text"] = editorial_text

        #Idioma
        language_text = ficha.find("div",{"id":"metadata-idioma"})
        if language_text is not None:
            language_text = language_text.get_text()
            language_text = language_text.replace(" ", "").replace('\n', '')
            concat_detail = "{};{}".format(concat_detail, language_text)
        else:
            language_text = ''
            concat_detail = "{};".format(concat_detail)
        bookdetail_dict["language_text"] = language_text

        #Num de páginas
        pages_text = ficha.find("div",{"id":"metadata-número páginas"})
        if pages_text is not None:
            pages_text = pages_text.get_text()
            pages_text = pages_text.replace(" ", "").replace('\n', '')
            concat_detail = "{};{}".format(concat_detail, pages_text)
        else:
            pages_text = ''
            concat_detail = "{};".format(concat_detail)
        bookdetail_dict["pages"] = pages_text

        #Encuadernación
        enc_text = ficha.find("div",{"id":"metadata-encuadernación"})
        if enc_text is not None:
            enc_text = enc_text.get_text()
            enc_text = enc_text.replace('\n', '').strip()
            concat_detail = "{};{}".format(concat_detail, enc_text)
        else:
            enc_text = ''
            concat_detail = "{};".format(concat_detail)
        bookdetail_dict["binding"] = enc_text

        #ISBN
        isbn_text = ficha.find("div",{"id":"metadata-isbn"})
        if isbn_text is not None:
            isbn_text = isbn_text.get_text()
            isbn_text = isbn_text.replace(" ", "").replace('\n', '')
            concat_detail = "{};{}".format(concat_detail, isbn_text)
        else:
            isbn_text = ''
            concat_detail = "{};".format(concat_detail)
        bookdetail_dict["isbn"] = isbn_text

        #ISBN13
        isbn13_text = ficha.find("div",{"id":"metadata-isbn13"})
        if isbn13_text is not None:
            isbn13_text = isbn13_text.get_text()
            isbn13_text = isbn13_text.replace(" ", "").replace('\n', '')
            concat_detail = "{};{}".format(concat_detail, isbn13_text)
        else:
            isbn13_text = ''
            concat_detail = "{};".format(concat_detail)
        bookdetail_dict["isbn13"] = isbn13_text

        scrapp_date = date.today()
        concat_detail = "{};{}".format(concat_detail, scrapp_date)
        bookdetail_dict["scrapp_date"] = scrapp_date
        insert_book_detail(bookdetail_dict)
        #print(concat_detail)
        f = open('detail_book.csv', 'a', encoding='utf-8')
        f.write(concat_detail)
        f.write('\n')
        f.close()

def navega_categoria(url, name):
    for page in range(1,201):
        pageurl = str(url+'?page='+str(page))
        html_detail = urlopen(pageurl)
        bsObj = BeautifulSoup(html_detail.read(),"html.parser")
        if(bsObj.find("section", {"id":"noEncontrado"})):
            print('pagina '+str(pageurl)+' no existe')
            continue
        else:
            booksdiv = bsObj.find("div", {"class":"productos pais42"})
            for child in booksdiv.children:
                try:
                    classname = child.attrs["class"]
                    if classname[0] != 'clear':
                        productid = child.attrs["data-id_producto"]
                        titulo = child.a.attrs["title"]
                        bookurl = child.a.attrs["href"]
                        autor = child.a.find("div", {"class": "autor"}).get_text()
                        precio = child.a.find("div", {"class": "box-precio-v2 row margin-top-10 hide-on-hover"}).find("div", {"class":"box-precios col-xs-7 text-align-right padding-left-0"}).find("p",{"class":"precio-ahora"}).strong.get_text()
                        precio = precio.replace(" ", "")
                        insert_book_x_category(productid, name)
                        g = open('libros_por_categoria.csv', 'a', encoding='utf-8')
                        g.write(productid+';'+name+';'+titulo.strip()+';'+autor+";"+precio+";"+bookurl)
                        g.write('\n')
                        g.close()
                        book_detail(bookurl, productid)
                except AttributeError as e:
                    print(e)
                    pass