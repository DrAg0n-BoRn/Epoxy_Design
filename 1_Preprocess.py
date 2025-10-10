from helpers.function_map import TRANSFORMATION_RECIPE
from paths import PM
from ml_tools.ETL_engineering import DataProcessor


def preprocess_data() -> None:
    """
    Preprocesses the data by applying transformations
    """ 
    # instantiate processor
    PROCESSOR = DataProcessor(recipe=TRANSFORMATION_RECIPE)
    
    # Process df
    PROCESSOR.load_transform_save(input_path=PM["clean data"],
                                  output_path=PM["processed data"])

if __name__ == "__main__":
    PM.make_dirs()
    preprocess_data()
