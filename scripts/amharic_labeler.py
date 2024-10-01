import pandas as pd

class AmharicNERLabeler:

    def __init__(self):
        self.price_keywords = ['ዋጋ', 'ብር', 'ከ']
        self.location_list = [
            'አዲስ', 'የታይላንድ', 'ቦሌ', 'ቡልጋሪ', 
            'በረራ', 'ልደታ', 'ባልቻ', 'አአ'
        ]
        self.product_keywords = [
            'ምርት', 'ስቶቭ', 'ማንኪያ', 'የችበስመጥበሻ',
            'መጥበሻ', 'መጥበሻዎች', 'ምርቶች', 'ባትራ', 'ካርድ'
        ]

    def label_tokens(self, tokens):

        labels = []

        for i, token in enumerate(tokens):
            token_stripped = token.strip()  

         
            if token_stripped.endswith('ብር'):
                labels.append('I-PRICE')  
                continue
            
            
            if token_stripped == 'ዋጋ':
                labels.append('B-PRICE')  
                continue
            
          
            if token_stripped.isdigit():
                
                next_token = tokens[i + 1].strip() if i < len(tokens) - 1 else None
                if next_token == 'ብር':
                    labels.append('I-PRICE')  
                    continue

                prev_token = tokens[i - 1].strip() if i > 0 else None
                if prev_token == 'ዋጋ':
                    labels.append('I-PRICE')  
                    continue
                else:
                    labels.append('O')  
                    continue
            
         
            if token_stripped == 'ብር':
               
                prev_token = tokens[i - 1].strip() if i > 0 else None
                if prev_token and prev_token.isdigit():
                    labels.append('I-PRICE')  
                    continue
            
           
            if 'ዋጋ' in token_stripped and 'ብር' in token_stripped:
                labels.append('I-PRICE')  
                continue
            
          
            if 'ከ' in token_stripped and 'ብር' in token_stripped:
                labels.append('I-PRICE')  
                continue
            
        
            if 'ዋጋ' in token_stripped and any(char.isdigit() for char in token_stripped):
                labels.append('I-PRICE') 
                continue

            
            if token_stripped in self.location_list:
                labels.append('B-LOC')  
                continue
            
           
            if token_stripped in self.product_keywords:
                labels.append('B-PROD')  
                continue

           
            labels.append("O")  

        return list(zip(tokens, labels)) 

    def label_dataframe(self, df, token_column):
        df['Labeled'] = df[token_column].apply(self.label_tokens)
        return df
    
    def save_conll_format(self, labeled_data, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            for _, row in labeled_data.iterrows():
                for token, label in row['Labeled']:
                    f.write(f"{token} {label}\n")
                f.write("\n") 