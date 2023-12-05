import pandas as pd
from pathlib import Path
from News_Reccomendation_System.utils.common import load_json
from box import ConfigBox 
from News_Reccomendation_System.entity.config_entity import FullNewsConfig



class FullNews:

    def __init__(self, config: FullNewsConfig):
        self.config = config

    def __to_records(self, df: pd.DataFrame):
        records = df.to_dict('records')
        records = list(map(lambda x: ConfigBox(x), records))
        return records

    def get_full_news(self, news_id):
        news = pd.read_csv(self.config.news_data, sep='\t', names= self.config.col_name)
        js = load_json(Path(self.config.item2ind_json))
        itemId = js[news_id]
        self.trending_df = news[news['itemId'] == itemId]
        trending_records = self.__to_records(df= self.trending_df)

        return trending_records
    