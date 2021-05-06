from selenium import webdriver
from bs4 import BeautifulSoup
import re
import requests
import time
import json 
import os
import difflib

'''
<一次性>
用來確認seeking alpha 跟 finhub 的差異
結論:
finhub資料跟seeking alpha不一樣
少了很多段落，雖然錯字有被修正
'''


project = "SOX30"

if not os.path.isdir('finnhub_metadata'):
    os.mkdir('finnhub_metadata')

SOX=['AMD','ADI','AMAT','AVGO','ASML','CCMP','CRUS','CREE','ENTG','INTC','KLAC','LRCX','MRVL','MXIM','MCHP','MU','MKSI','MPWR','NVDA','NXPI','ON','QRVO','QCOM','SMTC','SLAB','SWKS','TSM','TER','TXN','XLNX']

input_file = open ('/Users/eason880913/Desktop/work/alpha_crawler/results/new_SOX30/TSM/TSM_result.json')
json_array = json.load(input_file)

r = requests.get('https://finnhub.io/api/v1/stock/transcripts/list?symbol=TSM&token=buv11pv48v6rf2qogf10').json()['transcripts']

for i in range(len(r)):
    if 'Conference call' in r[i]['title']:
        continue
    fin_title = []
    fin_title.append(r[i]['year'])
    fin_title.append(r[i]['quarter'])
    # print(fin_title)

    for j in range(len(json_array)):
        title = json_array[j]['entry']['title']
        text_SA = json_array[j]["entry"]['transcript']
        url = json_array[j]["entry"]['url']
        if fin_title == title:
            break

    FH_id = r[i]['id']
    res = requests.get(f'https://finnhub.io/api/v1/stock/transcripts?id={FH_id}&token=buv11pv48v6rf2qogf10').json()
    ansl = []
    for k in range(len(res['transcript'])):
        ansl.append("<h>"+res['transcript'][k]['name']+"</h>")
        for m in range(len(res['transcript'][k]['speech'])):
            ansl.append("<p>"+res['transcript'][k]['speech'][m]+"</p>")
    text_FH = ''.join(ansl)

    print(title)
    print(difflib.SequenceMatcher(None, text_SA, text_FH).quick_ratio())

    # if str(fin_title) == '[2020, 3]':
    #     print(text_SA,'\n\n\n\n\n',text_FH)
    #     break
    



# with open(f'finnhub_metadata/{project}/project.json','w') as f:
#     f.write(all_dict) 
# ans = requests.get('https://finnhub.io/api/v1/stock/transcripts?id=AAPL_162777&token=buv11pv48v6rf2qogf10').json()
# print(ans)