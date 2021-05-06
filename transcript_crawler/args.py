import argparse

def get_ticker_cralwer_args():
    """Get arguments needed in ticker_crawler.py"""
    parser = argparse.ArgumentParser('Scrape the component of stock (ticker)')

    parser.add_argument('--stocks_list',
                        type=list,
                        default=['nasdaq100', 'dowjones', 'sp500'],
                        help='there are nasdaq100, dowjones, sp500')

    parser.add_argument('--output_json',
                        type=str,
                        default='stock_component.json',
                        help='stocks component output')
    args = parser.parse_args()
    return args

def get_main_cralwer_args():
    """Get arguments needed in main.py"""
    parser = argparse.ArgumentParser('Scrape the transcript from every company')
    
    parser.add_argument('--input_json',
                    type=str,
                    default='stock_component.json',
                    help='stocks component output')

    parser.add_argument('--driver_path',
                        type=str,
                        default='chromedriver',
                        help='chromdriver path')

    parser.add_argument('--stock',
                        type=str,
                        default='nasdaq100',
                        help='the component of stock will find from stock_component.json')
    
    parser.add_argument('--project_folder_name',
                        type=str,
                        default='nasdaq',
                        help='project_folder_name')
    args = parser.parse_args()
    return args