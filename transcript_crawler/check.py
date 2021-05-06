import json
import operator
import re
from os import listdir
from os.path import isfile, isdir, join
from module.parse import *
from collections import Counter
# NASDAQ100 = ['AAPL','AMZN','MSFT','FB','GOOGL','GOOG','TSLA','NVDA','ADBE','PYPL','NFLX','INTC','CMCSA','PEP','CSCO','COST','AVGO','AMGN','TMUS','QCOM','TXN','CHTR','SBUX','AMD','GILD','MDLZ','INTU','ISRG','BKNG','JD','VRTX','ZM','FISV','ATVI','CSX','ADP','REGN','ILMN','MELI','MU','AMAT','ADSK','BIIB','MNST','LRCX','ADI','LULU','KHC','EBAY','CTSH','EA','DOCU','XEL','WDAY','DXCM','ORLY','EXC','NXPI','NTES','CTAS','BIDU','MAR','ROST','IDXX','WBA','SNPS','SPLK','VRSK','PCAR','CDNS','ASML','PAYX','ANSS','KLAC','SGEN','FAST','ALGN','MCHP','SIRI','XLNX','CPRT','PDD','ALXN','MRNA','VRSN','SWKS','CERN','DLTR','INCY','MXIM','TTWO','CHKP','CTXS','CDW','TCOM','BMRN','ULTA','EXPE','WDC','FOXA','LBTYK','FOX','LBTYA']
# print(len(NASDAQ100))

# all_list=['AMD','ADI','AMAT','AVGO','ASML','CCMP','CRUS','CREE','ENTG','INTC','KLAC','LRCX','MRVL','MXIM','MCHP','MU','MKSI','MPWR','NVDA','NXPI','ON','QRVO','QCOM','SMTC','SLAB','SWKS','TSM','TER','TXN','XLNX']
# all_list=['MCD','JNJ','KO','HD','VZ','MMM','AXP','NKE','MRK','CAT','PG','JPM','CSCO','WMT','WBA','TRV','GS','DIS','V','AAPL','IBM','UNH','PFE','DOW','MSFT','RTX','CVX','BA','XOM']
# for k in all_list:
#     project = k

all_list=['ADI']

for k in all_list:
    ans_all = []
    input_file = open (f'results/new_SOX30/{k}/{k}_result.json')
    # input_file = open (f'/Users/eason880913/Desktop/work/alpha_crawler/NASDAQ100/AAPL/AAPL_result.json')
    json_array = json.load(input_file)

    for i in json_array:
        if i["entry"]['title'] == []:
            print(i["entry"]['title'],'\n',i["entry"]['exec'],'\n',i["entry"]['analysts'],'\n',i["entry"]['url'],end = '\n')
    for i in json_array:
        if i["entry"]['exec'] == []:
            print(i["entry"]['title'],'\n',i["entry"]['exec'],'\n',i["entry"]['analysts'],'\n',i["entry"]['url'],end = '\n')
    for i in json_array:
        if i["entry"]['analysts'] == []:
            print(i["entry"]['title'],'\n',i["entry"]['exec'],'\n',i["entry"]['analysts'],'\n',i["entry"]['url'],end = '\n')

    for i in json_array:
        print(i["entry"]['title'],i["entry"]['oldticker'])
        ans_all.append(i["entry"]['title'][0])
    print(Counter(ans_all))


