#coding=utf-8
from py2neo import *
from flask import *
import json
import jieba
import hanlp
import re
from sim import proc
import codecs
import math
app = Flask(__name__)
from flask_cors import *
CORS(app,supports_credentials=True)
graph = Graph('http://47.96.143.66:7474',username='neo4j',password='Tsinghua1')
recognizer = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)
stop_words_file = 'data/stop_words.txt'
stopwords = [x.strip() for x in codecs.open(stop_words_file, 'r', encoding='utf8').readlines()]

#cache_pre = [x.strip() for x in codecs.open("cache.txt",'r',encoding='utf8').readlines()]
print("Cache Loading......")
cache = []
cache_hint = {}
cache_len = 0

def filter(senq):
	str = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", senq)
	return str
def cont(lst, str):
	cond = ''
	leng = 2048
	for item in lst:
		if ((str in item)):
			if (len(item)<leng):
				leng = len(item)
				cond=item

	return cond

@app.route('/',methods=['GET','POST'])
def search():
	if request.method == 'POST':
		return "HELLO"
	local_sbj = None
	local_slot = None
	local_ett1 = None
	local_ett2 = None
	answer_group = []
	req = (request.args['q'])
	matchObj = re.match(r'(.*)的(.*)[为,是](.*)',req,re.M|re.I)
	matchPro = re.match(r'(.*)[和,跟,与](.*)的关系(.*)',req,re.M|re.I)
	ask_pattern = False
	if matchObj:
		local_sbj = matchObj.group(1)
		local_slot = matchObj.group(2)
		ask_pattern = True
	if matchPro:
		local_ett1 = matchPro.group(1)
		local_ett2 = matchPro.group(2)
		ask_pattern = True
	entity_list = (recognizer([list(req)]))[0]
	h2n = {'NR':'per','NS':'loc','NT':'org'}

	entitys = [ett[0] for ett in entity_list]

	roles = [h2n[ett[1]] for ett in entity_list]
	seq_list = jieba.cut(req)

	seq = ' '.join([seq for seq in seq_list if (not seq in stopwords)])

	dq = graph.run("CALL apoc.index.search('index_label', 'owl__Individual.rdfs__label:XXX') YIELD node RETURN node".replace('XXX',seq))
	lst = []
	lst_latent = []

	counter=0
	keyset = []
	num = 0 
	items = []
	score_sum = 0.0
	deno_list = []
	max_deno = 0.0
	global cache_len
	global cache
	global cache_hint
	corpus = []
	while dq.forward():


		dct ={}
		num+=1
		item = dq.current['node']
		group = None #conflict/person/org/place/other
		dct["score"] = item["score"]
		deno_list.append(item["score"])
	#	score_sum += math.exp(item["score"])
		if (item["score"]>max_deno):
			max_deno = item["score"]
		props = {}
		for k in item.keys():
			subitem=None

			if (k[0]=='n' and k[1]=='s'):
				index = k.split('__')[1]

				if (index in cache_hint.keys()):
					subitem = cache[cache_hint[index]]['sub']
					detail = cache[cache_hint[index]]['det']
				else:
					out = graph.run("CALL apoc.index.search('index_prop','owl__Property.uri:\"http://xlore.org/property/XXX\"') YIELD node RETURN node".replace("XXX",index))
					out.forward()

					try:

						subitem = out.current['node']['rdfs__label']
						detail = out.current['node']['ns0__fullname']

						cache_hint[index]=cache_len
						cache_len+=1

						cache.append({"sub":subitem,"det":detail})


					except:
						pass

				try:	
					subgroup = 'none'
					if ("##" in detail): # we can classify now
						if ('Person' in detail):
							subgroup = 'per'
						elif ('Organization' in detail):
							subgroup = 'org'
						elif ('Place' in detail):
							subgroup = 'loc'
						else:
							subgroup = 'other'
					if (subgroup!='none'):
						if (group in ['per','org','loc'] and subgroup in ['per','org','loc']):
							if (group!=subgroup):
								group = 'conflict'
						elif (group == None and subgroup in ['per','org','loc']):
							group = subgroup
				except:
					pass


			if (k=='rdfs__label'):
				subitem = "名称"

			elif (k=='rdfs__comment'):
				subitem = "详情"
				item[k]=item[k].replace("（）","").replace("\"\"","").replace('()','').replace("::;","")
			elif (k=='uri'):
				subitem = "锚点"
			if (subitem!=None):
				props[item[k]]=subitem
			if (not subitem in keyset):
				keyset.append(subitem)
			for key in keyset:
				if (not key in dct.keys()):
					dct[key]=""

			if (subitem!=None):
				dct[subitem]=item[k]


		if (not dct["名称"] in entitys):
			lst_latent.append(dct)
		else:
			role = roles[entitys.index(dct["名称"])]

			if (local_sbj!=None and dct["名称"] in local_sbj):
				if (local_slot != None and local_slot in dct.keys() and dct[local_slot]!=""):
					answer = local_sbj+"的"+local_slot+"是"+dct[local_slot]
					answer_uri = dct["锚点"]
					answer_group.append({"word":answer,"uri":answer_uri})
			elif (local_ett1 !=None and local_ett2!=None):
				cond1 = cont(props.keys(),local_ett1)
				cond2 = cont(props.keys(),local_ett2)
				if (dct["名称"] in local_ett1 and cond2!=''):


					answer = local_ett1+"的"+props[cond2]+"为"+cond2
					answer_uri = dct["锚点"]
					answer_group.append({"word":answer,"uri":answer_uri})
				elif (dct["名称"] in local_ett2 and cond1!=[]):

					answer = local_ett2+"的"+props[cond1]+"为"+cond1
					answer_uri = dct["锚点"]
					answer_group.append({"word":answer,"uri":answer_uri})
		#	print(answer,"is our answer!")
			if (role in ['per','loc','org'] and group in ['per','loc','org']):
				if (not role==group):
					dct["entity_class"] = "other"
					lst_latent.append(dct)

				else:
					dct["entity_class"] = role
					try:
						corpus.append(filter(dct["详情"]))
					except:
						corpus.append("its an empty one")
						dct["rel"]=0
					lst.append(dct)

			else:
				dct["entity_class"] = "other"
				try:
					corpus.append(filter(dct["详情"]))
				except:
					corpus.append("its an empty one")
				lst.append(dct)
	for score in deno_list:
		score_sum+=math.exp(score-max_deno)

	scores = proc(corpus,filter(req),stopwords)
	print(scores)
	for idx,item in enumerate(scores):

		if (not "rel" in lst[idx].keys()):
			lst[item[0]]["rel"]=item[1]
	lst.sort(key = lambda x:(x["rel"]*2+math.exp(x["score"]-max_deno)/score_sum),reverse=True)
	print(lst)
	lst_latent.sort(key = lambda x:(x["score"]),reverse=True)

	lst_weak = []
	last = {}
	idx = 0
	while idx<len(lst):
		if (lst[idx]['名称'] in last.keys()):
			lst_weak.append(lst[idx])
			lst.pop(idx)
			idx-=1
		else:
			last[lst[idx]["名称"]]=1
		idx+=1
	print("build end.")

	num = 0

	for idx,item in enumerate(lst):

		classes = []
		related = []
		num+=1
		uri = item["锚点"]
		print(item["名称"])
		#if (not item["名称"] in found.keys()):
		#	found[item["名称"]]=1
		#else:
		#	continue
		class_out = graph.run("MATCH (n:owl__Individual{uri:'XXX'})-[r:owl__InstanceOf]->(p) RETURN p LIMIT 5".replace("XXX",uri))
		print(item["名称"],"search end")
		while class_out.forward():
			subsub = {}
			subsub['uri']=class_out.current['p']['uri']
			subsub['名称']=class_out.current['p']['rdfs__label']
			classes.append(subsub)

		related_out = graph.run("MATCH (n:owl__Individual{uri:'XXX'})-[]->(p:owl__Individual) RETURN p LIMIT 5".replace("XXX",uri))
		while related_out.forward():
			subsub = {}
			subsub['uri']=related_out.current['p']['uri']
			subsub['名称']=related_out.current['p']['rdfs__label']
			related.append(subsub)
		lst[idx]["标签"]=classes
		lst[idx]["相关项"]=related

	for idx,item in enumerate(lst_weak):

		classes = []
		related = []
		num+=1
		uri = item["锚点"]
		print(item["名称"])
		#if (not item["名称"] in found.keys()):
		#	found[item["名称"]]=1
		#else:
		#	continue
		class_out = graph.run("MATCH (n:owl__Individual{uri:'XXX'})-[r:owl__InstanceOf]->(p) RETURN p LIMIT 1".replace("XXX",uri))
		print(item["名称"],"search end")
		while class_out.forward():
			subsub = {}
			subsub['uri']=class_out.current['p']['uri']
			subsub['名称']=class_out.current['p']['rdfs__label']
			classes.append(subsub)

		related_out = graph.run("MATCH (n:owl__Individual{uri:'XXX'})-[]->(p:owl__Individual) RETURN p LIMIT 1".replace("XXX",uri))
		while related_out.forward():
			subsub = {}
			subsub['uri']=related_out.current['p']['uri']
			subsub['名称']=related_out.current['p']['rdfs__label']
			related.append(subsub)
		lst_weak[idx]["标签"]=classes
		lst_weak[idx]["相关项"]=related


	if (len(answer_group)==0 and ask_pattern==True):
		answer_group.append({"word":"对不起，没有找到您提供问题的答案","uri":""})
	QA = {}
	QA['tag']='answer'
	QA['详情'] = answer_group 

	print(QA)

	if (answer_group!=[]):
		lst = [QA]+lst
	lst = lst+(lst_weak)+(lst_latent)
	for idx,item in enumerate(lst):
		lst[idx]["rel"]=0
		lst[idx]["score"]=0
	result_json = json.dumps(lst)
	resp = Response(result_json)
	resp.headers['Access-Control-Allow-Origin']='*'


	return resp 

app.debug=True
app.run(host='0.0.0.0',port='5000')
