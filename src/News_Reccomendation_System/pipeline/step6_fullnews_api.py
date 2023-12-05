from News_Reccomendation_System.config.configuration import ConfigurationManager
from News_Reccomendation_System.components.fullnews import FullNews
from News_Reccomendation_System import logger





class FullNewsPipeline:
    def __init__(self) -> None:
        pass

    def main(self, news_id):

        config = ConfigurationManager()
        fullnews_configuration = config.get_fullnews_config()
        fullnews = FullNews(config= fullnews_configuration)
        fullnews_records = fullnews.get_full_news(news_id= news_id)

        return fullnews_records
    



STEP_NAME = ' ---- Requesting FullNews API ---------'


def get_fullnews_api(news_id):
    try:
        logger.info(f' >>>>>>> Step {STEP_NAME} started <<<<<<<<<<<')
        obj = FullNewsPipeline()
        records = obj.main(news_id= news_id)
        logger.info(f' >>>>>>> Step {STEP_NAME} completed <<<<<<<<<<<\n\nx====================x')
        return records

    except Exception as e:
            logger.exception(e)
            raise e