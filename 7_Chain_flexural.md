---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.1
  kernelspec:
    display_name: epoxydesign
    language: python
    name: python3
---

```python
from ml_tools.ML_datasetmaster import DragonDataset
from ml_tools.ML_models import DragonTabNet
from ml_tools.ML_configuration import (
    FormatRegressionMetrics,
    FinalizeRegression, 
    DragonTabNetParams,  
    DragonTrainingConfig
)

from ml_tools.ML_trainer import DragonTrainer
from ml_tools.ML_callbacks import DragonModelCheckpoint, DragonPatienceEarlyStopping, DragonPlateauScheduler
from ml_tools.ML_utilities import build_optimizer_params
from ml_tools.ML_utilities import inspect_model_architecture
from ml_tools.utilities import load_dataframe_with_schema
from ml_tools.IO_tools import train_logger
from ml_tools.path_manager import make_fullpath
from ml_tools.schema import FeatureSchema
from ml_tools.keys import TaskKeys

from torch.optim import AdamW

from paths import PM
from helpers.constants import FLEXURAL_STRENGTH as REGRESSION_TARGET
```

```python
SCHEMA_PATH = PM.chain_artifacts2
TRAIN_DATASET_FILE = PM.chain_flexural_file

TRAIN_ARTIFACTS_DIR = PM.chain_flexural
TRAIN_CHECKPOINTS_DIR = TRAIN_ARTIFACTS_DIR / "Checkpoints"
TRAIN_EVALUATION_DIR = TRAIN_ARTIFACTS_DIR / "Evaluation"

PM.make_dirs()
```

## 1. Config

```python
train_config = DragonTrainingConfig(
    validation_size=0.2,
    test_size=0.1,
    initial_learning_rate=0.001,
    batch_size=64,
    task = TaskKeys.REGRESSION,
    device = "cuda",
    finalized_filename = "regression_" + REGRESSION_TARGET,
    random_state=101,
    
    target = REGRESSION_TARGET,
    weight_decay=0.01,
    early_stop_patience=20,
    scheduler_patience=3,
    scheduler_lr_factor=0.5,
)
```

## 2. Load Schema and Dataframe

```python
schema = FeatureSchema.from_json(SCHEMA_PATH)

df, _ = load_dataframe_with_schema(df_path=TRAIN_DATASET_FILE, schema=schema)
```

## 3. Make Datasets

```python
dataset = DragonDataset(pandas_df=df,
                        schema=schema,
                        kind=train_config.task,
                        feature_scaler="fit",
                        target_scaler="fit",
                        validation_size=train_config.validation_size,
                        test_size=train_config.test_size,
                        random_state=train_config.random_state,
                        )
```

## 4. Model and Trainer

```python
model_params = DragonTabNetParams(
    schema=schema,
    out_targets=dataset.number_of_targets,
    n_d=16,
    n_a=16,
    n_steps=4,
    gamma=1.0,
    n_independent=2,
    n_shared=5,
    virtual_batch_size=512,
    momentum=0.05,
    mask_type='sparsemax',
    batch_norm_continuous=True
)

model = DragonTabNet(**model_params)
# Initialize decision thresholds before training.
model.data_aware_initialization(train_dataset=dataset.train_dataset, num_samples=1000)

# optimizer
optim_params = build_optimizer_params(model=model, weight_decay=train_config.weight_decay)
optimizer = AdamW(params=optim_params, lr=train_config.initial_learning_rate)

trainer = DragonTrainer(model=model,
                        train_dataset=dataset.train_dataset,
                        validation_dataset=dataset.validation_dataset,
                        kind=train_config.task,
                        optimizer=optimizer,
                        device=train_config.device,
                        checkpoint_callback=DragonModelCheckpoint(save_dir=TRAIN_CHECKPOINTS_DIR, 
                                                                  monitor="Validation Loss"),
                        early_stopping_callback=DragonPatienceEarlyStopping(patience=train_config.early_stop_patience, 
                                                                            monitor="Validation Loss"),
                        lr_scheduler_callback=DragonPlateauScheduler(monitor="Validation Loss",
                                                                     patience=train_config.scheduler_patience,
                                                                     factor=train_config.scheduler_lr_factor),  
                        )

# Make paths
for local_path in [TRAIN_ARTIFACTS_DIR, TRAIN_CHECKPOINTS_DIR, TRAIN_EVALUATION_DIR]:
    _ = make_fullpath(local_path, make=True, enforce="directory")
```

## 5. Training

```python
history = trainer.fit(save_dir=TRAIN_ARTIFACTS_DIR, epochs=500, batch_size=train_config.batch_size)
```

## 6. Evaluation

```python
trainer.evaluate(save_dir=TRAIN_EVALUATION_DIR,
                model_checkpoint="best",
                test_data=dataset.test_dataset,
                val_format_configuration=FormatRegressionMetrics(scatter_color='tab:pink'),
                test_format_configuration=FormatRegressionMetrics(scatter_color='tab:green'),
                )
```

## 7. Explanation

```python
trainer.explain_captum(save_dir=TRAIN_EVALUATION_DIR,
                       n_samples=1000,
                       n_steps=500)
```

## 8. Save artifacts

```python
# Dataset artifacts
dataset.save_artifacts(TRAIN_ARTIFACTS_DIR)

# Model artifacts
model.save_architecture(TRAIN_ARTIFACTS_DIR)
inspect_model_architecture(model=model, save_dir=TRAIN_ARTIFACTS_DIR)

# FeatureSchema
schema.to_json(TRAIN_ARTIFACTS_DIR)

# Train log
train_logger(train_config=train_config,
             model_parameters=model_params,
             train_history=history,
             save_directory=TRAIN_ARTIFACTS_DIR)
```

## 9. Finalize Deep Learning

```python
trainer.finalize_model_training(model_checkpoint='current',
                                save_dir=TRAIN_ARTIFACTS_DIR,
                                finalize_config=FinalizeRegression(filename=train_config.finalized_filename,
                                                                    target_name=dataset.target_names[0]))
```
