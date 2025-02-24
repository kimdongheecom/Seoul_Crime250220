from dataclasses import dataclass

from flask import json
import googlemaps
import pandas as pd


@dataclass 
class DataReader:

    def __init__(self): #나중에 추가되는 엑셀때문에.,......init을 추가했다.
        self._context = 'C:\\Users\\bitcamp\\Documents\\kimdonghee250220\\com\\kimdonghee\\datas\\' 
        self._fname = ''
    
    @property
    def context(self) -> str:
        return self._context
    @context.setter
    def context(self,context):
        self._context = context
    @property
    def fname(self) -> str:
        return self._fname
    @fname.setter
    def fname(self,fname):
        self._fname = fname

    
    def new_file(self)->str:
        return self._context + self._fname

    def csv_to_dframe(self) -> object:
        file = self.new_file()
        return pd.read_csv(file, thousands=',')

    def xls_to_dframe(self, header, usecols)-> object:
        file = self.new_file()
        return pd.read_excel(file, header=header, usecols=usecols)

    def json_load(self):
        file = self.new_file()
        return json.load(open(file))
    
    @staticmethod
    def create_gmaps():
        return googlemaps.Client(key='...')

    # cctv : object 
    # crime : object
    # pop : object
 

    # @property 
    # def cctv(self) -> object:
    #     return self._cctv                         
    
    # @cctv.setter 
    # def cctv(self, cctv):
    #     self._cctv = cctv

    # @property 
    # def crime(self) -> object:
    #     return self._crime                        
    
    # @crime.setter 
    # def crime(self, crime):
    #     self._crime = crime
    
    # @property 
    # def pop(self) -> object:
    #     return self._pop                        
    
    # @pop.setter 
    # def pop(self, pop):
    #     self._pop = pop
    
    @property 
    def context(self) -> object:
        return self._context                        
    
    @context.setter 
    def context(self, context):
        self._context = context
    
    @property 
    def fname(self) -> object:
        return self._fname                        
    
    @fname.setter 
    def fname(self, fname):
        self._fname = fname
    
         