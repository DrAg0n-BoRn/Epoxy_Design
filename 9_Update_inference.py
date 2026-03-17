from ml_tools.utilities import load_dataframe_greedy, save_dataframe
from ml_tools.ML_models import DragonAttentionMLP as CLASSIFICATION_MODEL
from ml_tools.schema import FeatureSchema
from ml_tools.keys import InferenceKeys

from paths import PM
from helpers.tools import make_inference
from helpers.constants import CURING, FILLER


def inference_helper(artifact_directory, features_array):
    inference_handler = make_inference(artifact_directory=artifact_directory, model_class=CLASSIFICATION_MODEL)
    
    results = inference_handler.predict_batch_numpy(features=features_array)
    predicted_labels = results[InferenceKeys.LABEL_NAMES]
    return predicted_labels


def main():
    df = load_dataframe_greedy(directory=PM.optimization)
    
    schema = FeatureSchema.from_json(PM.engineering_artifacts)
    
    df_features = df[list(schema.continuous_feature_names)]
    features_array = df_features.to_numpy()
    
    predicted_curing = inference_helper(artifact_directory=PM.classification_curing, features_array=features_array)
    predicted_filler = inference_helper(artifact_directory=PM.classification_filler, features_array=features_array)
    
    df[CURING] = predicted_curing
    df[FILLER] = predicted_filler
    
    save_dataframe(df=df, full_path=PM.final_data_file)
    

if __name__ == "__main__":
    main()
