import re
import numpy as np
import pandas as pd

class AmharicTextPreprocessor:
    def __init__(self):
        self.allowed_characters = re.compile(r'[^ሀ-ፐ0-9\s/]')  
       

    def normalize_text(self, text):
        if not isinstance(text, str) or not text.strip():
            return np.nan

        
        text = re.sub(self.allowed_characters, '', text) 
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def preprocess(self, text):
        normalized_text = self.normalize_text(text)
        return normalized_text if normalized_text and normalized_text != '' else np.nan

    def preprocess_dataframe(self, df, text_column):
        df['preprocessed_message'] = df[text_column].apply(self.preprocess)
        return df