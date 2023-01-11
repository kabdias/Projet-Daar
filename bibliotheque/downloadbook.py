import requests
import os


for i in range(66150,67250):
	url = 'https://www.gutenberg.org/cache/epub/'+str(i)+'/pg'+str(i)+'.txt'
	r = requests.get(url, allow_redirects=True)
	print(r)
	if str(r)=='<Response [200]>':
		print('yes')
		#print(r.content.decode('utf-8'))

		with open('pg'+str(i)+'.txt','w',encoding='utf-8') as f:
			f.write(r.content.decode('utf-8'))
	else:
		print(r)
		print('EEERRRROOOOOOOOOORRRRR')
		continue