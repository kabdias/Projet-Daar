from elasticsearch import Elasticsearch
#from utils import *
import json
import nltk
nltk.download('punkt')
import json
import re
import glob
from pyvis.network import Network
import networkx as nx
import os

#print(ind)
# response = elastic.index(index='pdf', doc_type='pdfs', document=ind)
# print(response)

index_name='books3'

def extract_titles(txt):
	title = ""
	for sent in nltk.sent_tokenize(txt):
        
		if "Title:" in sent:
			title=sent.split('Title: ')[1].split("\n")[0]
			return title

def extract_author(txt):
	author="not found"
	try:
		author=txt.split("Author: ")[1].split("Release Date")[0].replace('\n','')
	except:
		try:
			author=txt.split("Authors: ")[1].split("Release Date")[0].replace('\n','')
		except:
			author=txt.split("Editor: ")[1].split("Release Date")[0].replace('\n','')

	return author

def extract_id(txt):
	id=""
	for sent in nltk.sent_tokenize(txt):
		if ("[eBook" in sent):
			id=sent.split("#")[1].split("]")[0]
			break
	return id


def distance(s1,s2):
	word_tokens1 =  nltk.word_tokenize(s1)
	word_tokens2 =  nltk.word_tokenize(s2)
	words1=[i for i in word_tokens1 if i.isalpha()]
	words2=[i for i in word_tokens2 if i.isalpha()]
	l=list(set(words1) & set(words2))
	n=0
	d=0
	for i in l:
		n1=words1.count(i)
		n2=words2.count(i)
		n+=max(n1,n2)-min(n1,n2)
		d+=max(n1,n2)
	return n/d
        


def dic_crank(tresh):

	files=glob.glob("*.txt")
	id_list=[]
	G = nx.Graph()
	nt = Network(height='100%', width='100%')
	nodes = []
	#print(files)
	doc_neigh = {}
	id_titre = {}
	id_auteur = {}
	
	for f in files:
	        id_list.append(int(f.split('g')[1].split('.')[0]))

	N=len(id_list)
	li=[]
	dic_distance={} ### dictionary of distances of each book with other
	dic_crank={}

	for i in id_list:
		f=open("pg"+str(i)+".txt","r",encoding="utf8")
		t = f.read()
		li.append(t)
		dic_distance[i]=[]
		G.add_node(i, title = str(extract_titles(t)))
		nodes.append(i)
		id_titre[i] = extract_titles(t)
		id_auteur[i] = extract_author(t)
	for i in range(len(id_list)):
		doc_neigh[id_list[i]] = []
			
	for i in range(len(id_list)):
		for j in range(len(id_list)):
			if i != j:
				id1= li[i].split('[eBook #')[1].split(']')[0]
				id2= li[j].split('[eBook #')[1].split(']')[0]
				d=distance(li[i],li[j])
				if d < tresh and not G.has_edge(nodes[i],nodes[j]):
					G.add_edge(nodes[i], nodes[j])
					doc_neigh[id_list[i]].append(id_list[j])
					doc_neigh[id_list[j]].append(id_list[i])
				dic_distance[int(id1)].append(d)
				dic_distance[int(id2)].append(d)
				print(f"d({id1},{id2}) = ",round(d,5), "--- Pregress ... " , 100*(j+1+i*len(id_list))/len(id_list)**2 , "%")

	for i in id_list:
		dic_distance[i]=list(dict.fromkeys(dic_distance[i]))
		dic_crank[i]=(N-1)/sum(dic_distance[i])

	print(dic_distance)
	print(dic_crank)
	nt.from_nx(G)
	nt.show_buttons(filter_ = True)
	nt.show('nx.html')
	print(doc_neigh)
	return dic_crank,id_list,doc_neigh,id_titre,id_auteur


def text_json(txt,i, neigh, titre_neigh , auteur_neigh):
	s1 = {}
	s2 = {}
	for sugg in neigh[i] :
		s1[str(sugg)] = titre_neigh[sugg]
		s2[str(sugg)] = auteur_neigh[sugg]
	dict={"title": extract_titles(txt),"author": extract_author(ind),"Id":extract_id(txt),"crank":dic_crank[i], "content": txt, "neighbors" : neigh[i], "title_neigh" : s1 , "author_neigh" : s2}
	#print(dict)
	return json.dumps(dict)


os.chdir(os.getcwd()+'/bibliotheque')

dic_crank,id_list,doc_neigh,id_titre,id_auteur = dic_crank(0.5)

elastic=Elasticsearch(hosts=["127.0.0.1"])
if elastic.indices.exists(index=index_name):
	elastic.indices.delete(index=index_name, ignore=[400, 404])



for i in id_list:
	#print(str(i))
	f=open("pg"+str(i)+".txt","r",encoding="utf8")
	ind=f.read()
	#print(extract_author(ind))
	response = elastic.index(index=index_name, doc_type='books', document=text_json(ind,i, doc_neigh, id_titre, id_auteur))
	#print(response)

os.chdir('..')
