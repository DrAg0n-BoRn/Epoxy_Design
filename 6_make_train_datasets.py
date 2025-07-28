from ml_tools.utilities import train_dataset_orchestrator
from paths import PM
from helpers.constants import FINAL_TARGETS


def main():
    dataset_dirs = [PM["feature engineering clip"], PM["mice datasets"]]

    train_dataset_orchestrator(list_of_dirs=dataset_dirs, # type: ignore
                            target_columns=FINAL_TARGETS,
                            save_dir=PM["model datasets"])


if __name__ == "__main__":
    main()
