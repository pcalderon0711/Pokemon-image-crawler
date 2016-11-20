import os
import requests
from bs4 import BeautifulSoup

url = 'http://pokemondb.net/pokedex/all'
poke_folder = os.makedirs('poke_images', exist_ok = True)
soup = BeautifulSoup(requests.get(url).text)

poke_links = soup.select('.ent-name')

prev_url = None
for link in poke_links:
	poke_url = link['href']
	number = link['title'][18:21]
	if prev_url == poke_url: continue
	name = link.text
	poke_soup = BeautifulSoup(requests.get(url[:-12] + poke_url).text)
	img_urls = poke_soup.select('div > ul > li > div > div > img')
	for index, img_url in enumerate(img_urls):
		print('Downloading image of', name)
		res = requests.get(img_url['src'])
		img_file = open(os.path.join('poke_images', number+'_'+name+'_'+str(index)+'.jpg'), 'wb')
		for chunk in res.iter_content(100000):
			img_file.write(chunk)
		img_file.close()
	prev_url = poke_url