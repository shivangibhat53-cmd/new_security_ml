from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig

import sys
if __name__ == '__main__':
    try:
        data_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(data_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info('Intiate the data ingestion')
        data_ingestion_artifact = data_ingestion.intiate_data_ingestion()
        print(data_ingestion_artifact)

    except Exception as e:
        raise NetworkSecurityException(e,sys)
