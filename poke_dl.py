import os
import requests
from collections import Counter
from bs4 import BeautifulSoup

url = 'http://pokemondb.net/pokedex/all'
poke_folder = os.makedirs('poke_images', exist_ok = True)
soup = BeautifulSoup(requests.get(url).text)

poke_links = soup.select('.ent-name')
nicknames = {}
top_words = {}

prev_url = None
for link in poke_links[-10:]:
	poke_url = link['href']
	number = link['title'][18:21]
	if prev_url == poke_url: continue
	name = link.text
	poke_soup = BeautifulSoup(requests.get(url[:-12] + poke_url).text)
	nicknames[name] = poke_soup.select('q')[0].text
	descriptions_html = poke_soup.select('table.vitals-table')[-2]
	description_list = []
	for description in descriptions_html:
		description_list.extend(description.text.split())
	dl = []
	for poke, count in dict(Counter(description_list)).items():
		dl.append((count,poke))
	dl.sort(reverse = True)
	top_words[name] = dl[:5]
	img_urls = poke_soup.select('div > ul > li > div > div > img')
	for index, img_url in enumerate(img_urls):
		print('Downloading image of', name)
		res = requests.get(img_url['src'])
		img_file = open(os.path.join('poke_images', number+'_'+name+'_'+str(index)+'.jpg'), 'wb')
		for chunk in res.iter_content(100000):
			img_file.write(chunk)
		img_file.close()
	prev_url = poke_url