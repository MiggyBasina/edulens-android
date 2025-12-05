import pandas as pd
import numpy as np

class MobileDataProcessor:
    def __init__(self):
        self.chunk_size = 10000
        
    def load_file_mobile(self, file_path, max_rows=5000):
        """Load CSV or Excel file with mobile memory limits"""
        try:
            # Check file extension
            file_ext = file_path.lower()
            
            if file_ext.endswith('.csv'):
                df = pd.read_csv(file_path, nrows=max_rows, low_memory=False)
                print(f"📁 Loading CSV: {file_path}")
                
            elif file_ext.endswith(('.xlsx', '.xls')):
                try:
                    # For Excel, load first sheet
                    df = pd.read_excel(file_path, nrows=max_rows)
                    print(f"📁 Loading Excel: {file_path}")
                except Exception as excel_error:
                    print(f"❌ Excel read error: {excel_error}")
                    # Try with engine specification
                    try:
                        df = pd.read_excel(file_path, nrows=max_rows, engine='openpyxl')
                    except:
                        try:
                            df = pd.read_excel(file_path, nrows=max_rows, engine='xlrd')
                        except:
                            return pd.DataFrame()
            
            else:
                print(f"❌ Unsupported file format: {file_path}")
                return pd.DataFrame()
            
            # Optimize and clean
            df = self.optimize_dataframe(df)
            df.columns = df.columns.astype(str).str.strip().str.lower().str.replace(' ', '_')
            
            print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except Exception as e:
            print(f"❌ Load error: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def optimize_dataframe(self, df):
        """Optimize dataframe memory usage"""
        if df.empty:
            return df
        
        # Convert object columns to category where appropriate
        for col in df.select_dtypes(include=['object']).columns:
            if df[col].nunique() / len(df) < 0.5:
                df[col] = df[col].astype('category')
        
        # Downcast numeric columns
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col] = pd.to_numeric(df[col], downcast='integer')
        
        print(f"   Optimized: {len(df.columns)} columns")
        return df
    
    def detect_data_type(self, df):
        """Detect type of educational data"""
        if df.empty:
            return 'general'
        
        columns = df.columns.str.lower().str.replace('_', '').str.replace(' ', '')
        
        # Check for educational data patterns
        edu_keywords = {
            'performance': ['grade', 'score', 'mark', 'gpa', 'result'],
            'attendance': ['attendance', 'present', 'absent', 'late'],
            'survey': ['survey', 'question', 'response', 'rating', 'scale'],
            'demographic': ['age', 'gender', 'ethnicity', 'background']
        }
        
        scores = {}
        for data_type, keywords in edu_keywords.items():
            score = 0
            for keyword in keywords:
                if any(keyword in col for col in columns):
                    score += 1
            scores[data_type] = score
        
        # Return highest scoring type
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return 'general'