from model import BST
import pytorch_lightning as pl
from pytorch_lightning.loggers import TensorBoardLogger

model = BST()
# Create a logger for the outputs of the training
logger = TensorBoardLogger(save_dir="lightning_logs/", name="my_experiment")


trainer = pl.Trainer(accelerator='auto', max_epochs=5, logger=logger)
trainer.fit(model)