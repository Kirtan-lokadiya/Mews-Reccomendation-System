import os
from News_Reccomendation_System import logger
from News_Reccomendation_System.utils.common import save_json
import pandas as pd
import numpy as np
from pathlib import Path
from News_Reccomendation_System.entity.config_entity import DataTransformationConfig

class DataTransformtion:
    def __init__(self, config: DataTransformationConfig):
        self.config = config



    def user_data(self):
        df = pd.read_csv(self.config.data_path_usr,
                         sep="\t",
                         names=["impressionId",
                                "userId",
                                "timestamp",
                                "click_history",
                                "impressions"]
                                )
        return df
    
    def news_data(self):
        df = pd.read_csv(self.config.data_path_news,
                         sep='\t',
                         names=["itemId",
                                "category",
                                "subcategory",
                                "title","abstract",
                                "url",
                                "title_entities",
                                "abstract_entities"]
                                )
        return df
    
    def indexize_users(self, raw_behaviour: pd.DataFrame):
        ## Indexize users
        unique_userIds = raw_behaviour['userId'].unique()
        # Allocate a unique index for each user, but let the zeroth index be a UNK index:
        ind2user = {idx +1: itemid for idx, itemid in enumerate(unique_userIds)}
        user2ind = {itemid : idx for idx, itemid in ind2user.items()}
        print(f"We have {len(user2ind)} unique users in the dataset")

        save_json(path= Path(os.path.join(self.config.root_dir, 'ind2user.json')), data= ind2user)
        # Create a new column with userIdx:
        raw_behaviour['userIdx'] = raw_behaviour['userId'].map(lambda x: user2ind.get(x,0))
                
        return raw_behaviour
    
    def get_iten2ind_hash(self, news :pd.DataFrame):
        ind2item = {idx +1: itemid for idx, itemid in enumerate(news['itemId'].values)}
        item2ind = {itemid : idx for idx, itemid in ind2item.items()}

        save_json(path= Path(os.path.join(self.config.root_dir, 'ind2uitem.json')), data= ind2item)

        return item2ind
    
    def indexise_click_history(self, item2ind: dict, raw_behaviour: pd.DataFrame):

        def process_click_history(s):
            list_of_strings = str(s).split(" ")
            return [item2ind.get(l, 0) for l in list_of_strings]

        raw_behaviour['click_history_idx'] = raw_behaviour.click_history.map(lambda s:  process_click_history(s))

        return raw_behaviour
    

    def one_click_no_click(self, item2ind: dict, raw_behaviour: pd.DataFrame):

        def process_impression(s):
            list_of_strings = s.split(" ")
            itemid_rel_tuple = [l.split("-") for l in list_of_strings]
            noclicks = []
            for entry in itemid_rel_tuple:
                if entry[1] =='0':
                    noclicks.append(entry[0])
                if entry[1] =='1':
                    click = entry[0]
            return noclicks, click

        raw_behaviour['noclicks'], raw_behaviour['click'] = zip(*raw_behaviour['impressions'].map(process_impression))
        # We can then indexize these two new columns:
        raw_behaviour['noclicks'] = raw_behaviour['noclicks'].map(lambda list_of_strings: [item2ind.get(l, 0) for l in list_of_strings])
        raw_behaviour['click'] = raw_behaviour['click'].map(lambda x: item2ind.get(x,0))

        return raw_behaviour


    def conver_datetime_to_hrs(self, raw_behaviour: pd.DataFrame):

        raw_behaviour['epochhrs'] = pd.to_datetime(raw_behaviour['timestamp']).values.astype(np.int64)/(1e6)/1000/3600
        raw_behaviour['epochhrs'] = raw_behaviour['epochhrs'].round()

        return raw_behaviour
    

    def get_user_behaviour(self, raw_behaviour: pd.DataFrame):

        raw_behaviour['noclick'] = raw_behaviour['noclicks'].map(lambda x : x[0])
        behaviour = raw_behaviour[['epochhrs','userIdx','click_history_idx','noclick','click']]

        return behaviour
    

    def train_test_spilt_behaviour(self, behaviour):

        # Let us use the last 10pct of the data as our validation data:
        test_time_th = behaviour['epochhrs'].quantile(0.9)
        train = behaviour[behaviour['epochhrs']< test_time_th]
        valid =  behaviour[behaviour['epochhrs']>= test_time_th]

        train.to_csv(os.path.join(self.config.root_dir, 'train.tsv'), index = False, sep= '\t')
        valid.to_csv(os.path.join(self.config.root_dir, 'valid.tsv'), index = False, sep= '\t')

