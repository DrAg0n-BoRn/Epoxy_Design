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
from ml_tools.ML_models import DragonAttentionMLP
from ml_tools.ML_configuration import (
    FormatMultiClassClassificationMetrics,
    FinalizeMultiClassClassification,
    DragonAttentionMLPParams
)

from ml_tools.ML_configuration import DragonTrainingConfig
from ml_tools.ML_trainer import DragonTrainer
from ml_tools.ML_callbacks import DragonModelCheckpoint, DragonPatienceEarlyStopping, DragonPlateauScheduler
from ml_tools.ML_utilities import build_optimizer_params
from ml_tools.ML_utilities import inspect_model_architecture
from ml_tools.utilities import load_dataframe
from ml_tools.path_manager import make_fullpath
from ml_tools.IO_tools import train_logger
from ml_tools.data_exploration import encode_classification_target
from ml_tools.schema import FeatureSchema
from ml_tools.keys import TaskKeys
from torch.optim import AdamW
from ml_tools.ML_chain import prepare_chaining_dataset

from paths import PM
from helpers.constants import FILLER as CLASSIFICATION_TARGET
```

```python
SCHEMA_PATH = PM.engineering_artifacts
TRAIN_DATASET_FILE = PM.imputed_data_file

TRAIN_ARTIFACTS_DIR = PM.classification_filler
TRAIN_CHECKPOINTS_DIR = TRAIN_ARTIFACTS_DIR / "Checkpoints"
TRAIN_EVALUATION_DIR = TRAIN_ARTIFACTS_DIR / "Evaluation"
```

## 1. Config

```python
train_config = DragonTrainingConfig(
    validation_size=0.1,
    test_size=0.1,
    initial_learning_rate=0.001,
    batch_size=64,
    task = TaskKeys.MULTICLASS_CLASSIFICATION,
    device = "cuda",
    finalized_filename = "classification_" + CLASSIFICATION_TARGET,
    random_state=101,
    
    target=CLASSIFICATION_TARGET,
    weight_decay=0.01,
    early_stop_patience=20,
    scheduler_patience=3,
    scheduler_lr_factor=0.5,    
)
```

## 2. Load Schema and Dataframe

```python
schema = FeatureSchema.from_json(SCHEMA_PATH)

df_full, _ = load_dataframe(df_path=TRAIN_DATASET_FILE, use_columns=list(schema.continuous_feature_names) + [CLASSIFICATION_TARGET])

df_nn = prepare_chaining_dataset(dataset=df_full, all_targets=[CLASSIFICATION_TARGET], target_subset=[CLASSIFICATION_TARGET])
```

```python
# Encode
df, class_map = encode_classification_target(df=df_nn, target_col=CLASSIFICATION_TARGET, save_dir=TRAIN_ARTIFACTS_DIR)
```

## 3. Make Datasets

```python
dataset = DragonDataset(pandas_df=df,
                        schema=schema,
                        kind=train_config.task,
                        feature_scaler="fit",
                        target_scaler="none",
                        validation_size=train_config.validation_size,
                        test_size=train_config.test_size,
                        random_state=train_config.random_state,
                        class_map=class_map
                        )
```

## 4. Model and Trainer

```python
model_params = DragonAttentionMLPParams(
    in_features=dataset.number_of_features,
    out_targets=len(class_map),
    hidden_layers=[50,100,200,200,100,50],
    drop_out=0.0
)

model = DragonAttentionMLP(**model_params)

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
                val_format_configuration=FormatMultiClassClassificationMetrics(cmap="BuGn",
                                                                               ROC_PR_line='darkorange'),
                test_format_configuration=FormatMultiClassClassificationMetrics(cmap="BuPu",
                                                                                ROC_PR_line='tab:cyan')
                # classification_threshold=0.5 # for Classification tasks
                )
```

## 7. Explanation

```python
trainer.explain_captum(save_dir=TRAIN_EVALUATION_DIR,
                       n_samples=400,
                       n_steps=200,
                       target_names=list(class_map.keys()))
```

```python
trainer.explain_attention(save_dir=TRAIN_EVALUATION_DIR)
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
                                finalize_config=FinalizeMultiClassClassification(filename=train_config.finalized_filename,
                                                                                 target_name=dataset.target_names[0],
                                                                                 class_map=class_map)
                                )
```
