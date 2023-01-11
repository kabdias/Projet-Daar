from django.shortcuts import render
from ProjetDaar.utils import *
from django.core.files.storage import FileSystemStorage
from elasticsearch import Elasticsearch
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http import HttpResponse

index_name='books3'

class Home(TemplateView):
	template_name = 'interface.html'

def search(request):
	sortby='crank:desc'
	if (request.POST.get("scorebox")=="on"):
		sortby='_score'
		print("scorebox activated")
	elastic_client = Elasticsearch(hosts=["127.0.0.1"])
	if request.method == "POST":
		content=request.POST.get("content")
		if(request.POST.get("advenced")=="on"): 
			payload = json.dumps({
                "query": {
                "regexp": {
                "content": content+".*"
                }
                },
                "size": "2000"
            })
		else:
			payload = json.dumps({
                "query": {
                "match": {
                "content": content
                }
                },
                "size": "2000"
            })

	response=elastic_client.search(index=index_name, body=payload,sort=sortby)
	
	li= []
	suggest = []
	k = 0
	for i in response['hits']['hits']:
		l=[]
		l.append(i['_source']['title'])
		l.append(i['_source']['author'])
		l.append(i['_source']['Id'])
		if k < 3 and i['_source']['neighbors']:
			for document in i['_source']['neighbors'] :
				s = []
				s.append(i['_source']['title_neigh'][str(document)])
				s.append(i['_source']['author_neigh'][str(document)])
				s.append(str(document))
				suggest.append(s)
		li.append(l)
		k += 1
	rm = []
	print("suggérés --- ", suggest)
	for a in suggest :
		if a in li :
			rm.append(a)
	for r in rm :
		suggest.remove(r)

	print("resultats --- ", li)
	return render(request, 'suggestion.html', {'resp': content,'list':li, 'suggestions' : suggest})
    

