#!/usr/bin/env python

import pandas as pd
import numpy as np


def get_products_filtered(categories=None):
	'''
	Indata
	Antingen skickas None in (pythons version av NULL) via categories och daa skall alla produkter haemtas.
	Om categories inte aer None, skickas en dicitonary in med gender, type och subtype.
	gender aer plaggets maalgrupps koen, type representerar huvudkategorin, subtype subkategorin.

	Returdata
	En lista av produkter. Respektive produkts information finns i en dictionary med foeljande nycklar:
	id: Det unika artikelnumret
	brand: Maerket paa produkten
	type: Typ av plagg, huvudkategori.
	subtype: Typ av plagg, subkategori
	color: Plaggets faerg
	gender: Koen
	price: Priset paa plagget
	size: Storleken paa plagget

	Exempelvis:
	[{'id': 1, 'brand': 'WESC', 'type': 'Shirt, 'subtype': 'T-shirt', 'color': 'Red', 'gender': 'Female', 'price': 299, 'size': 'M'},
	...,
	{'id': 443, 'brand': 'Cheap Monday', 'type': 'Pants, 'subtype': 'Jeans', 'color': 'Black', 'gender': 'Male', 'price': 449, 'size': 'S'}]

	'''
	
	df = pd.read_csv('data/Products.csv')
	if categories is not None:
		for category in categories.keys():
			df = df[df[category] == categories[category]]
	''' SQL '''

	return df.to_dict('records')

def get_products_search(values):
	'''
	Indata
	En lista (array) utav straengar (enskilda ord) som skall matchas mot maerket paa alla typer av produkter.
	
	Returdata
	En lista av produkter. Respektive produkts information finns i en dictionary med foeljande nycklar:
	id: Det unika artikelnumret
	brand: Maerket paa produkten
	type: Typ av plagg, huvudkategori.
	subtype: Typ av plagg, subkategori
	color: Plaggets faerg
	gender: Koen
	price: Priset paa plagget
	size: Storleken paa plagget

	Exempelvis:
	[{'id': 1, 'brand': 'WESC', 'type': 'Shirt, 'subtype': 'T-shirt', 'color': 'Red', 'gender': 'Female', 'price': 299, 'size': 'M'},
	...,
	{'id': 443, 'brand': 'Cheap Monday', 'type': 'Pants, 'subtype': 'Jeans', 'color': 'Black', 'gender': 'Male', 'price': 449, 'size': 'S'}]

	'''

	df = pd.read_csv('data/Products.csv')
	df = df[df['brand'].str.contains('(?i)' + '|'.join(values))]
	''' SQL '''

	return df.to_dict('records')

def get_products_ids(ids):
	'''
	Indata
	En lista (array) utav heltal som representerar artikelnummer paa produkter.

	Returdata
	En lista av produkter. Respektive produkts information finns i en dictionary med foeljande nycklar:
	id: Det unika artikelnumret
	brand: Maerket paa produkten
	type: Typ av plagg, huvudkategori.
	subtype: Typ av plagg, subkategori
	color: Plaggets faerg
	gender: Koen
	price: Priset paa plagget
	size: Storleken paa plagget

	Exempelvis:
	[{'id': 1, 'brand': 'WESC', 'type': 'Shirt, 'subtype': 'T-shirt', 'color': 'Red', 'gender': 'Female', 'price': 299, 'size': 'M'},
	...,
	{'id': 443, 'brand': 'Cheap Monday', 'type': 'Pants, 'subtype': 'Jeans', 'color': 'Black', 'gender': 'Male', 'price': 449, 'size': 'S'}]

	'''

	df = pd.read_csv('data/Products.csv')
	df = df.loc[df['id'].isin(ids)]
	''' SQL '''

	return df.to_dict('records')

def get_categories():
	'''
	Returdata
	En lista innehaallande dictionaries med nycklarna title och children.
	title representerar koenet plaggen aer gjorda foer (t.ex. Dam och Herr).
	children skall haalla en lista utav ytterligare dictionary object, daer varje dictionary 
	innehaaller nycklarna url och name.
	url tilldelar ni en tom straeng (d.v.s. '') och nyckeln name tilldelar ni en huvudkategori.


	Exempelvis:
	[{'title': 'Dam', 'children': [{'url': '', 'name': 'Troejor'}, {'url': '', 'name': 'Byxor'}]},
	{'title': 'Herr', 'children': [{'url': '', 'name': 'Troejor'}, {'url': '', 'name': 'Vaeskor'}]}]

	'''

	df = pd.read_csv('data/Products.csv')
	genders = df['gender'].unique()
	types = [df[(df['gender'] == genders[0])]['type'].unique().tolist(), df[(df['gender'] == genders[1])]['type'].unique().tolist()]
	children = [[{'url': '', 'name': name} for name in types[0]],[{'url': '', 'name': name} for name in types[1]]]
	''' SQL '''

	result = [{'title' : genders[0], 'children': children[0]}, {'title': genders[1], 'children': children[1]}]
	return result

