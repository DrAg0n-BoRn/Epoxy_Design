from helpers.function_map import TRANSFORMATION_RECIPE
from paths import PM
from ml_tools.ETL_engineering import DataProcessor
from ml_tools.utilities import load_dataframe, save_dataframe


def preprocess_data() -> None:
    """
    Preprocesses the data by applying transformations
    """ 
    # instantiate processor
    PROCESSOR = DataProcessor(recipe=TRANSFORMATION_RECIPE)
    
    # load raw data csv
    df, _ = load_dataframe(df_path=PM["clean data"], kind="polars", all_strings=True)
    
    # Process df
    df_preprocessed = PROCESSOR.transform(df=df) # type: ignore
    
    # save_preprocessed csv
    save_dataframe(df=df_preprocessed, save_dir=PM["processed data"].parent, filename=PM["processed data"].name)


if __name__ == "__main__":
    PM.make_dirs()
    preprocess_data()
