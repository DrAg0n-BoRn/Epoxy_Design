---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.1
  kernelspec:
    display_name: dragon-mice
    language: python
    name: python3
---

```python
from ml_tools.MICE import DragonMICE
from ml_tools.schema import FeatureSchema
from ml_tools.path_manager import safe_move, list_csv_paths
from ml_tools.utilities import load_dataframe
from ml_tools.VIF import compute_vif

from paths import PM
from helpers.constants import TARGETS_REGRESSION
```

## 1. MICE

```python
schema = FeatureSchema.from_json(PM.engineering_artifacts)

mice_imputer = DragonMICE(schema=schema,
                        impute_targets=False)
    
mice_imputer.run_pipeline(df_path_or_dir=PM.engineering_data_file,
                        save_datasets_dir=PM.mice_datasets,
                        save_metrics_dir=PM.mice_metrics)
```

## 2. Select training dataset

```python
all_csv_dict = list_csv_paths(directory=PM.mice_datasets)
```

```python
safe_move(source=all_csv_dict["engineered_data_MICE"],
          destination_directory=PM.datasets,
          rename=PM.imputed_data_file.stem)
```

## 3. VIF

```python
df, _ = load_dataframe(df_path=PM.imputed_data_file, kind="pandas")
```

```python
vif_df = compute_vif(df=df,
                    ignore_columns=TARGETS_REGRESSION,
                    save_dir=PM.vif,
                    show_plot=True)
```
