from ml_tools.MICE_imputation import run_mice_pipeline
from paths import PM
from helpers.constants import TARGETS
from ml_tools.utilities import deserialize_object


def main():
    binary_columns = deserialize_object(filepath=PM["binary columns"])
    
    run_mice_pipeline(df_path_or_dir=PM["feature engineering clip"],
                      target_columns=TARGETS,
                      save_datasets_dir=PM["mice datasets"],
                      save_metrics_dir=PM["mice metrics"],
                      binary_columns=binary_columns,
                      iterations=25)


if __name__ == "__main__":
    main()
