import torch
import os
import torch.nn as nn
import math
import pandas as pd
import torchmetrics
import pytorch_lightning as pl


class CTRTransformer(pl.LightningModule):
    def __init__(
        self, args=None,
    ):
        super().__init__()
        super(CTRTransformer, self).__init__()
        
        self.save_hyperparameters()
        self.args = args
        #-------------------
        # Embedding layers
        ##Users 
        self.embeddings_user_id = nn.Embedding(
            int(users.user_id.astype(int).max())+1, int(math.sqrt(users.user_id.astype(int).max()))+1
        )
        ###Users features embeddings
        self.embeddings_user_sex = nn.Embedding(
            len(users.sex.unique()), int(math.sqrt(len(users.sex.unique())))
        )
        self.embeddings_age_group = nn.Embedding(
            len(users.age_group.unique()), int(math.sqrt(len(users.age_group.unique())))
        )
        self.embeddings_user_occupation = nn.Embedding(
            len(users.occupation.unique()), int(math.sqrt(len(users.occupation.unique())))
        )
        self.embeddings_user_zip_code = nn.Embedding(
            len(users.zip_code.unique()), int(math.sqrt(len(users.sex.unique())))
        )
        
        ##Movies
        self.embeddings_movie_id = nn.Embedding(
            int(movies.movie_id.astype(int).max())+1, int(math.sqrt(movies.movie_id.astype(int).max()))+1
        )
        
        ###Movies features embeddings
        genre_vectors = movies[genres].to_numpy()
        self.embeddings_movie_genre = nn.Embedding(
            genre_vectors.shape[0], genre_vectors.shape[1]
        )
        
        
        
        self.embeddings_movie_year = nn.Embedding(
            len(movies.year.unique()), int(math.sqrt(len(movies.year.unique())))
        )
        
        self.positional_embedding = PositionalEncoding(8, 9)
        
        # Network
        self.transfomerlayer = nn.TransformerEncoderLayer(72, 3, dropout=0.2)
        self.linear = nn.Sequential(
            nn.Linear(
                661,
                1024,
            ),
            nn.LeakyReLU(),
            nn.Linear(1024, 512),
            nn.LeakyReLU(),
            nn.Linear(512, 256),
            nn.LeakyReLU(),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

        self.criterion = torch.nn.MSELoss()
        self.mae = torchmetrics.MeanAbsoluteError()
        self.mse = torchmetrics.MeanSquaredError()
        


    def encode_input(self,inputs):
        user_id, movie_history, target_movie_id,  movie_history_ratings, target_movie_rating, sex, age_group, occupation = inputs
               
        #MOVIES
        movie_history = self.embeddings_movie_id(movie_history)
        target_movie = self.embeddings_movie_id(target_movie_id)
         
        target_movie = torch.unsqueeze(target_movie, 1)
        transfomer_features = torch.cat((movie_history, target_movie),dim=1)

        #USERS
        user_id = self.embeddings_user_id(user_id)
        
        sex = self.embeddings_user_sex(sex)
        age_group = self.embeddings_age_group(age_group)
        occupation = self.embeddings_user_occupation(occupation)
        user_features = torch.cat((user_id, sex, age_group,occupation), 1)
        
        return transfomer_features, user_features, target_movie_rating.float()
    
    def forward(self, batch):
        transfomer_features, user_features, target_movie_rating = self.encode_input(batch)
        positional_embedding = self.positional_embedding(transfomer_features)
        transfomer_features = torch.cat((transfomer_features, positional_embedding), dim=2)
        transformer_output = self.transfomerlayer(transfomer_features)
        transformer_output = torch.flatten(transformer_output,start_dim=1)
        
        #Concat with other features
        features = torch.cat((transformer_output,user_features),dim=1)

        output = self.linear(features)
        return output, target_movie_rating
        
    def training_step(self, batch, batch_idx):
        out, target_movie_rating = self(batch)
        out = out.flatten()
        loss = self.criterion(out, target_movie_rating)
        
        mae = self.mae(out, target_movie_rating)
        mse = self.mse(out, target_movie_rating)
        rmse =torch.sqrt(mse)
        
        self.log(
            "train/mae", mae, on_step=True, on_epoch=True, prog_bar=True
        )
        
        self.log(
            "train/rmse", rmse, on_step=True, on_epoch=True, prog_bar=True
        )
        
        self.log("train/step_loss", loss, on_step=True, on_epoch=False, prog_bar=False)
        return loss

    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=0.0005)

    def setup(self, stage=None):
        print("Loading datasets")
        self.train_dataset = MovieDataset("data/train_data.csv")
        self.val_dataset = MovieDataset("data/test_data.csv")
        self.test_dataset = MovieDataset("data/test_data.csv")
        print("Done")

    def train_dataloader(self):
        return torch.utils.data.DataLoader(
            self.train_dataset,
            batch_size=128,
            shuffle=False,,
            num_workers=os.cpu_count(),
        )

    def val_dataloader(self):
        return torch.utils.data.DataLoader(
            self.val_dataset,
            batch_size=128,
            shuffle=False,
            num_workers=os.cpu_count(),
        )

    def test_dataloader(self):
        return torch.utils.data.DataLoader(
            self.test_dataset,
            batch_size=128,
            shuffle=False,
            num_workers=os.cpu_count(),
        )
        

    
