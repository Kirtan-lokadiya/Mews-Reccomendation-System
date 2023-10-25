#  Components

import os
from typing import Any
from pathlib import Path
from News_Reccomendation_System import logger
from News_Reccomendation_System.utils.common import load_json
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import torch.nn as nn
import pytorch_lightning as pl
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import torch
import joblib
import ktrain

from News_Reccomendation_System.entity.config_entity import ModelTrainerConfig


class MindDataset(Dataset):
    # A fairly simple torch dataset module that can take a pandas dataframe (as above), 
    # and convert the relevant fields into a dictionary of arrays that can be used in a dataloader
    def __init__(self, df):
        # Create a dictionary of tensors out of the dataframe
        self.data = {
            'userIdx' : torch.tensor(df.userIdx.values),
            'click' : torch.tensor(df.click.values),
            'noclick' : torch.tensor(df.noclick.values)
        }
    def __len__(self):
        return len(self.data['userIdx'])
    def __getitem__(self, idx):
        return {key: val[idx] for key, val in self.data.items()}
    

# Build a matrix factorization model
class NewsMF(pl.LightningModule):
    def __init__(self, num_users, num_items, dim = 10):
        super().__init__()
        self.dim=dim
        self.useremb = nn.Embedding(num_embeddings=num_users, embedding_dim=dim)
        self.itememb = nn.Embedding(num_embeddings=num_items, embedding_dim=dim)
    
    def forward(self, user, item):
        batch_size = user.size(0)
        uservec = self.useremb(user)
        itemvec = self.itememb(item)

        score = (uservec*itemvec).sum(-1).unsqueeze(-1)
        
        return score
    
    def training_step(self, batch, batch_idx):
        batch_size = batch['userIdx'].size(0)

        score_click = self.forward(batch['userIdx'], batch['click'])
        score_noclick = self.forward(batch['userIdx'], batch['noclick'])
        
        scores_all = torch.concat((score_click, score_noclick), dim=1)
        # Compute loss as cross entropy (categorical distribution between the clicked and the no clicked item)
        loss = F.cross_entropy(input=scores_all, target=torch.zeros(batch_size, device=scores_all.device).long())
        return loss
    
    def validation_step(self, batch, batch_idx):
        # for now, just do the same computation as during training
        loss = self.training_step(batch, batch_idx)
        self.log("val_loss", loss, prog_bar=True, on_step=False, on_epoch=True)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer


class ModelTrainer:

    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def get_data(self):
        train = pd.read_csv(self.config.train_data_path, sep= '\t')
        valid = pd.read_csv(self.config.test_data_path, sep= '\t')

        return train, valid

    def get_hashes(self):
        ind2user = load_json(Path(self.config.ind2user))
        ind2item = load_json(Path(self.config.ind2item))

        return ind2item, ind2user
            

    def build_datasets(self, train, valid):
        bs = self.config.batch_size
        ds_train = MindDataset(train)
        train_loader = DataLoader(ds_train, batch_size=bs, shuffle=True)
        ds_valid = MindDataset(valid)
        valid_loader = DataLoader(ds_valid, batch_size=bs, shuffle=False)

        # batch = next(iter(train_loader))
        
        return train_loader, valid_loader
    
    def model_training(self, train_loader, valid_loader, ind2item, ind2user):

        mf_model = NewsMF(num_users=len(ind2user)+1, num_items = len(ind2item)+1)
    
        trainer = pl.Trainer(max_epochs=10)
        trainer.fit(model=mf_model, train_dataloaders=train_loader, val_dataloaders=valid_loader)

        joblib.dump(mf_model, os.path.join(self.config.root_dir, self.config.model_name))

    def model_training_2(self):
        df = pd.read_csv(self.config.news, sep= '\t',
                         names=["itemId","category",
                                "subcategory",
                                "title",
                                "abstract",
                                "url",
                                "title_entities",
                                "abstract_entities"])

        df.dropna(inplace= True)
        df.drop_duplicates(inplace= True)
        df['article'] = df.apply(lambda row: row['title'] + row['abstract'], axis= 1)
        corpus = list(df['article'])
        del df
        tm = ktrain.text.get_topic_model(texts= corpus, n_features= 100000)
        tm.build(corpus, threshold= 0.25)
        tm.train_recommender()

        joblib.dump(tm, os.path.join(self.config.root_dir, self.config.model_content))

