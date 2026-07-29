from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import sys
if __name__ == '__main__':
    try:
        data_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(data_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info('Intiate the data ingestion')
        data_ingestion_artifact = data_ingestion.intiate_data_ingestion()
        logging.info('Data Intiation completed')
        data_validation_config = DataValidationConfig(data_pipeline_config )
        logging.info('Intiate data validation')
        data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
        data_validation_artifact = data_validation.intiate_data_validation()
        logging.info('Data validation completed')

        print(data_validation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e,sys)
