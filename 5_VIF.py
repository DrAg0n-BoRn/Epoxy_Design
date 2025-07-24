from ml_tools.VIF_factor import compute_vif_multi
from paths import PM
from helpers.constants import FINAL_TARGETS


def main():
    compute_vif_multi(input_directory=PM["mice datasets"],
                      output_plot_directory=PM["vif metrics"],
                      output_dataset_directory=PM["vif datasets"],
                      ignore_columns=FINAL_TARGETS,
                      max_features_to_plot=20)


if __name__ == "__main__":
    main()
