from ml_tools.VIF import compute_vif
from paths import PM
from helpers.constants import TARGETS_REGRESSION
from ml_tools.utilities import load_dataframe_greedy


if __name__ == "__main__":
    df = load_dataframe_greedy(directory=PM.mice_datasets)
    
    compute_vif(df=df,
                ignore_columns=TARGETS_REGRESSION,
                save_dir=PM.vif)
