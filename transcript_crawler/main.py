# -*- coding: utf-8 -*-
"""
output:
    project_folder_name
    ├── project
        ├── {project}/urls.csv
        ├── {project}/earning_call.csv
        └── {project}_result.json
    ├── done
        └── {project}_result.json
@author: Eason
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import requests
import time
import pytz
import datetime
import json 
import os
import csv
from selenium.common.exceptions import TimeoutException
from enum import Enum
from module.transcript_urls_crawler import *
from module.login import *
from module.setting import *
from module.parse import *
from args import get_main_cralwer_args


def company_list_maker(input_json):
    with open (input_json,'r') as f:
        list_of_companies = json.load(f)
    return list_of_companies

def crawler_to_json(project,driver,log_writer,project_folder_name):
    #default settings
    ticker_company_holder = {}
    Stage = Enum('Stage', 'preamble execs analysts body skip')
    with open(f'results/{project_folder_name}/{project}/earning_call.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        all_dict =[]
        for row in rows:
            transcript = {}
            details = {}
            execs = []
            analysts = []
            script = []
            mode = 1
            # As the pages are represented by a series of `<p>` elements, all with
            # the same class `.p1` `.p2`...and no unique identfiers, we have to do this the
            # old-fashioned way - breaking it into chunks and iterating over them.
            url = row[0]
            driver.get(url)
            res = driver.page_source
            soup = BeautifulSoup(res,'lxml')
            
            # title & all_title
            title_maker(soup,details,url,log_writer,input_detail)

            # company & ticker
            company_ticker_macker_v3(soup,details,url,ticker_company_holder,project)
            
            #date_maker 
            date_maker(soup,details,url,log_writer)

            #old_ticker
            old_ticker_macker(soup,details)

            #exchange
            details['exchange'] = "NASDAQ"#default

            #content (exec, analysts, body)
            chunks = soup.select('div#a-body [class="p p1"]')
            for i in range(len(chunks)):
                # If the current line is a heading and we're not currently going
                # through the transcript body (where headings represent speakers),
                # change the current section flag to the next section.
                if '<strong>'in str(chunks[i]) or '<h1>' in str(chunks[i]):
                    mode += 1
                    if mode >4:
                        mode = 4
                if '<strong>Executives'in str(chunks[i]) or 'Executives</h1>' in str(chunks[i]) or '<span>Company Participants' in str(chunks[i]):
                    mode = 2
                if '<strong>Analysts'in str(chunks[i]) or 'Analysts</h1>' in str(chunks[i]) or '<span>Conference Call Participants' in str(chunks[i]):
                    mode = 3
                # if '<strong>Operator'in str(chunks[i]) or 'Operator</h1>' in str(chunks[i]):
                #     mode = 5
                if '<strong>' not in str(chunks[i]) or (mode == 4):
                    currStage = Stage(mode)
                    # If we're on the preamble stage, each bit of data is extracted
                    # separately as they all have their own key in the JSON.
                    
                    
                    if currStage == Stage['preamble']:
                        #old_ticler_maker
                        if '<strong>' not in str(chunks[i]) and details['oldticker'] == '':#如果不是標題
                            try:
                                row_ticker = re.findall('\\(\w*\\)',chunks[i].text)[0]
                                row_ticker = re.sub('\\(|\\)','',row_ticker)
                                row_ticker = re.sub('\w*\\:','',row_ticker)
                                details['oldticker'] = row_ticker
                            except:
                                log_writer(f'maybe oldticker error in {url}')
                    

                    # If we're onto the 'Executives' section, we create a list of
                    # all of their names, positions and company name (from the preamble).
                    if currStage == Stage['execs']:
                        if chunks[i].text ==''or chunks[i].text == ' ':
                            continue
                        if len(chunks[i].text.split(" - ")) > 1:
                            name = re.sub('^\\s|\\s$','',chunks[i].text.split(" - ")[0])
                            position = re.sub('^\\s|\\s$','',chunks[i].text.split(" - ")[1])
                        elif len(chunks[i].text.split(" – ")) > 1:
                            name = re.sub('^\\s|\\s$','',chunks[i].text.split(" – ")[0])
                            position = re.sub('^\\s|\\s$','',chunks[i].text.split(" – ")[1])
                        elif len(chunks[i].text.split(", ")) > 1:
                            name = re.sub('^\\s|\\s$','',chunks[i].text.split(", ")[0])
                            position = re.sub('^\\s|\\s$','',chunks[i].text.split(", ")[1])
                        else:
                            name = chunks[i].text
                            position = ""
                        execs.append((name,position,details['company']))

                    # This does the same, but with the analysts (which never seem
                    # to be separated by em-dashes for some reason).
                    elif currStage == Stage['analysts']:
                        if chunks[i].text ==''or chunks[i].text == ' ':
                            continue
                        elif '\n\n' in chunks[i].text:
                            anal_str = chunks[i].text
                            anal_str = re.sub('$\n','',anal_str)
                            phrase_list = anal_str.split("\n\n")
                            for i in range(len(phrase_list)):
                                name = phrase_list[i].split(", ")[0]
                                company = phrase_list[i].split(", ")[1]
                                analysts.append((name,company))
                        elif len(chunks[i].text.split(" - ")) > 1:
                            name = chunks[i].text.split(" - ")[0]
                            company = chunks[i].text.split(" - ")[1]
                            analysts.append((name,company))
                        elif len(chunks[i].text.split(" – "))>1:
                            name = chunks[i].text.split(" – ")[0]
                            company = chunks[i].text.split(" – ")[1]
                            analysts.append((name,company))
                        elif len(chunks[i].text.split(" -- "))>1:
                            name = chunks[i].text.split(" -- ")[0]
                            company = chunks[i].text.split(" -- ")[1]
                            analysts.append((name,company))
                        elif len(chunks[i].text.split(", "))>1:
                            name = chunks[i].text.split(", ")[0]
                            company = chunks[i].text.split(", ")[1]
                            analysts.append((name,company))
                        else:
                            analysts.append((chunks[i].text,''))
                            continue
                        

                    # This strips the transcript body of everything except simple
                    # HTML, and stores that.
                    elif currStage == Stage['body']:
                        line = chunks[i].text
                        line = re.sub('^\\s|\\s$','',line)
                        if line == '' or line == ' ':
                            continue
                        elif '<strong>' not in str(chunks[i]) and '<br/>' not in str(chunks[i]):
                            html = "p>"
                            script.append("<"+html+line+"</"+html)

                        elif '<strong>' in str(chunks[i]) and '<br/>' not in str(chunks[i]):
                            html = "h>"
                            script.append("<"+html+line+"</"+html)
                        elif '<br/>' in str(chunks[i]):
                            contents = str(chunks[i])
                            contents = contents.split('<br/>')
                            for m in range(len(contents)):
                                    contents[m] = re.sub('<p class="p p\\d*">|</p>','',contents[m])
                                    contents[m] = re.sub('strong','h',contents[m])
                                    contents[m] = re.sub('^\\s|\\s$','',contents[m])
                                    if contents[m] == '':
                                            continue
                                    if '<h>' not in contents[m]:
                                            contents[m] = "<p>"+contents[m]+'</p>'
                                    script.append(contents[m])
                                    
                
            #法說會內容後面的
            count_all_p = soup.select('div#a-body [class="p_count"]')
            for j in range(2,len(count_all_p)+2):
                single_p = soup.select(f'div#a-body [class="p p{j}"]')
                for k in range(len(single_p)):
                    line = single_p[k].text
                    line = re.sub('^\\s|\\s$','',line)
                    if line == '' or line == ' ':
                            continue
                    if '<strong>' not in str(single_p[k]) and '<br/>' not in str(single_p[k]):
                        html = "p>"
                        script.append("<"+html+line+"</"+html)
                    elif '<strong>' in str(single_p[k]) and '<br/>' not in str(single_p[k]):
                        html = "h>"
                        script.append("<"+html+line+"</"+html)
                    elif '<br/>' in str(single_p[k]):
                        contents = str(single_p[k])
                        contents = contents.split('<br/>')
                        for m in range(len(contents)):
                                contents[m] = re.sub('<p class="p p\\d*">|</p>','',contents[m])
                                contents[m] = re.sub('strong','h',contents[m])
                                contents[m] = re.sub('^\\s|\\s$','',contents[m])
                                if contents[m] == '':
                                    continue
                                if '<h>' not in contents[m]:
                                    contents[m] = "<p>"+contents[m]+'</p>'
                                script.append(contents[m])
            
            #delete^<p> transcript
            # if len(re.findall('^<p>.*',''.join(script))) >0:
            #     print('<p>',url)
            #     continue

            '''
            #cleaning operator 
            operator = re.findall("<h>Operator</h><p>.*?</p>",''.join(script))
            for i in operator:
                script = re.sub(i,'',''.join(script))
            script = re.sub('<h>Operator</h>','',script)
            ''' 

            # Adds the various arrays to the dictionary for the transcript
            details['exec'] = execs 
            details['analysts'] = analysts
            details['transcript'] = ''.join(script)
            details['url'] = url
            # Adds this transcript to the dictionary of all scraped
            # transcripts, and yield that for the output
            transcript["entry"] = details
            all_dict.append(transcript)
            continue

        all_dict = cleaning_repeat_date(all_dict) 
        all_dict = json.dumps(all_dict)
       
        with open(f'results/{project_folder_name}/{project}/{project}_result.json','w') as f:
            f.write(all_dict)   
        with open(f'results/{project_folder_name}/done/{project}_result.json','w') as f:
            f.write(all_dict)  

def main(args):
    list_of_companies = company_list_maker(args.input_json)
    project_folder_name = args.project_folder_name

    for n in range(len(list_of_companies)):
        log_writer = procedure_log(f'results/{project_folder_name}/problem')
        driver = init_selenium(args.driver_path)
        driver = login_v3(driver)  
        project = list_of_companies[n]
        file_maker(project_folder_name,project)
        driver = url_crawler(driver,project,project_folder_name)
        cleaning_urls(project,project_folder_name)
        crawler_to_json(project,driver,log_writer,project_folder_name)
        driver.quit()
 
if __name__ == '__main__':
    main(get_main_cralwer_args())