def get_subcategories(gender, category):
	'''
	Indata
	Tvaa straengar, gender och category, daer gender aer koenet som det efterfraagas klaeder foer
	och category aer huvudkategorin vars subkategorier vi vill haemta.

	Returdata
	En lista innahaallande dictionaries med nycklarna gender, category, och children.
	gender representerar koenet plaggen aer gjorda foer (t.ex. Dam och Herr).
	category aer den inkommande kategorin vi haemtar subkategorier foer
	children skall haalla en lista utav ytterligare dictionary object, daer varje dictionary 
	innehaaller nycklarna url och name.
	url tilldelar ni en tom straeng (d.v.s. '') och nyckeln name tilldelar ni en subkategori.

	Exempelvis:
	[{'gender': 'Dam', 'category': 'Troejor', 'children': [{'url': '', 'name': 'T-shirts'}, {'url': '', 'name': 'Linnen'}]}]

	'''

	df = pd.read_csv('data/Products.csv')
	types = df[(df['gender'] == gender) & (df['type'] == category)]['subtype'].unique().tolist()
	children = [{'url': '', 'name': name} for name in types]
	result = [{'gender' : gender, 'category': category, 'children': children}]
	''' SQL '''

	return result

def write_order(order):
	'''
	Indata
	order som aer en dictionary med nycklarna och dess motsvarande vaerden:
	town: Kundens stad
	name: Kundens namn
	zipcode: Kundens postkod
	address: Kundens address
	email: Kundens email
	items: En lista av heltal som representerar alla produkters artikelnummer. Saa maanga gaanger
		ett heltal finns i listan, saa maanga artiklar av den typen har kunden koept. Exempelvis:
		[1,2,2,3]. I den listan har kunden koept 1 styck av produkt 1, 2 styck av produkt 2, och 1
		styck av produkt 3.
	'''

	df_orders = pd.read_csv('data/Orders.csv')
	# Get new order ID
	orderID = df_orders['orderid'].max() + 1
	# Grab the products id number and the amount of each product
	item_ids = list(map(int, order['items'].strip('[]').split(',')))
	items = [{'id': int(x), 'amount': item_ids.count(x)} for x in list(set(item_ids))]

	# Get the name and so on for the customer.
	try:
		firstname, lastname = order['name'].split()
	except:
		firstname = order['name']
		lastname = ''
	email = order['email']
	address = order['address']
	zipcode = order['zipcode']
	town = order['town']

	# Write the actual order
	df_products = pd.read_csv('data/Products.csv')
	for item in items:
		product = df_products[df_products['id'] == item['id']].to_dict('records')[0]
		df_orders.loc[len(df_orders)] = [orderID, firstname, lastname, address, town, zipcode, product['id'], product['brand'], product['type'], product['subtype'], product['color'], product['gender'], product['price'], product['size'], item['amount']]
	df_orders.to_csv('data/Orders.csv', index=False)


def get_20_most_popular():
	'''
	Returdata
	En lista av de 20 produkter som aer mest saalda i webshopen. 
	Respektive produkts information finns i en dictionary med foeljande nycklar:
	id: Det unika artikelnumret
	brand: Maerket paa produkten
	type: Typ av plagg, huvudkategori.
	subtype: Typ av plagg, subkategori
	color: Plaggets faerg
	gender: Koen
	price: Priset paa plagget
	size: Storleken paa plagget

	Exempelvis:
	[{'id': 1, 'brand': 'WESC', 'type': 'Shirt, 'subtype': 'T-shirt', 'color': 'Red', 'gender': 'Female', 'price': 299, 'size': 'M'},
	...,
	{'id': 443, 'brand': 'Cheap Monday', 'type': 'Pants, 'subtype': 'Jeans', 'color': 'Black', 'gender': 'Male', 'price': 449, 'size': 'S'}]

	'''
	df = pd.read_csv('data/Orders.csv')
	top20_ids = df.groupby(['id']).sum().loc[:,['amount']].sort_values('amount', ascending=False).iloc[:20].index.tolist()
	df = pd.read_csv('data/Products.csv')

	return df.iloc[top20_ids,:].to_dict('records')


def main():
	#test = get_products_filtered({'type': 'Bags', 'subtype': 'Leather bag'})
	#test = get_products_ids([1,2,3])
	#test = get_categories()
	#test = get_subcategories('Female', 'Bags')
	test = get_20_most_popular()
	#write_order({'town': 'asad', 'name': 'asd asd', 'items': '[2160,2160,2160,2160,2160,2160,2160,2160,2160]', 'zipcode': '123123', 'address': 'asd', 'email': 'asd'})
	#test = get_products_search(['jack', 'and', 'jones'])
	print(test)

if __name__ == '__main__':
	main()
