import pandas as pd
from pathlib import Path
from News_Reccomendation_System.utils.common import load_json
from box import ConfigBox 
from News_Reccomendation_System.entity.config_entity import TrendingAPIConfig



class Trending:

    def __init__(self, config: TrendingAPIConfig):
        self.config = config

    def __to_records(self, df: pd.DataFrame):
        records = df.to_dict('records')
        records = list(map(lambda x: ConfigBox(x), records))
        return records

    def get_trending_news(self):
        tr = pd.read_csv(self.config.training_data, sep='\t')
        val = pd.read_csv(self.config.validation_data, sep='\t')
        df = pd.concat( [tr, val], ignore_index= True)
        del tr, val
        trends= df['click'].value_counts()
        trends.sort_values(ascending=False)
        news = pd.read_csv(self.config.news_data, sep='\t', names= self.config.col_name)
        js = load_json(Path(self.config.item2ind_json))
        news['news_id'] = news.itemId.apply(lambda x: js[x])
        self.trending_df = news[news['news_id'].isin(trends.index)]
        trending_records = self.__to_records(df= self.trending_df)

        return trending_records
    
    def get_category_df(self, category: str) -> pd.DataFrame:

        category_df = self.trending_df[self.trending_df['category']==category]
        category_records = self.__to_records(category_df)
        return category_records