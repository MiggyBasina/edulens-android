import pandas as pd
import numpy as np
import google.generativeai as genai
from datetime import datetime
import json

class EducationalAnalyst:
    def __init__(self, supabase_client=None):
        self.supabase = supabase_client
        self.datasets_info = {}
        
        # Initialize Gemini with YOUR API key
        self.api_key = "AIzaSyAN_EoTAu8Vc7i4EtMN4ebgY0n_QsRFZWQ"
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.gemini_available = True
            print("✅ Gemini AI initialized successfully")
        except Exception as e:
            print(f"❌ Gemini initialization failed: {e}")
            self.model = None
            self.gemini_available = False
    
    def answer_question(self, question, datasets_dict, dataset_summaries=""):
        """Answer questions with FULL access to datasets"""
        if not self.gemini_available:
            return "AI service is not available. Please check your internet connection and API key."
        
        if not datasets_dict:
            return "I don't have access to any datasets yet. Please load some educational data first from the dashboard."
        
        try:
            print(f"🤖 Processing question: '{question}'")
            print(f"📊 Datasets available: {list(datasets_dict.keys())}")
            
            # Create detailed context from datasets
            context = self._create_detailed_context(datasets_dict)
            
            prompt = f"""You are an educational AI assistant for teachers and professors. 
            Your job is to help analyze educational datasets to improve teaching and student outcomes.

            ===== DATASETS YOU HAVE ACCESS TO =====
            {context}

            ===== TEACHER'S QUESTION =====
            "{question}"

            ===== HOW TO RESPOND =====
            1. REFER TO THE SPECIFIC DATA ABOVE when answering
            2. If the question is about the data, mention specific columns, values, or patterns
            3. Provide practical, actionable advice for teachers
            4. Keep your response concise but helpful
            5. If you need to make assumptions, state them clearly

            ===== YOUR RESPONSE =====
            """
            
            print("🤖 Sending to Gemini...")
            response = self.model.generate_content(prompt)
            print("✅ Got response from Gemini")
            
            return response.text.strip()
            
        except Exception as e:
            print(f"❌ Gemini query failed: {e}")
            import traceback
            traceback.print_exc()
            
            # Simple error message
            return f"I encountered an error while processing your question. Please try again or ask a simpler question. Error: {str(e)[:100]}"
    
    def _create_detailed_context(self, datasets_dict):
        """Create detailed context from datasets for Gemini"""
        if not datasets_dict:
            return "No datasets loaded."
        
        context_parts = []
        
        for name, df in datasets_dict.items():
            # Basic info
            dataset_info = f"📊 DATASET: '{name}'\n"
            dataset_info += f"   • Records: {len(df):,}\n"
            dataset_info += f"   • Columns: {len(df.columns)}\n"
            
            # Column details
            columns = list(df.columns)
            dataset_info += f"   • Column names:\n"
            for i, col in enumerate(columns[:12], 1):  # Show first 12 columns
                dtype = str(df[col].dtype)
                unique_vals = df[col].nunique()
                dataset_info += f"     {i}. {col} ({dtype}) - {unique_vals} unique values\n"
            
            if len(columns) > 12:
                dataset_info += f"     ... and {len(columns)-12} more columns\n"
            
            # Data type detection
            data_type = self._detect_edu_type(df)
            dataset_info += f"   • Data type: {data_type.replace('_', ' ').title()}\n"
            
            # Sample data (first 3 rows, first 5 columns)
            if len(df) > 0:
                sample = df.head(3)
                sample_cols = sample.columns[:5]  # First 5 columns
                
                dataset_info += f"   • Sample data (first 3 rows):\n"
                for idx, row in sample.iterrows():
                    row_data = []
                    for col in sample_cols:
                        value = row[col]
                        # Truncate long values
                        if isinstance(value, str) and len(value) > 30:
                            value = value[:27] + "..."
                        row_data.append(f"{col}: {value}")
                    
                    dataset_info += f"     Row {idx+1}: {', '.join(row_data)}\n"
            
            # Basic statistics for numeric columns
            numeric_cols = []
            for col in columns:
                try:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        numeric_cols.append(col)
                except:
                    pass
            
            if numeric_cols:
                dataset_info += f"   • Numeric columns: {', '.join(numeric_cols[:5])}\n"
                for col in numeric_cols[:3]:  # Stats for first 3 numeric columns
                    try:
                        avg = df[col].mean()
                        std = df[col].std()
                        dataset_info += f"   • {col}: avg={avg:.2f}, std={std:.2f}\n"
                    except:
                        pass
            
            context_parts.append(dataset_info)
        
        return "\n" + "\n".join(context_parts) + "\n"
    
    def generate_dashboard_insights(self, datasets_dict):
        """Generate practical insights for teachers"""
        if not datasets_dict:
            return "• No datasets loaded\n• Connect to cloud or upload data\n• Insights will appear here"
        
        try:
            if not self.gemini_available:
                return self._generate_simple_insights(datasets_dict)
            
            # Create simple context for insights
            context_parts = []
            for name, df in datasets_dict.items():
                info = f"'{name}': {len(df)} records, {len(df.columns)} columns"
                
                # Add column examples
                cols = list(df.columns)[:4]
                info += f", columns: {', '.join(cols)}"
                
                # Detect data type
                data_type = self._detect_edu_type(df)
                info += f", type: {data_type}"
                
                context_parts.append(info)
            
            context = "\n".join(context_parts)
            
            prompt = f"""You are an educational assistant helping teachers.

            AVAILABLE DATASETS:
            {context}

            TASK: Generate 3-4 bullet points of practical insights.
            Focus on: student performance patterns, engagement opportunities, teaching strategies.
            Keep each insight specific and actionable.

            FORMAT exactly like this (bullet points only):
            • [Insight 1 - specific to the data]
            • [Insight 2 - teaching recommendation]
            • [Insight 3 - student support suggestion]
            • [Insight 4 - data observation]

            Do not add explanations or extra text.
            """
            
            response = self.model.generate_content(prompt)
            insights = response.text.strip()
            
            # Clean up response
            lines = [line.strip() for line in insights.split('\n')]
            bullet_points = []
            for line in lines:
                if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                    bullet_points.append(f"• {line[1:].strip()}")
                elif line and not any(line.startswith(word) for word in ['ROLE', 'TASK', 'AVAILABLE', 'FORMAT']):
                    bullet_points.append(f"• {line}")
            
            # Limit to 4 bullet points
            return "\n".join(bullet_points[:4])
            
        except Exception as e:
            print(f"❌ Insight generation error: {e}")
            return self._generate_simple_insights(datasets_dict)
    
    def _generate_simple_insights(self, datasets_dict):
        """Generate simple insights when Gemini fails"""
        total_rows = sum(len(df) for df in datasets_dict.values())
        total_cols = sum(len(df.columns) for df in datasets_dict.values())
        
        return f"""• {len(datasets_dict)} datasets loaded
• {total_rows:,} total student records
• {total_cols} different metrics tracked
• Ask AI for detailed analysis"""
    
    def _detect_edu_type(self, df):
        """Detect type of educational data"""
        cols = ' '.join(df.columns).lower()
        
        if any(word in cols for word in ['grade', 'score', 'mark', 'gpa']):
            return 'student_performance'
        elif any(word in cols for word in ['attendance', 'present', 'absent']):
            return 'attendance'
        elif any(word in cols for word in ['survey', 'question', 'response']):
            return 'survey'
        elif any(word in cols for word in ['enrollment', 'admission', 'student']):
            return 'enrollment'
        else:
            return 'educational_data'