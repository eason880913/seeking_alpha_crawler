# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import requests
import json 
import os
import csv
import Levenshtein
from args import get_name_similair_args
from tqdm import tqdm

'''
Due to there are name abbrevation or middle name in English e.g.Romit Jitendra Shah & Romit J. Shah, Daniel Durn, Daniel J. Durn
so caculate the similar ratio to decide whether two different name is same

four types of number of similar raito
Levenshtein.distance(s1, s2) Compute absolute Levenshtein distance of two strings.
Levenshtein.ratio(s1, s2) The similarity is a number between 0 and 1, it's usually equal or somewhat higher than difflib.SequenceMatcher.ratio(), because it's based on real minimal edit distance.
Levenshtein.jaro(s1, s2) The Jaro-Winkler string similarity metric is a modification of Jaro metric giving more weight to common prefix, as spelling mistakes are more likely to occur near ends of words. The prefix weight is inverse value of common prefix length sufficient to consider the strings *identical*. If no prefix weight is specified, 1/10 is used.
Levenshtein.jaro_winkler(s1, s2) The result is a list of triples with the same meaning as in SequenceMatcher's get_matching_blocks() output. It can be used with both editops and opcodes. The second and third arguments don't have to be actually

output result csv in similar result in folder

usge :
python name_similar_ratio.py --company='AMAT' --token='yourtoken'
'''

def folder_builder(outputfolder):
    if not os.path.isdir(outputfolder):
            os.mkdir(outputfolder)

def get_all_name(company, token, crawler_data):
    r = requests.get(f'https://finnhub.io/api/v1/stock/transcripts?symbol={company}&token={token}').json()['transcripts']
    all_name = []
    with tqdm(total=len(r)) as pbar:
        for i in range(len(r)):
            #有分 conference call & earning call
            if 'Conference call' in r[i]['title']:
                pbar.update(1)
                continue
            FH_id = r[i]['id']
            res = requests.get(f'https://finnhub.io/api/v1/stock/transcripts?id={FH_id}&token={token}').json()
            for j in range(len(res['participant'])):
                name = re.sub(',',' 2c',res['participant'][j][crawler_data])
                all_name.append(name)
            pbar.update(1)
    print('success to get all names...')
    return all_name

def cleaning_name_list(all_name, reverse):
    # remove repeat & sort
    name_list = list(set(all_name))
    name_list.sort()
    if reverse:
        l1 = []
        for i in name_list:
            sli = list(i)
            sli.reverse()
            l1.append(''.join(sli))
        name_list = l1
    return name_list

def save_ratio_result(company, crawler_data, name_list):
    #save csv
    with open (f'similar_result/{company}_{crawler_data}.csv','w') as f:
        f.write('Levenshtein.jaro_winkler,'+','.join(name_list)+'\n') #headline in csv
        for i in name_list:
            tlist = []
            for j in name_list:
                tlist.append(str(round(Levenshtein.jaro_winkler(i, j,0.1),2)))
            f.write(i+','+','.join(tlist)+'\n')
    print(f'success to save result to similar_result/{company}_{crawler_data}.csv')

def main(args):
    folder_builder(args.outputfolder)
    all_name = get_all_name(args.company, args.token, args.crawler_data)
    name_list = cleaning_name_list(all_name, args.reverse)
    save_ratio_result(args.company, args.crawler_data, name_list)

if __name__ == '__main__':
    main(get_name_similair_args())

