from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from buscalibre_funciones import *
import re
import os
import requests # to get image from the web
import shutil # to save it locally
import urllib.request


try:
    html = urlopen("https://www.buscalibre.cl/")
except HTTPError as e:
    print(e)
else:
    bsObj = BeautifulSoup(html.read(),"html.parser")
    #Se busca el tag <p> que tiene como título las categorías
    tagInicialCategorias = bsObj.find("p", string="categoria")
    #Subimos al nivel del padre
    parent_tag = tagInicialCategorias.parent
    #Sabemos que el siguiente tag es <ul> para el listado de categorías
    td_tag = parent_tag.parent
    next_td_tag = td_tag.findNext('ul')
    #Buscamos todos los hijos de ese <ul> y los almacenamos en un CSV
    for child in next_td_tag.children:
        g = open('cat_libros.csv', 'a', encoding='utf-8')
        caturl = 'https://www.buscalibre.cl'+child.findNext('a').attrs["href"]
        catname = child.get_text()
        g.write(catname+';'+caturl)
        g.write('\n')
        navega_categoria(caturl, catname)
    ## FIN DE LA PRIMERA PARTE ##p