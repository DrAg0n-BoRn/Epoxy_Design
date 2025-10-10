from ml_tools.VIF_factor import compute_vif_multi
from paths import PM
from ml_tools.utilities import deserialize_object


def main():
    continuous_features = deserialize_object(filepath=PM["continuous columns"])
        
    compute_vif_multi(input_directory = PM["mice datasets"],
                      output_plot_directory = PM["vif metrics"],
                      output_dataset_directory = PM["vif datasets"],
                      use_columns = continuous_features)


if __name__ == "__main__":
    main()
