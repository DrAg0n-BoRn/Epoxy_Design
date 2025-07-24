from helpers.constants import CONTINUOUS_RANGE, TARGETS_RANGE
from ml_tools.utilities import save_dataframe, yield_dataframes_from_dir
from ml_tools.data_exploration import clip_outliers_multi, plot_value_distributions
from paths import PM


def main():
    # FILL RANGES IN ADVANCE
    clip_dict = CONTINUOUS_RANGE | TARGETS_RANGE

    for df, df_name in yield_dataframes_from_dir(datasets_dir=PM["feature engineering unclip"]):
        # clip values
        df_clip = clip_outliers_multi(df=df, clip_dict=clip_dict, verbose=True)
        # plot final value distributions
        plot_value_distributions(df=df_clip, save_dir=PM["feature engineering clip"])
        # save data
        save_dataframe(df=df_clip, save_dir=PM["feature engineering clip"], filename=df_name + "_clip")
        

if __name__ == "__main__":
    main()
