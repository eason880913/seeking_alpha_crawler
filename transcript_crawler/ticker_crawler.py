import requests
from bs4 import BeautifulSoup
from args import get_ticker_cralwer_args
import json
'''
usge:
python name_similar_ratio.py
'''
def main(args):
    all_list = []
    for stock in args.stocks_list:
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        res = requests.get(f'https://www.slickcharts.com/{stock}', headers=headers)
        soup = BeautifulSoup(res.text,'lxml')
        articles = soup.select('td a')
        ans_list = []
        for i in range(len(articles)):
            if i%2 == 1:
                ans = articles[i]['href']
                ans = ans.replace('/symbol/','')
                ans_list.append(ans)
        all_list.append({stock:ans_list})
    with open(args.output_json,'w') as f:
        f.write(json.dumps(all_list))

if __name__ == '__main__':
    main(get_ticker_cralwer_args())