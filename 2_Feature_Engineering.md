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

# Feature Engineering

```python
from ml_tools.data_exploration import info
info()
```

```python
from ml_tools.data_exploration import (summarize_dataframe,
                                       show_null_columns,
                                       drop_macro,
                                       clean_column_names,
                                       plot_value_distributions,
                                       split_continuous_categorical_targets,
                                       clip_outliers_multi,
                                       plot_continuous_vs_target,
                                       plot_categorical_vs_target,
                                       plot_correlation_heatmap,
                                       check_class_balance,
                                       finalize_feature_schema)
from ml_tools.utilities import load_dataframe, save_dataframe_with_schema, merge_dataframes
from ml_tools.IO_tools import save_json

from paths import PM
from helpers.constants import TARGETS_REGRESSION, TARGETS_CLASSIFICATION, TENSILE_STRENGTH, FLEXURAL_STRENGTH, EPOXY_CURING_RATIO, FILLER_PROPORTION, TEMPERATURE, EPOXY, CURING, FILLER
```

## 1 Load data

```python
df_start, _ = load_dataframe(df_path=PM.processed_data_file, kind="pandas")
```

```python
# Filter and keep rows with epoxy E-51 only, then drop the epoxy column
df_start = df_start[df_start[EPOXY] == "E-51"].drop(columns=[EPOXY]).copy()
```

```python
summarize_dataframe(df_start)
```

## 2 Clean Data

```python
df_clean_I = drop_macro(df=df_start,
           log_directory=PM.engineering_plots,
           targets=TARGETS_REGRESSION + TARGETS_CLASSIFICATION,
           skip_targets=True,
           threshold=0.8)
```

```python
df_clean_II = clean_column_names(df_clean_I, replacement_char=" ")
```

```python
df_clean = df_clean_II
summarize_dataframe(df_clean)
```

```python
show_null_columns(df_clean)
```

## 3. Value distribution

```python
plot_value_distributions(df=df_clean, save_dir=PM.engineering_plots)
```

## 4 Split data

```python
df_clean.dtypes
```

```python
df_continuous, df_classification_targets, df_regression_targets = split_continuous_categorical_targets(df=df_clean, 
                                                                                                       categorical_cols=TARGETS_CLASSIFICATION, 
                                                                                                       target_cols=TARGETS_REGRESSION)
```

## 5 Clip Outliers

```python
summarize_dataframe(df_continuous)
```

```python
CONTINUOUS_CLIP_RANGE = {
    EPOXY_CURING_RATIO: (1,10),
    FILLER_PROPORTION: (1,30),
    TEMPERATURE: (295,450),
}

df_continuous_clip = clip_outliers_multi(df=df_continuous, clip_dict=CONTINUOUS_CLIP_RANGE)
```

```python
summarize_dataframe(df_regression_targets)
```

```python
TARGETS_CLIP_RANGE = {
    TENSILE_STRENGTH: (0.1,100), 
    FLEXURAL_STRENGTH: (10,175), 
    # ELONGATION_AT_BREAK: (0.1,20), 
    # IMPACT_STRENGTH: (0.1,80)
}

df_regression_targets_clip = clip_outliers_multi(df=df_regression_targets, clip_dict=TARGETS_CLIP_RANGE)
```

## 6 Plots

```python
plot_continuous_vs_target(df_continuous=df_continuous_clip, df_targets=df_regression_targets_clip, save_dir=PM.engineering_plots)
```

```python
plot_categorical_vs_target(df_categorical=df_classification_targets, df_targets=df_continuous_clip, save_dir=PM.engineering_plots, max_categories=90)
```

```python
plot_correlation_heatmap(df=df_continuous_clip, save_dir=PM.engineering_plots, plot_title="Continuous Features")
```

```python
plot_correlation_heatmap(df=df_regression_targets_clip, save_dir=PM.engineering_plots, plot_title="Regression Targets")
```

## 7 Merge datasets

```python
# final dataset
df_final = merge_dataframes(df_continuous_clip, df_regression_targets_clip, df_classification_targets)
summarize_dataframe(df_final)
```

## 8 Check Class Balance for classification targets

```python
for classification_target in TARGETS_CLASSIFICATION:
    check_class_balance(df=df_final, target=classification_target, plot_to_dir=PM.engineering_plots, plot_filename=f"{classification_target}_class_balance")
```

## 9 Make FeatureSchema

```python
feature_schema = finalize_feature_schema(df_features=df_continuous_clip, categorical_mappings=None)
```

## 10 Save dataframe

```python
save_dataframe_with_schema(df=df_final, full_path=PM.engineering_data_file, schema=feature_schema)
```

## 11 Save artifacts

```python
# Save feature schema
feature_schema.to_json(PM.engineering_artifacts)
```

```python
feature_schema.save_artifacts(PM.engineering_artifacts)
```

```python
# Save used ranges for continuous data
save_json(data=CONTINUOUS_CLIP_RANGE | TARGETS_CLIP_RANGE,
          directory=PM.engineering_artifacts,
          filename="Clip Range")
```
