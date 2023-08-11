from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from datetime import date
import re
import os
import requests # to get image from the web
import shutil # to save it locally
import urllib.request

images_path = r'C:\Users\Eduardo\Desktop\django\scrapping\buscalibre\books_images'

def store_image(picture_url, name):
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    response = requests.get(picture_url)
    if(response.status_code == 200):
        format_name = re.sub('[^a-zA-Z0-9 \n\.]', '', name)
        foldername = images_path+'\{}.jpg'.format(format_name[:30])
        with open(foldername, "wb") as f:
                f.write(response.content)

def book_detail(bookurl):
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
        tariff_zone = general_info_zone.find("div", {"class":"box-precio-compra"})
        concat_detail = "{}".format(bookname.replace('\n', ''))
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
            concat_detail = "{};{}".format(concat_detail, pricenow.replace('\n', '').strip())
        else:
            concat_detail = "{};".format(concat_detail)

        #Precio antes
        pricebefore = tariff_zone.find("p",{"class":"precioAntes"})
        if pricebefore is not None:
            pricebefore = pricebefore.get_text()
            concat_detail = "{};{}".format(concat_detail, pricebefore.replace('\n', '').strip())
        else:
            concat_detail = "{};".format(concat_detail)

        #Formato del libro
        if exists_format is not None:
            if(exists_format.get_text() == 'Formato'):
                format_text = ficha.find("div",{"class":"col-xs-7"}).find("div",{"class":"box"}).get_text()
                concat_detail = "{};{}".format(concat_detail, format_text.replace('\n', '').strip())
        else:
            concat_detail = "{};".format(concat_detail)

        #Autor
        autor_text = ficha.find("div",{"id":"metadata-autor"}).a
        if autor_text is not None:
            autor_text = autor_text.get_text()
            concat_detail = "{};{}".format(concat_detail, autor_text.replace('\n', '').strip())
        else:
            concat_detail = "{};".format(concat_detail)

        #Editorial
        editorial_text = ficha.find("div",{"id":"metadata-editorial"}).a
        if editorial_text is not None:
            editorial_text = editorial_text.get_text()
            concat_detail = "{};{}".format(concat_detail, editorial_text.replace('\n', '').strip())
        else:
            concat_detail = "{};".format(concat_detail)

        #Idioma
        language_text = ficha.find("div",{"id":"metadata-idioma"})
        if language_text is not None:
            language_text = language_text.get_text()
            concat_detail = "{};{}".format(concat_detail, language_text.replace(" ", "").replace('\n', ''))
        else:
            concat_detail = "{};".format(concat_detail)

        #Num de páginas
        pages_text = ficha.find("div",{"id":"metadata-número páginas"})
        if pages_text is not None:
            pages_text = pages_text.get_text()
            concat_detail = "{};{}".format(concat_detail, pages_text.replace(" ", "").replace('\n', ''))
        else:
            concat_detail = "{};".format(concat_detail)

        #Encuadernación
        enc_text = ficha.find("div",{"id":"metadata-encuadernación"})
        if enc_text is not None:
            enc_text = enc_text.get_text()
            concat_detail = "{};{}".format(concat_detail, enc_text.replace('\n', '').strip())
        else:
            concat_detail = "{};".format(concat_detail)

        #ISBN
        isbn_text = ficha.find("div",{"id":"metadata-isbn"})
        if isbn_text is not None:
            isbn_text = isbn_text.get_text()
            concat_detail = "{};{}".format(concat_detail, isbn_text.replace(" ", "").replace('\n', ''))
        else:
            concat_detail = "{};".format(concat_detail)

        #ISBN13
        isbn13_text = ficha.find("div",{"id":"metadata-isbn13"})
        if isbn13_text is not None:
            isbn13_text = isbn13_text.get_text()
            concat_detail = "{};{}".format(concat_detail, isbn13_text.replace(" ", "").replace('\n', ''))
        else:
            concat_detail = "{};".format(concat_detail)
        concat_detail = "{};{}".format(concat_detail, date.today())
        print(concat_detail)
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
                    titulo = child.a.attrs["title"]
                    bookurl = child.a.attrs["href"]
                    autor = child.a.find("div", {"class": "autor"}).get_text()
                    precio = child.a.find("div", {"class": "box-precio-v2 row margin-top-10 hide-on-hover"}).find("div", {"class":"box-precios col-xs-7 text-align-right padding-left-0"}).find("p",{"class":"precio-ahora"}).strong.get_text()
                    precio = precio.replace(" ", "")
                    g = open('libros_por_categoria.csv', 'a', encoding='utf-8')
                    g.write(name+';'+titulo.strip()+';'+autor+";"+precio+";"+bookurl)
                    g.write('\n')
                    g.close()
                    book_detail(bookurl)
                except AttributeError as e:
                    #print(e)
                    pass