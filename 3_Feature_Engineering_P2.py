from helpers.constants import CONTINUOUS_RANGE, TARGETS_RANGE, TARGETS
from ml_tools.utilities import save_dataframe, load_dataframe
from ml_tools.data_exploration import clip_outliers_multi, plot_value_distributions, split_features_targets, split_continuous_binary
from paths import PM


def main():
    # FILL RANGES IN ADVANCE
    clip_dict = CONTINUOUS_RANGE | TARGETS_RANGE
    
    df, _ = load_dataframe(df_path=PM["engineered data unclip"], kind="pandas")
    
    df_clip = clip_outliers_multi(df=df, clip_dict=clip_dict, verbose=True) # type: ignore
    
    # plot final value distributions
    df_features, df_targets = split_features_targets(df=df_clip, targets=TARGETS)
    df_continuous, df_binary = split_continuous_binary(df_features)
    
    plot_value_distributions(df=df_targets, save_dir=PM["feature engineering clip"])
    plot_value_distributions(df=df_continuous, save_dir=PM["feature engineering clip"])
    
    # save data
    save_dataframe(df=df_clip, save_dir=PM["engineered data clip"].parent, filename=PM["engineered data clip"].name)
        

if __name__ == "__main__":
    main()
