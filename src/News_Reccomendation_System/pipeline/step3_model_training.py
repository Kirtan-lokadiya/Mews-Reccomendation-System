from News_Reccomendation_System.config.configuration import ConfigurationManager
from News_Reccomendation_System.components.model_training import ModelTrainer
from News_Reccomendation_System import logger



STEP_NAME = '04 ---- Model Training Step'



class ModelTrainingPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config= model_trainer_config)
        train, valid = model_trainer.get_data()
        ind2item, ind2user = model_trainer.get_hashes()
        train_loader, valid_loader = model_trainer.build_datasets(train= train,
                                                                  valid= valid)
        model_trainer.model_training(train_loader= train_loader,
                                     valid_loader= valid_loader,
                                     ind2item= ind2item,
                                     ind2user= ind2user)
        model_trainer.model_training_2()
        
        


def run_model_trainer():

    try:
        logger.info(f' >>>>>>> Step {STEP_NAME} started <<<<<<<<<<<')
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f' >>>>>>> Step {STEP_NAME} completed <<<<<<<<<<<\n\nx====================x')

    except Exception as e:
            logger.exception(e)
            raise e