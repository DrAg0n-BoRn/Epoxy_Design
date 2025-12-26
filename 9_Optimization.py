import torch
from ml_tools.ML_utilities import DragonArtifactFinder
from ml_tools.ML_models import DragonNodeModel, DragonGateModel, DragonTabularTransformer
from ml_tools.ML_inference import DragonInferenceHandler, DragonChainInference
from ml_tools.ML_optimization import DragonParetoOptimizer
from ml_tools.ML_configuration import DragonParetoConfig
from ml_tools.schema import FeatureSchema

from paths import PM
from helpers.constants import TARGET_tensile_strength, TARGET_flexural_strength, TARGET_elongation_at_break, TARGET_impact_strength


DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'


def make_inference(artifact_directory, model_class, device=DEVICE):
    finder = DragonArtifactFinder(directory=artifact_directory, load_scaler=True, load_schema=False, strict=True)
    
    model = model_class.load_architecture(finder.model_architecture_path)
    
    inference_handler = DragonInferenceHandler(model=model,
                                               state_dict=finder.weights_path, # type: ignore
                                               device=device,
                                               scaler=finder.scaler_path)
    
    return inference_handler


def make_optimizer_config():
    # define optimization directions for each target
    target_objectives = {TARGET_tensile_strength: 'max',
                         TARGET_flexural_strength: 'max',
                         TARGET_elongation_at_break: 'max',
                         TARGET_impact_strength: 'max'}
    
    optimizer_config = DragonParetoConfig(save_directory=PM.optimization_results,
                                          target_objectives=target_objectives, # type: ignore
                                          continuous_bounds_map=PM.optimization_results,
                                          population_size=500,
                                          generations=1000,
                                          float_precision=2)
    
    return optimizer_config


def main():
    # make inference handlers
    handler_node = make_inference(artifact_directory=PM.train_artifacts_1, model_class=DragonNodeModel)
    handler_gate = make_inference(artifact_directory=PM.train_artifacts_2, model_class=DragonGateModel)
    handler_tabtransform = make_inference(artifact_directory=PM.train_artifacts_3, model_class=DragonTabularTransformer)
    
    # make chain inference
    chain_inference = DragonChainInference(handlers=[handler_node, handler_gate, handler_tabtransform])
    
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
    
    # plots
    optimizer.plot_pareto_3d(x_target=TARGET_tensile_strength,
                             y_target=TARGET_flexural_strength,
                             z_target=TARGET_elongation_at_break)
    
    optimizer.plot_pareto_3d(x_target=TARGET_tensile_strength,
                             y_target=TARGET_flexural_strength,
                             z_target=TARGET_impact_strength)
    
    optimizer.plot_pareto_3d(x_target=TARGET_tensile_strength,
                             y_target=TARGET_elongation_at_break,
                             z_target=TARGET_impact_strength)
    
    optimizer.plot_pareto_3d(x_target=TARGET_flexural_strength,
                             y_target=TARGET_elongation_at_break,
                             z_target=TARGET_impact_strength)
    

if __name__ == '__main__':
    main()
