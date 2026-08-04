import subprocess
from networksecurity.exception.exception import NetworkSecurityException
import sys

class S3Sync:
    def sync_folder_to_s3(self, folder, aws_url_bucket):
        try:
            command = ['aws','s3','sync',folder,aws_url_bucket]
            subprocess.run(command, check= True)
        except subprocess.CalledProcessError as e:
            # Captures AWS CLI configuration or connectivity errors cleanly
            raise NetworkSecurityException(f"AWS S3 Sync failed: {e}", sys)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def sync_folder_from_s3(self, folder, aws_url_bucket):
        try:
            command = ['aws','s3','sync',aws_url_bucket,folder]
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            # Captures AWS CLI configuration or connectivity errors cleanly
            raise NetworkSecurityException(f"AWS S3 Sync failed: {e}", sys)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

        
