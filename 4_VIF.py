from ml_tools.VIF import compute_vif
from paths import PM
from helpers.constants import TARGET_elongation_at_break, TARGET_flexural_strength, TARGET_impact_strength, TARGET_tensile_strength
from ml_tools.utilities import load_dataframe_greedy


if __name__ == "__main__":
    df = load_dataframe_greedy(directory=PM.mice_datasets)
    
    compute_vif(df=df,
                ignore_columns=[TARGET_elongation_at_break, TARGET_flexural_strength, TARGET_impact_strength, TARGET_tensile_strength],
                save_dir=PM.vif)
