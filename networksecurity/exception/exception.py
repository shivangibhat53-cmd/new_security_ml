import sys
from networksecurity.logging import logger
from types import ModuleType
class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:ModuleType):
        #super().__init__(error_message)
        self.error_message = error_message
        _,_,exec_tb = error_details.exc_info()

        self.filename = exec_tb.tb_frame.f_code.co_filename
        self.lineno = exec_tb.tb_lineno

    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.filename,self.lineno,str(self.error_message)
        )
