from News_Reccomendation_System.config.configuration import ConfigurationManager
from News_Reccomendation_System.components.data_transformation import DataTransformtion
from News_Reccomendation_System import logger





STEP_NAME = '03 ---- Data Transformation Step'



class DataTransformationPipeline:
    def __init__(self) -> None:
        pass
    
    def main(self):
        


        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformtion(config= data_transformation_config)
        raw_behaviour = data_transformation.user_data()
        news = data_transformation.news_data()
        item2ind = data_transformation.get_iten2ind_hash(news= news)
        raw_behaviour = data_transformation.indexize_users(raw_behaviour= raw_behaviour)
        raw_behaviour = data_transformation.indexise_click_history(raw_behaviour= raw_behaviour, item2ind= item2ind)
        raw_behaviour = data_transformation.one_click_no_click(raw_behaviour= raw_behaviour, item2ind= item2ind)
        raw_behaviour = data_transformation.conver_datetime_to_hrs(raw_behaviour= raw_behaviour)
        behaviour = data_transformation.get_user_behaviour(raw_behaviour= raw_behaviour)
        data_transformation.train_test_spilt_behaviour(behaviour= behaviour)
            
            
            





def run_data_transformation():
    try:
        logger.info(f' >>>>>>> Step {STEP_NAME} started <<<<<<<<<<<')
        obj = DataTransformationPipeline()
        obj.main()
        logger.info(f' >>>>>>> Step {STEP_NAME} completed <<<<<<<<<<<\n\nx====================x')

    except Exception as e:
            logger.exception(e)
            raise e
