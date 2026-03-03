import torch
from ml_tools.ML_inference import DragonInferenceHandler
from ml_tools.ML_utilities import DragonArtifactFinder


DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'


def make_inference(artifact_directory, model_class):
    finder = DragonArtifactFinder(directory=artifact_directory, load_scaler=True, load_schema=False, strict=True)
    
    model = model_class.load_architecture(finder.model_architecture_path)
    
    inference_handler = DragonInferenceHandler(model=model,
                                               state_dict=finder.weights_path, # type: ignore
                                               device=DEVICE,
                                               scaler=finder.scaler_path)
    
    return inference_handler
