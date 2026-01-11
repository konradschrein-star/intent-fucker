"""
CSV Processor
Handles CSV file parsing, validation, and output generation
"""

import pandas as pd
from typing import List, Dict, Tuple, Optional
from pathlib import Path
from config import REQUIRED_COLUMNS, OUTPUT_COLUMNS


class CSVProcessor:
    def __init__(self):
        self.input_data = None
        self.results = []
    
    def validate_csv(self, filepath: str) -> Tuple[bool, str]:
        """
        Validate CSV file has required columns
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            df = pd.read_csv(filepath)
            
            # Check if file is empty
            if df.empty:
                return (False, "CSV file is empty")
            
            # Check for required columns
            missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
            
            if missing_columns:
                return (False, f"Missing required columns: {', '.join(missing_columns)}")
            
            return (True, "Valid CSV")
            
        except pd.errors.EmptyDataError:
            return (False, "CSV file is empty")
        except pd.errors.ParserError:
            return (False, "Invalid CSV format")
        except Exception as e:
            return (False, f"Error reading CSV: {str(e)}")
    
    def load_csv(self, filepath: str) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """
        Load and validate CSV file
        
        Returns:
            Tuple of (success, message, dataframe)
        """
        is_valid, message = self.validate_csv(filepath)
        
        if not is_valid:
            return (False, message, None)
        
        try:
            df = pd.read_csv(filepath)
            self.input_data = df
            return (True, f"Loaded {len(df)} keywords", df)
        except Exception as e:
            return (False, f"Error loading CSV: {str(e)}", None)
    
    def parse_manual_input(self, text: str) -> pd.DataFrame:
        """
        Parse manually entered keywords
        Expected format: one keyword per line, or CSV-like with title,views,views_per_year
        """
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
        
        data = []
        for line in lines:
            # Check if line contains commas (CSV format)
            if ',' in line:
                parts = [p.strip() for p in line.split(',')]
                if len(parts) >= 3:
                    try:
                        data.append({
                            'title': parts[0],
                            'views': int(parts[1]) if parts[1].isdigit() else 0,
                            'views_per_year': float(parts[2]) if parts[2].replace('.', '').isdigit() else 0.0
                        })
                    except:
                        # If parsing fails, treat as simple keyword
                        data.append({
                            'title': parts[0],
                            'views': 0,
                            'views_per_year': 0.0
                        })
                else:
                    # Not enough parts, use first part as keyword
                    data.append({
                        'title': parts[0],
                        'views': 0,
                        'views_per_year': 0.0
                    })
            else:
                # Simple keyword without metadata
                data.append({
                    'title': line,
                    'views': 0,
                    'views_per_year': 0.0
                })
        
        self.input_data = pd.DataFrame(data)
        return self.input_data
    
    def get_keywords(self) -> List[Dict]:
        """
        Get keywords as list of dictionaries
        """
        if self.input_data is None:
            return []
        
        return self.input_data.to_dict('records')
    
    def add_result(self, keyword_data: Dict, classification_result: Dict):
        """
        Add a classification result
        """
        result = {
            'title': keyword_data['title'],
            'views': keyword_data['views'],
            'views_per_year': keyword_data['views_per_year'],
            'relevance_score': classification_result['relevance_score'],
            'relevance_accepted': classification_result['relevance_accepted'],
            'category': classification_result['category'],
            'category_confidence': classification_result['category_confidence'],
            'reason': classification_result['reason']
        }
        self.results.append(result)
    
    def export_results(self, output_dir: str) -> Tuple[str, str]:
        """
        Export results to two CSV files: accepted and rejected
        
        Returns:
            Tuple of (accepted_filepath, rejected_filepath)
        """
        if not self.results:
            raise ValueError("No results to export")
        
        df = pd.DataFrame(self.results)
        
        # Split into accepted and rejected
        accepted_df = df[df['relevance_accepted'] == True]
        rejected_df = df[df['relevance_accepted'] == False]
        
        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filenames with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        accepted_file = output_path / f"accepted_keywords_{timestamp}.csv"
        rejected_file = output_path / f"rejected_keywords_{timestamp}.csv"
        
        # Export to CSV
        accepted_df.to_csv(accepted_file, index=False)
        rejected_df.to_csv(rejected_file, index=False)
        
        return (str(accepted_file), str(rejected_file))
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the classification results
        """
        if not self.results:
            return {
                'total': 0,
                'accepted': 0,
                'rejected': 0,
                'acceptance_rate': 0.0
            }
        
        df = pd.DataFrame(self.results)
        total = len(df)
        accepted = len(df[df['relevance_accepted'] == True])
        rejected = total - accepted
        
        return {
            'total': total,
            'accepted': accepted,
            'rejected': rejected,
            'acceptance_rate': round((accepted / total * 100), 2) if total > 0 else 0.0,
            'category_breakdown': df['category'].value_counts().to_dict()
        }
    
    def reset(self):
        """Clear all data and results"""
        self.input_data = None
        self.results = []


# Test function
if __name__ == "__main__":
    processor = CSVProcessor()
    
    # Test manual input
    test_input = """ys origin walkthrough
ys 8 review
how to install ys"""
    
    df = processor.parse_manual_input(test_input)
    print(f"Parsed {len(df)} keywords:")
    print(df)
