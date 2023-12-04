from News_Reccomendation_System.config.configuration import ConfigurationManager
from News_Reccomendation_System.components.trending import Trending
from News_Reccomendation_System import logger





class TrendingNewsPipeline:
    def __init__(self) -> None:
        pass

    def main(self, category=None):

        config = ConfigurationManager()
        trending_api_configuration = config.get_trending_config()
        trending = Trending(config= trending_api_configuration)
        trending_records = trending.get_trending_news()
        if category:
            category_records = trending.get_category_df(category= category)
            return category_records
        return trending_records
    



STEP_NAME = ' ---- Requesting Trending API ---------'


def trending_api(category= None):
    try:
        logger.info(f' >>>>>>> Step {STEP_NAME} started <<<<<<<<<<<')
        obj = TrendingNewsPipeline()
        trends = obj.main(category= category)
        logger.info(f' >>>>>>> Step {STEP_NAME} completed <<<<<<<<<<<\n\nx====================x')
        return trends

    except Exception as e:
            logger.exception(e)
            raise e