from News_Reccomendation_System import logger
# One very odd question may arise to mind tht why did we not import it like 
# from src.portfolio_project_one
# mentioning src was not necesarry because we pip installed the project_porfolio_one as a library when we wrote our setup.py and ran -e . 
# and ran -e . in our requirements.txt

logger.info("Welcome to   SWARAJ BARI' s  News Reccomendation System Project")



from News_Reccomendation_System.pipeline.step1_data_ingestion import run_data_ingestion
from News_Reccomendation_System.pipeline.step2_data_transformation import run_data_transformation
from News_Reccomendation_System.pipeline.step3_model_training import run_model_trainer





run_data_ingestion()  # run data ingestion pipeline
run_data_transformation()  # run data transformation pipeline
run_model_trainer()  # run model trainer
