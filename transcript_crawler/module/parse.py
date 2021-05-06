import re
import datetime

def input_detail(details,year,quarter):
    year_q = []
    year_q.append(int(year))
    year_q.append(int(quarter))
    details['title'] = year_q
    return details
    
def title_maker(soup,details,url,log_writer,input_detail):
    '''
    Q4 2020 4th
    F4Q2014 1st
    F3Q 2014 3rd
    F1Q08 2nd
    '''
    all_title = soup.select('header div#a-hd h1')[0].text
    details['all_title'] = all_title
    res1 = re.findall('F\\dQ\\d{4}',all_title)
    res2 = re.findall('Q\\d',all_title)
    res3 = re.findall('\\d{4}',all_title)
    res4 = re.findall('F\\dQ',all_title)
    res5 = re.findall('F\\dQ\\d{2}',all_title)
    if len(res1) == 1:
        quarter = re.findall('F\\dQ',str(res1[0]))
        quarter = re.sub('F|Q','',quarter[0])
        year = re.sub('F\\dQ','',res1[0])
        details = input_detail(details,year,quarter)
    elif len(res5) == 1 :   
        quarter = re.findall('F\\dQ',str(res5[0]))
        quarter = re.sub('F|Q','',quarter[0])
        year = re.sub('F\\dQ','',res5[0])
        year = 2000 + int(year)
        details = input_detail(details,year,quarter)
    elif len(res3) > 0 and len(res4) == 1:
        quarter = re.sub('\\D','',res4[0])
        year = res3[0]
        details = input_detail(details,year,quarter)
    elif len(res2) == 1 and len(res3) > 0:
        quarter = re.sub('Q','',res2[0])
        year = res3[0]
        details = input_detail(details,year,quarter)
    else:
        details['title'] = [0,0]
        log_writer(f'error in title maker : {all_title} url: {url}')
        print(f'error in title maker : {all_title} url: {url}')

def date_maker(soup,details,url,log_writer):
    title_title = soup.select('[class="a-info clearfix"]')[0].text
    title_title = title_title.split('ET')[0]
    title_title = re.sub('\\.','',title_title)
    try:
        title_title = datetime.datetime.strptime(title_title,"%b %d, %Y %I:%M %p ")
        details['date'] = str(title_title)
    except:
        log_writer(f'date_maker_err in : {title_title} url: {url}')
        print(f'date_maker_err in : {title_title} url: {url}')

def company_ticker_macker(soup,project,details,url):
    '''
    Includes: TSM : class="ticker-link"
    About: Taiwan Semiconductor Manufacturing Company Limited (TSM) : class="ticker-link inside-about-section"
    '''
    details['ticker'] = project
    try:
        if soup.select('[class="ticker-link inside-about-section"]') > 0:
            about_text = soup.select('[class="ticker-link inside-about-section"]')[0].text
            details['company'] = about_text.split('(')[0]
            details['ticker'] = re.sub('\\)','',about_text.split('(')[1])
        elif soup.select('[class="ticker-link"]') > 0:
            details['ticker'] = soup.select('[class="ticker-link inside-about-section"]')[0].text
            details['company'] = ''
            print('company要補',url)
    except:
        print("company_ticker_macker",'有少',url)
        details['company'] = ''
        details['ticker'] = ''
'''
def company_ticker_macker_v2(soup,details,url,ticker_company_holder):
    try:
        ticker_link = soup.select('[class="ticker-link"]')
        ticker = re.sub('https:\\/\\/seekingalpha\\.com/symbol/','',ticker_link[0]['href'])  
        details['ticker'] = ticker
        try:
            details['company'] = ticker_company_holder[ticker]
        except:
            driver.get(ticker_link[0]['href'])
            time.sleep(1)
            res1 = driver.page_source
            soup = BeautifulSoup(res1,'lxml')
            company = soup.select('[data-test-id="symbol-full-name"]')[0].text
            company = re.sub('\s\\|\s.*','',company)
            details['company'] = company
            ticker_company_holder[ticker] = company
            print(ticker_company_holder)
            # details['company'] = re.findall('.*Inc\\.',company)[0]
    except:
        details['company'] = ''
        details['ticker'] = ''
        print(f'worng company or ticker in {url}')
'''
def company_ticker_macker_v3(soup,details,url,ticker_company_holder,project):
    details['ticker'] = project
    try:
        details['company'] = ticker_company_holder[project]
    except:   
        about_text = soup.select('[class="ticker-link inside-about-section"]')[0].text
        details['company'] = about_text.split('(')[0]
        ticker_company_holder[project] = about_text.split('(')[0]
        print(ticker_company_holder)

def old_ticker_macker(soup,details):
    '''
    old ticker find in preamble where there is a link 
    '''
    try:
        ticker_link = soup.select('[class="ticker-link"]')
        ticker = re.sub('https:\\/\\/seekingalpha\\.com/symbol/','',ticker_link[0]['href']) 
        ticker = re.sub('/symbol/','',ticker)
        details['oldticker'] = ticker
    except:
        details['oldticker'] = ''


def cleaning_repeat_date(json_array):
    titles = []
    a = 0
    for i in range(len(json_array)):
        # print(json_array[i-a]["entry"]["date"],json_array[i-a]["entry"]["title"])  '',join(json_array[i-a]["entry"]["title"]
        if str(json_array[i-a]["entry"]["title"])+str(json_array[i-a]["entry"]["analysts"])+(json_array[i-a]["entry"]["oldticker"]) in titles:
            print(json_array[i-a]["entry"]["date"],json_array[i-a]["entry"]["title"])
            ans = json_array.pop(i-a)
            a += 1
            continue
        titles.append(str(json_array[i-a]["entry"]["title"])+str(json_array[i-a]["entry"]["analysts"])+(json_array[i-a]["entry"]["oldticker"]))
    return json_array

