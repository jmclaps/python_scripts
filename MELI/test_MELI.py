#Importo las librerías
import requests
import pandas as pd

#Defino variables para llamar la API
site = 'MLA'
seller_id = '57995397'


itemsVendedor = requests.get('https://api.mercadolibre.com/sites/'+site+'/search?seller_id='+seller_id)

print(itemsVendedor.status_code)

diccItemsVendedor = itemsVendedor.json()

items = pd.DataFrame(columns =['item_id','title','category_id'])

for lista in diccItemsVendedor['results']:
    serieInsert = pd.Series([lista['id'],lista['title'],lista['category_id']],index =['item_id','title','category_id'])
    items = items.append(serieInsert, ignore_index=True)

categories = pd.DataFrame(columns =['category_id','name'])

for categoryId in items['category_id'].unique():
    categoriasGral = requests.get('https://api.mercadolibre.com/categories/'+categoryId)
    diccCategoriasGral = categoriasGral.json()
    serieCatInsert = pd.Series([diccCategoriasGral['id'],diccCategoriasGral['name']],index =['category_id','name'])
    categories = categories.append(serieCatInsert, ignore_index=True)


itemWithCategories = pd.merge(items,categories, left_on='category_id', right_on='category_id')

itemWithCategories.to_csv(path_or_buf='/Users/fengod/python_scripts/MELI/itemWithCategories.csv',index=False)

