from selenium import webdriver
from bs4 import BeautifulSoup
import re
import requests
import time
import csv
from selenium.common.exceptions import TimeoutException

def url_crawler(driver,project,project_folder_name):
    driver.get(f'https://seekingalpha.com/symbol/{project}/transcripts')
    time.sleep(2)
    for i in range(15):
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')# 向下request更多資料
        time.sleep(1)
        driver.execute_script('window.scrollTo( 0,400);')
        time.sleep(1)
    res = driver.page_source
    soup = BeautifulSoup(res,'lxml')
    urls = soup.select('[title="SA Transcripts"]')
    url_list = []
    for i in range(len(urls)):
        url = soup.select('[title="SA Transcripts"]')[i]['href']#每一個profect class位置會不同
        url_list.append('https://seekingalpha.com'+url)
    with open(f'results/{project_folder_name}/{project}/urls.csv','w') as f:
        f.write('\n'.join(url_list))
        f.close()
    return driver

def cleaning_urls(project,project_folder_name):
    '''
    find out earnings call transcript
    useless:
        (results) earnings (conference) call presentation
        (results) earnings (conference) call webcast
        (results) earnings (conference) call slide
    '''
    
    with open(f'results/{project_folder_name}/{project}/urls.csv')as csvfile:
        rows = csv.reader(csvfile)
        url_list = []
        for row in rows:
            url = row[0]                        
            # classfy                                           https://seekingalpha.com/article/1158881-walt-disneys-ceo-discusses-f1q13-results-earnings-call-transcript?source=content_type:react|section:Transcripts|sectionAsset:Transcripts|first_level_url:symbol|button:Author|lock_status:Archived|line:50
            if 'earnings-call'in url or 'earnings-transcript'in url or 'earnings-conference-call' in url or 'earnings-call-transcript' in url  or 'earnings-and-conference-call' in url or 'results-earnings' in url or 'earnings-call-conference' in url:
                if 'slides'in url or 'webcast' in url or 'presentation' in url or 'retail-call-transcript' in url or 'guidance-call-transcript' in url or 'q-and-a' in url or 'conference-transcript' in url or 'transition-period-results' in url or 'sales-results-call' in url or 'phase-3-topline' in url or 'financial-call' in url  or 'meeting-broker' in url or 'microsemi-acquisition-call' in url or 'interim-results' in url or 'trial-results' in url or 'prepared-remarks' in url or 'annual-healthconx' in url: 
                    continue
                url_list.append(url)
            else:
                continue
        with open(f'results/{project_folder_name}/{project}/earning_call.csv','w') as f:
                f.write('\n'.join(url_list))
                f.close()        