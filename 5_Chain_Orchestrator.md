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

# Multi-Output Learning: Regressor Chains


<table>
  <thead>
    <tr>
      <th>Step</th>
      <th>Input Data</th>
      <th>Predicted Target(s)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Base Features</td>
      <td>Tensile Strength</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Base Features + Tensile Strength</td>
      <td>Flexural Strength</td>
    </tr>
    <!-- <tr>
      <td>3</td>
      <td>Base Features + Tensile Strength + Flexural Strength</td>
      <td>Elongation at Break<br>Impact Strength</td>
    </tr> -->
  </tbody>
</table>

```python
from ml_tools.ML_chain import DragonChainOrchestrator, derive_next_step_schema
from ml_tools.ML_inference import DragonInferenceHandler
from ml_tools.ML_utilities import DragonArtifactFinder
from ml_tools.ML_models import DragonNodeModel
from ml_tools.data_exploration import summarize_dataframe
from ml_tools.utilities import load_dataframe, save_dataframe_with_schema
from ml_tools.schema import FeatureSchema
import torch

from paths import PM
from helpers.constants import TENSILE_STRENGTH, FLEXURAL_STRENGTH, TARGETS_CLASSIFICATION
```

## Init

```python
imputed_df, _ = load_dataframe(df_path=PM.imputed_data_file)
```

```python
df_chain = imputed_df.drop(columns=TARGETS_CLASSIFICATION)
```

```python
chain_orchestrator = DragonChainOrchestrator(initial_dataset=df_chain,
                                             all_targets=[TENSILE_STRENGTH, FLEXURAL_STRENGTH])
```

```python
# Helper function
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def update_chain_orchestrator(artifacts_directory, model_class, previous_schema: FeatureSchema):
    finder = DragonArtifactFinder(directory=artifacts_directory, load_scaler=True, load_schema=False)
    
    inference_model = model_class.load_architecture(finder.model_architecture_path)
    
    handler = DragonInferenceHandler(model=inference_model,
                                    state_dict=finder.weights_path, # type: ignore
                                    scaler=finder.scaler_path,
                                    device=DEVICE)
    
    # update
    chain_orchestrator.update_with_inference(handler=handler)
    # return new schema
    new_schema = derive_next_step_schema(current_schema=previous_schema, handler=handler)
    return new_schema
```

## Step 1 - Tensile Strength

```python
feature_schema_1 = FeatureSchema.from_json(PM.engineering_artifacts)
```

```python
df_1 = chain_orchestrator.get_training_data(target_subset=[TENSILE_STRENGTH])
```

```python
summarize_dataframe(df_1)
```

Save training dataset validated with schema

```python
save_dataframe_with_schema(df=df_1, full_path=PM.chain_tensile_file, schema=feature_schema_1)
```

## Step 2 - Flexural Strength


Update chain orchestrator

```python
feature_schema_2 = update_chain_orchestrator(artifacts_directory=PM.chain_tensile, model_class=DragonNodeModel, previous_schema=feature_schema_1)
```

Get new training dataset

```python
df_2 = chain_orchestrator.get_training_data(target_subset=[FLEXURAL_STRENGTH])
```

```python
summarize_dataframe(df_2)
```

Save training dataset validated with schema

```python
feature_schema_2.to_json(PM.chain_artifacts2)
feature_schema_2.save_artifacts(PM.chain_artifacts2)
```

```python
save_dataframe_with_schema(df=df_2, full_path=PM.chain_flexural_file, schema=feature_schema_2)
```
