from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import (
            DataIngestionConfig,TrainingPipelineConfig,
            DataValidationConfig,DataTransformationConfig,
            ModelTrainerConfig)
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, ModelTrainerArtifact
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

        data_transformation_config =  DataTransformationConfig(data_pipeline_config)
        logging.info('Intiate data transformation')
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.intiate_data_transformation()
        logging.info('Data transformation completed')

        model_trainer_config = ModelTrainerConfig(data_pipeline_config)
        logging.info('Intiate Model Training')
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact= data_transformation_artifact)
        model_trainer_artifact = model_trainer.intiate_model_trainer()
        logging.info('Model Training completed')
        print(model_trainer_artifact)

    except Exception as e:
        raise NetworkSecurityException(e,sys)
