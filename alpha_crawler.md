# seeking_alpha_crawler
for crawling transcripts in seeking alpha

## transcript crawler 
### crawler
scrape all transcripts from companys of stock
#### usge:
python name_similar_ratio.py --stock='nasdaq100' --project_folder_name='nasdaq'
### check
check exec, analysts, title isnull
#### usge:
setup the result project_folder_name
python check.py
### ticker_crqwler
crawl all tickers e.g.NASDAQ100, SP500, dowjone30
#### usge:
python ticker_crawler.py

## similar_caculator
### name_similiar_ratio
Due to there are name abbrevation or middle name in English 
e.g.Romit Jitendra Shah & Romit J. Shah, Daniel Durn, Daniel J. Durn
so caculate the similar ratio to decide whether two different name is same
#### usge:
python name_similar_ratio.py --company='AMAT' --token='yourtoken'
### content_similair_caculators
<一次性>
用來確認seeking alpha 跟 finhub 的差異
結論:
finhub資料跟seeking alpha不一樣
少了很多段落，雖然錯字有被修正