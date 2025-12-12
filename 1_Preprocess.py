from helpers.function_map import TRANSFORMATION_RECIPE
from paths import PM
from ml_tools.ETL_engineering import DragonProcessor


def preprocess_data() -> None:
    """
    Preprocesses the data by applying transformations
    """ 
    # instantiate processor
    PROCESSOR = DragonProcessor(recipe=TRANSFORMATION_RECIPE)
    
    # Process df
    PROCESSOR.load_transform_save(input_path=PM.clean_data_file, output_path=PM.processed_data_file)

if __name__ == "__main__":
    preprocess_data()
