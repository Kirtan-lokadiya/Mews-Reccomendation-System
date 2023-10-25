import os
import urllib.request as request    # to download the file from the url
import zipfile
from News_Reccomendation_System import logger
from News_Reccomendation_System.utils.common import get_size

from pathlib import Path
from News_Reccomendation_System.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    # def download_data(self):
    #     if not os.path.exists(self.config.local_data_file):
    #         print(self.config.source_URL)
    #         filename, headers = request.urlretrieve(
    #             url = self.config.source_URL,                               # Thw link gave me an error because my repo was private
    #             filename = self.config.local_data_file
    #         )

    #         logger.info(f'{filename} downloaded successfully!, with following info: \n{headers}')
    #     else:
    #         logger.info(f'File already exists pf size: {get_size(Path(self.config.local_data_file))}')


    def extract_zip_file(self):
        '''
        This will unzip the downloaded zip file
        '''
        zip_extract_to_path = self.config.unzip_dir
        os.makedirs(zip_extract_to_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_file:
            zip_file.extractall(zip_extract_to_path)