from ml_tools.MICE import DragonMICE
from ml_tools.schema import FeatureSchema
from paths import PM


if __name__ == "__main__":
    schema = FeatureSchema.from_json(PM.engineering_artifacts)
    
    mice_imputer = DragonMICE(schema=schema,
                              impute_targets=False)
    
    mice_imputer.run_pipeline(df_path_or_dir=PM.engineered_data_file,
                              save_datasets_dir=PM.mice_datasets,
                              save_metrics_dir=PM.mice_metrics)
