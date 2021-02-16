import argparse
import logging

from pandas.core.frame import DataFrame
logging.basicConfig(level=logging.INFO)
from urllib.parse import urlparse
import pandas as pd
import hashlib
import nltk
from nltk.corpus import stopwords


logger=logging.getLogger(__name__)

def main(filename):
    logger.info('Starting cleaning process')

    df = _read_data(filename)
    newspaper_uid = _extract_newspaper_uid(filename)
    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _extract_host(df)
    df = _fill_missing_titles(df)
    df = _generate_uids_for_rows(df)
    df = _cleaning_body(df)
    df = _tokenize_titles(df)
    df = _tokenize_body(df)
    df = _remove_duplicates_entries(df, 'title')
    df = _drop_rows_with_missing_values(df)
    _save_data(df, filename)

    return df

def _read_data(filename):
    logger.info(f'Reading file {filename}')

    return pd.read_csv(filename)

def _extract_newspaper_uid(filename):
    logger.info('Extracting newspaper uid')
    newspaper_uid = filename.split('_')[0]

    logger.info(f'Newspaper uid detected: {newspaper_uid}')
    return newspaper_uid

def _add_newspaper_uid_column(df, newspaper_uid):
    logger.info(f'Filling newspaper_uid column with {newspaper_uid}')
    df['newspaper_uid'] = newspaper_uid

    return df

def _extract_host(df):
    logger.info('Extracting host from url')
    df['host'] =df['url'].apply(lambda url: urlparse(url).netloc)
    return df

def _fill_missing_titles(df):
    logger.info('Searching missing titles.')
    missing_titles_mask=df['title'].isna()
    missing_titles=(df[missing_titles_mask]['url'].str.extract(r'(?P<missing_titles>[^/]+)$')
                    .applymap(lambda title: title.split('-'))
                    .applymap(lambda title_word_list: ' '.join(title_word_list)))
    
    
    df.loc[missing_titles_mask, 'title']=missing_titles.loc[:,'missing_titles']
    return df

def _generate_uids_for_rows(df):
    logger.info('Generating uids for rows.')
    uids=(df.apply(lambda row: hashlib.md5(bytes(row['url'].encode('utf-8'))), axis=1)
            .apply(lambda hash_object: hash_object.hexdigest()))
    df['uid'] = uids
    df.set_index('uid',inplace=True)
    
    return df

def _cleaning_body(df):
    logger.info('Cleaning text body.')
    df['body']=df['body'].apply(lambda body: body.replace('\n', '')).apply(lambda body: body.replace('\r', ''))
    return df

def _tokenize_column(df, column_name):
    stop_words=set(stopwords.words('spanish'))
    return (df
                .dropna()
                .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)
                .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
                .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))
                .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list)))
                .apply(lambda valid_word_list: len(valid_word_list)))


def _tokenize_titles(df):
    df['n_tokens_title']=_tokenize_column(df, 'title')
    return df

def _tokenize_body(df):
    df['n_tokens_body']=_tokenize_column(df, 'body')
    return df

def _remove_duplicates_entries(df, column_name):
    logger.info('Removing duplicates entries')
    df.drop_duplicates(subset=[column_name], keep='first', inplace=True)
    return df

def _drop_rows_with_missing_values(df):
    logger.info('Dropping rows with missing values')
    return df.dropna()

def _save_data(df, filename):
    clean_filename=f'clean_{filename}'
    logger.info(f'Saving data at location: {clean_filename}')
    df.to_csv(clean_filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='The path to the dirty data',
                        type=str)

    args = parser.parse_args()

    df = main(args.filename)
    print(df)