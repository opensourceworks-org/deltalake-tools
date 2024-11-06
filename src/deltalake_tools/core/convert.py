import logging
from deltalake import convert_to_deltalake
from deltalake_tools.models.models import S3ClientDetails
from deltalake_tools.result import Err, Ok, Result

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeltaConverter:
    def __init__(self, source_path: str, table_path: str = None):
        self.source_path = source_path
        self.table_path = table_path

    def convert_parquet_to_delta(self, 
            inplace: bool = False,
            storage_options: S3ClientDetails = None) -> Result[str, str]:
        

        if storage_options is not None:
            storage_options = storage_options.to_s3_config().unwrap()

        try:
            convert_to_deltalake(
                    self.source_path,
                    storage_options=storage_options,  
                )  
        except Exception as e:
            logger.error(f"Error converting Parquet to Delta: {str(e)}")
            return Err(f"Error converting Parquet to Delta: {str(e)}")

        return Ok("Parquet converted to Delta successfully")

        
def convert_parquet_to_delta(
    source_path: str,
    table_path: str = None,
    inplace: bool = False,
    storage_options: S3ClientDetails = None,
) -> Result[str, str]:
    converter = DeltaConverter(source_path, table_path)
    return converter.convert_parquet_to_delta(inplace, storage_options)
    
