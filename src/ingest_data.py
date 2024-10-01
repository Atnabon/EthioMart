import os
import pandas as pd
import zipfile
from abc import ABC, abstractmethod

class DataIngestor(ABC):
    @abstractmethod
    def ingest(self, file_path:str) -> pd.DataFrame:
        """Abstract method to ingest data from a given file."""
        pass


class ZipDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame:
        if not file_path.endswith(".zip"):
            raise ValueError("The provided file is not a .zip file")
        
        
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall("extracted_data")

       
        extracted_files = os.listdir("extracted_data")
        csv_files = [f for f in extracted_files if f.endswith(".csv")]

        if len(csv_files) == 0:
            raise FileNotFoundError("No csv file found in the extracted data.")
        if len(csv_files) > 1:
            raise ValueError("Multiple CSV files found. Please specify which one to use.") 

      
        csv_file_path = os.path.join("extracted_data", csv_files[0])
        df = pd.read_csv(csv_file_path)   
        return df    

class DataInestorFactory:
    @staticmethod
    def get_data_ingestor(file_extension:str) -> DataIngestor:
        if file_extension == ".zip":
            return ZipDataIngestor()
        else:
            raise ValueError(f"No ingestor available for: {file_extension}")

def main():
  
    file_path = "data/archive.zip"

   
    file_extension = os.path.splitext(file_path)[1]

   
    ingestor = DataInestorFactory.get_data_ingestor(file_extension)

    
    ingestor.ingest(file_path)

if __name__ == "__main__":
    main()