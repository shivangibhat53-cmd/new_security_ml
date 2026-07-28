import os 
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv('MONGODB_URI')
print(MONGO_DB_URL)

import certifi 
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkDataExtract():
    def __init__(self, database_name:str, collection_name :str):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.database = database_name
            self.collection = collection_name
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def cv_to_json_convertor(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop = True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def insert_data_mongodb(self,records,database_name = None, collection_name = None):
            try:
                target_db = database_name if database_name is not None else self.database
                target_col = collection_name if collection_name is not None else self.collection

                db = self.mongo_client[target_db]
                collection = db[target_col]
                collection.insert_many(records)
                return (len(records))
            except Exception as e:
                raise NetworkSecurityException(e,sys)


if __name__ == '__main__':
    FILE_PATH = r'network_data\phisingData.csv'
    DATABASE = 'shiv'
    COLLECTION = 'networkdata'
    networkobj = NetworkDataExtract(DATABASE,COLLECTION)
    records = networkobj.cv_to_json_convertor(FILE_PATH)
    no_of_records = networkobj.insert_data_mongodb(records)
    print(records)