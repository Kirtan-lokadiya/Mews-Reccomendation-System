from News_Reccomendation_System.constants import *
from News_Reccomendation_System.utils.common import read_yaml, create_directories

from News_Reccomendation_System.entity.config_entity import (DataIngestionConfig,
                                                        DataTransformationConfig,
                                                        ModelTrainerConfig)
                                                        # ModelEvaluationConfig) 

#  Updating Configuratiom Manager inside src/ config

class ConfigurationManager:                  
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,                     # These were all defined in constants
        params_filepath = PARAMS_FILE_PATH,
        schema_filepath = SCHEMA_FILE_PATH
    ):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config.artifact_root])



    def get_data_ingestion_config(self) -> DataIngestionConfig:   # return type is the entity we created

        config = self.config.data_ingestion

        create_directories([config.root_dir])     # we did define the root directory but i never had such a directory,  this is solved here

        data_ingestion_configuration = DataIngestionConfig(
            root_dir= config.root_dir,
            local_data_file= config.local_data_file,
            unzip_dir= config.unzip_dir
        )

        return data_ingestion_configuration
    

    def get_data_transformation_config(self) -> DataTransformationConfig:

        config = self.config.data_transformation
        
        create_directories([config.root_dir])

        data_transformation_configuration = DataTransformationConfig(
            root_dir= config.root_dir,
            data_path_usr= config.data_path_usr,
            data_path_news= config.data_path_news
        )

        return data_transformation_configuration
    

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        params = self.params.Behaviour_model
        

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir= config.root_dir,
            train_data_path= config.train_data_path,
            test_data_path= config.test_data_path,
            model_name= config.model_name,
            model_content= config.model_content,
            news= config.news,
            ind2user= config.ind2user,
            ind2item= config.ind2item,
            batch_size= params.batch_size
            
        )

        return model_trainer_config