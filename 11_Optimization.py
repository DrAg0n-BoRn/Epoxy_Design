import torch
from ml_tools.ML_utilities import DragonArtifactFinder
from ml_tools.ML_models import DragonNodeModel, DragonGateModel, DragonTabularTransformer
from ml_tools.ML_inference import DragonInferenceHandler, DragonChainInference
from ml_tools.ML_optimization import DragonParetoOptimizer
from ml_tools.ML_configuration import DragonParetoConfig
from ml_tools.schema import FeatureSchema
from itertools import combinations

from paths import PM
from helpers.constants import TARGETS_REGRESSION


DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'


def make_inference(artifact_directory, model_class):
    finder = DragonArtifactFinder(directory=artifact_directory, load_scaler=True, load_schema=False, strict=True)
    
    model = model_class.load_architecture(finder.model_architecture_path)
    
    inference_handler = DragonInferenceHandler(model=model,
                                               state_dict=finder.weights_path, # type: ignore
                                               device=DEVICE,
                                               scaler=finder.scaler_path)
    
    return inference_handler


def make_optimizer_config():
    # define optimization directions for each target
    target_objectives = {target: 'max' for target in TARGETS_REGRESSION}
    
    optimizer_config = DragonParetoConfig(save_directory=PM.optimization_results,
                                          target_objectives=target_objectives, # type: ignore
                                          continuous_bounds_map=PM.engineering_artifacts,
                                          population_size=500,
                                          generations=1000,
                                          float_precision=2)
    
    return optimizer_config


def main():
    # make inference handlers
    handler_1 = make_inference(artifact_directory=PM.train_artifacts_1, model_class=DragonNodeModel)
    handler_2 = make_inference(artifact_directory=PM.train_artifacts_2, model_class=DragonGateModel)
    handler_3 = make_inference(artifact_directory=PM.train_artifacts_3, model_class=DragonTabularTransformer)
    
    # make chain inference
    chain_inference = DragonChainInference(handlers=[handler_1, 
                                                     handler_2, 
                                                     handler_3
                                                     ])
    
    # optimizer config
    optimizer_config = make_optimizer_config()
    
    # original schema
    feature_schema = FeatureSchema.from_json(PM.engineering_artifacts)
    
    # make optimizer
    optimizer = DragonParetoOptimizer(inference_handler=chain_inference,
                                      schema=feature_schema,
                                      config=optimizer_config)
    
    # run optimization
    optimizer.run()
    
    # save results
    optimizer.save_solutions()
    
    # 3D plots
    if len(TARGETS_REGRESSION) >= 3:
        # Generate plots for all combinations
        for combo in combinations(TARGETS_REGRESSION, 3):
            optimizer.plot_pareto_3d(x_target=combo[0],
                                     y_target=combo[1],
                                     z_target=combo[2])


if __name__ == '__main__':
    main()
