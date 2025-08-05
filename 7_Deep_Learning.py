from paths import PM
from helpers.constants import MODEL_HIDDEN_LAYERS, INITIAL_LEARNING_RATE, DROP_OUT_RATE
import pandas

from ml_tools.path_manager import make_fullpath
from ml_tools.utilities import yield_dataframes_from_dir
from ml_tools import custom_logger

from ml_tools.ML_datasetmaster import SimpleDatasetMaker
from ml_tools.ML_models import MultilayerPerceptron, save_architecture
from ml_tools.ML_callbacks import EarlyStopping, ModelCheckpoint, LRScheduler
from ml_tools.ML_trainer import MLTrainer
from ml_tools.keys import PyTorchLogKeys

from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.optim import Adam
from torch.nn import MSELoss


def single_run(df: pandas.DataFrame, df_name: str):
    # Local directory
    local_dir = make_fullpath(PM["model metrics"] / df_name, make=True, enforce="directory")
    
    # Make dataset
    current_dataset = SimpleDatasetMaker(pandas_df=df,
                                         kind="regression")
    
    # Save feature names
    current_dataset.save_feature_names(directory=local_dir)
    
    # Define neural network architecture
    model = MultilayerPerceptron(in_features=len(current_dataset.feature_names),
                                out_targets=1,
                                hidden_layers=MODEL_HIDDEN_LAYERS,
                                drop_out=DROP_OUT_RATE)
    
    # Save architecture
    save_architecture(model=model, directory=local_dir)
    
    # define loss function
    loss_function = MSELoss()
    
    # Define optimizer
    optimizer = Adam(model.parameters(), lr=INITIAL_LEARNING_RATE)
    
    # define LR scheduler
    reduce_lr_on_plateau = ReduceLROnPlateau(optimizer=optimizer, mode='min')
    
    # Define callbacks
    callback_early_stop = EarlyStopping(monitor=PyTorchLogKeys.VAL_LOSS,
                                        mode='min',
                                        patience=10)
    
    callback_checkpoint = ModelCheckpoint(save_dir=local_dir,
                                          checkpoint_name=current_dataset.target_name,
                                          monitor=PyTorchLogKeys.VAL_LOSS,
                                          mode="min",
                                          save_best_only=True)
    
    callback_scheduler = LRScheduler(scheduler=reduce_lr_on_plateau,
                                     monitor=PyTorchLogKeys.VAL_LOSS)
    
    all_callbacks = [
        callback_early_stop,
        callback_checkpoint,
        callback_scheduler
    ]
    
    # Define Trainer
    trainer = MLTrainer(model=model,
                        train_dataset=current_dataset.train_dataset,
                        test_dataset=current_dataset.test_dataset,
                        kind="regression",
                        criterion=loss_function,
                        optimizer=optimizer,
                        device="mps",
                        dataloader_workers=4,
                        callbacks=all_callbacks)
    
    # Train model
    history_log = trainer.fit(epochs=200,
                              batch_size=8,
                              shuffle=True)
    
    # Evaluate
    trainer.evaluate(save_dir=local_dir)
    
    # Explain
    trainer.explain(save_dir=local_dir,
                    feature_names=current_dataset.feature_names)
    
    # save log
    log_dict = {
        "Task": "regression",
        "Model Architecture": repr(model),
        "Drop-out Rate": DROP_OUT_RATE,
        "Dataset": df_name,
        "Target": current_dataset.target_name,
        "Number of Features": len(current_dataset.feature_names),
        "Features": current_dataset.feature_names
    }
    
    custom_logger(data=log_dict | history_log,
                  save_directory=local_dir,
                  log_name=df_name)


def main():
    for df, df_name in yield_dataframes_from_dir(datasets_dir=PM["model datasets"]):
        single_run(df, df_name)


if __name__ == "__main__":
    main()
