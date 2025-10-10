from ml_tools.utilities import train_dataset_orchestrator
from paths import PM
from helpers.constants import TARGETS


def main():
    train_dataset_orchestrator(list_of_dirs=[PM["mice datasets"]],
                            target_columns=TARGETS,
                            save_dir=PM["train datasets"])


if __name__ == "__main__":
    main()
