import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from News_Reccomendation_System.utils.common import load_json
from News_Reccomendation_System.components.model_training import NewsMF, MindDataset
import torch

class User_Based_PredictionAPI:
    def __init__(self):
        self.model = joblib.load(Path('artifacts/model_trainer/model_user.joblib'))

    def input_user_id(self, user_id):
        ind2item = load_json(Path('artifacts/data_transformation/ind2uitem.json'))
        # print(ind2item)
        item_id = list(map(int, list(ind2item.keys())))
        userIdx =  [int(user_id)]*len(item_id)

        return ind2item, userIdx, item_id

    def get_news(self):
        df = pd.read_csv('artifacts/data_ingestion/news.tsv', 
                         sep= '\t',
                         names=["itemId","category",
                                "subcategory",
                                "title",
                                "abstract",
                                "url",
                                "title_entities",
                                "abstract_entities"])
        return df


    def predict(self, news, ind2item, userIdx, item_id):

        preditions = self.model.forward(torch.IntTensor(userIdx), torch.IntTensor(item_id))

        # Select top 10 argmax
        top_index = torch.topk(preditions.flatten(), 10).indices

        # Filter for top 10 suggested items
        filters = [ind2item[str(ix.item())] for ix in top_index]
        df = news[news["itemId"].isin(filters)]
        
        return df
    

class Content_Based_PredictionAPI:
    def __init__(self):
        self.model = joblib.load(Path('artifacts/model_trainer/model_content_based.joblib'))

    def input(self, news:str):
        news = str(news)
        return news


    def predict(self, news):
        for i, doc in enumerate(self.model.recommend(text= news, n= 5)):
            print(f'Recomed - {i+1}')
            print(" ".join(doc['text'].split()))
    

if __name__ == "__main":

    '''Test APIs'''

    obj = User_Based_PredictionAPI()
    ind2item, userIdx, item_id = obj.input_user_id(2350)  # for now
    news = obj.get_news()
    df = obj.predict(news= news,
                    ind2item= ind2item,
                    userIdx= userIdx,
                    item_id= item_id)

    print(df)


    obj2 = Content_Based_PredictionAPI()
    news = obj2.input(news = '''
    An off-duty pilot is accused of trying to shut down the engines of a Horizon Air jet in midflight
    ''')
    obj2.predict(news)

