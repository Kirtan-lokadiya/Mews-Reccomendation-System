import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from News_Reccomendation_System.utils.common import load_json
from News_Reccomendation_System.components.model_training import NewsMF, MindDataset
import torch

class User_Based_Prediction:
    def __init__(self):
        self.model = joblib.load(Path('artifacts/model_trainer/model_user.joblib'))

    def input_user_id(self, user_id):
        self.ind2item = load_json(Path('artifacts/data_transformation/ind2uitem.json'))
        # print(ind2item)
        self.item_id = list(map(int, list(self.ind2item.keys())))
        self.userIdx =  [int(user_id)]*len(self.item_id)

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
        self.news = df


    def predict(self):

        preditions = self.model.forward(torch.IntTensor(self.userIdx), torch.IntTensor(self.item_id))

        # Select top 10 argmax
        top_index = torch.topk(preditions.flatten(), 500).indices

        # Filter for top 10 suggested items
        filters = [self.ind2item[str(ix.item())] for ix in top_index]
        df = self.news[self.news["itemId"].isin(filters)]
        
        return df
    

class Content_Based_Prediction:
    def __init__(self):
        self.model = joblib.load(Path('artifacts/model_trainer/model_content_based.joblib'))

    def input(self, news:str):
        news = str(news)
        return news


    def predict(self, news):
        reccomendations = []
        for i, doc in enumerate(self.model.recommend(text= news, n= 10)):
            # print(f'Recomed - {i+1}')
            # print(doc['text'])
            reccomendations.append(doc['text'])


def user_based_rec_api(user_id):

    obj = User_Based_Prediction()
    obj.input_user_id(user_id= user_id)
    

if __name__ == "__main__":

    '''Test APIs'''

    # obj = User_Based_PredictionAPI()
    # ind2item, userIdx, item_id = obj.input_user_id(2350)  # for now
    # news = obj.get_news()
    # df = obj.predict(news= news,
    #                 ind2item= ind2item,
    #                 userIdx= userIdx,
    #                 item_id= item_id)

    # print(df)


    obj2 = Content_Based_PredictionAPI()
    news = obj2.input(news = '''
    25 Biggest Grocery Store Mistakes Making You Gain WeightFrom picking up free goodies to navigating the wrong aisles, these grocery shopping mistakes could be one of the sneaky reasons you're gaining weight.
    ''')
    obj2.predict(news)

