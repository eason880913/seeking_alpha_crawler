import argparse

def get_name_similair_args():
    """Get arguments needed in name_similair.py"""
    parser = argparse.ArgumentParser('Scrape Participant of transcript ')

    parser.add_argument('--token',
                        type=str,
                        default=None,
                        help='finbuh access token')
    parser.add_argument('--reverse',
                        type=bool,
                        default=False,
                        help='because last name is more import than first name')
    parser.add_argument('--company',
                        type=str,
                        required=True,)
    parser.add_argument('--outputfolder',
                        type=str,
                        default="similar_result",
                        help="output folder")
    parser.add_argument('--cacu_type',
                        type=str,
                        default="jaro_winkler",
                        help="check Levenshtein")
    parser.add_argument('--crawler_data',
                        type=str,
                        default="name",
                        help="check Levenshtein")
    args = parser.parse_args()

    return args