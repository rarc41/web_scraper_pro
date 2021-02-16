import logging
logging.basicConfig(level=logging.INFO)
import subprocess
import os
import shutil

logger = logging.getLogger(__name__)
news_sites_uids=['eluniversal', 'elpais']

def main():
    _extract()
    _transform()
    _load()

def _extract():
    logger.info("Starting sxtract process")
    for news_site_uid in news_sites_uids:
        subprocess.run(['python', 'main.py', news_site_uid], cwd='./extract')
        
        path = './extract'
        file = _search_file(path, news_site_uid)
        _move_file(path + '/' + file, './transform/' + file)
        # subprocess.run(['copy', r'./extract/*.csv', r'./transform'], shell=True)
        

        # subprocess.run(['find', '.', '-name', '{}*'.format(news_site_uid),
        #                 '-exec', 'mv', '{}', '../transform/{}_.csv'.format(news_site_uid), '\;'],
        #                cwd='./extract')
        



def _transform():
    logger.info('Starting transform process')
    
    for news_site_uid in news_sites_uids:
        dirty_data_filename=_search_file('./transform', news_site_uid)
        clean_data_filename=f'clean_{dirty_data_filename}'
        subprocess.run(['py', 'main.py', dirty_data_filename], cwd='./transform')
        subprocess.run(['rm', dirty_data_filename], cwd='./transform')
        subprocess.run(['mv', clean_data_filename, f'../load/{news_site_uid}.csv'], cwd='./transform')


def _load():
    logger.info('Starting load process')
    for news_site_uid in news_sites_uids:
        clean_data_filename =f'{news_site_uid}.csv'
        subprocess.run(['py', 'main.py', clean_data_filename], cwd='./load')
        # subprocess.run(['rm', clean_data_filename], './load')
        _remove_file('./load', clean_data_filename)
        
def _search_file(path, file_match):
    logger.info('Searching file')
    for rutas in list(os.walk(path))[0]:
        if len(rutas) > 1:
            for file in rutas:
                if file_match in file:
                    return file
    return None

def _move_file(origen, destino):
    logger.info('Moving file')
    shutil.move(origen, destino)
    
def _remove_file(path, file):
    logger.info(f'Removing file {file}')
    os.remove(f'{path}/{file}')

if __name__ == '__main__':
    main()
