
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import sys
import os
import numpy as np 
import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()
import certifi 
ca = certifi.where()
MONGO_DB_URL = os.getenv('MONGODB_URI')

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL,tlsCAFile=ca)
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            
            if '_id' in df.columns.to_list():
                df = df.drop(columns = ['_id'])

            df.replace({'na':np.nan}, inplace=True)
            logging.info('Data exported from the MongoDB')
            return df
        except Exception as e:
                    raise NetworkSecurityException(e,sys)

    def export_data_into_feature_store(self, dataframe : pd.DataFrame):
        try:
            logging.info('Intiated export data into feature store')
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            
            dir_path = os.path.dirname(feature_store_file_path)
            
            os.makedirs(dir_path,exist_ok = True)
            dataframe.to_csv(feature_store_file_path, index = False, header=True)
            logging.info('Raw data stored in Artifacts')
            return dataframe  
        except Exception as e:
                    raise NetworkSecurityException(e,sys)
                 
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info('Performed train test split on the dataframe')
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path,exist_ok=True)
            logging.info('Exporting train and test file path')

            train_set.to_csv(self.data_ingestion_config.training_file_path, index= False, header = True)

            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header = True)
            logging.info("Exported train and test file path")

        except Exception as e:
                    raise NetworkSecurityException(e,sys)
             

    def intiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path= self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
