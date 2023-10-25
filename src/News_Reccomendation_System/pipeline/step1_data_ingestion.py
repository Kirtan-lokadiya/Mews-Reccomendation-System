from News_Reccomendation_System.config.configuration import ConfigurationManager
from News_Reccomendation_System.components.data_ingestion import DataIngestion
from News_Reccomendation_System import logger





STEP_NAME = '01 ---- Data Ingestion Step'


class DataIngestionPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigurationManager()
        data_ingeston_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config= data_ingeston_config)
        data_ingestion.extract_zip_file()


def run_data_ingestion():

    try:

        logger.info(f' >>>>>>> Step {STEP_NAME} started <<<<<<<<<<<')
        obj = DataIngestionPipeline()
        obj.main()
        logger.info(f' >>>>>>> Step {STEP_NAME} completed <<<<<<<<<<<\n\nx====================x')

    except Exception as e:
        logger.exception(e)
        raise e