import pandas as pd
import os

def clean_and_save_individual_sheets():
    base_path = "/home/ubuntu/upload"
    output_dir = "/home/ubuntu/cleaned_data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load all raw data first
    all_raw_data = {}
    for f in os.listdir(base_path):
        if f.endswith(".csv"):
            try:
                all_raw_data[f.replace(".csv", "")] = pd.read_csv(os.path.join(base_path, f))
                print(f"Loaded {f}")
            except Exception as e:
                print(f"Erro ao carregar {f}: {e}")

    # Process each sheet individually to avoid column conflicts
    for sheet_name, df in all_raw_data.items():
        try:
            # Basic cleaning: remove completely empty rows and columns
            df_cleaned = df.dropna(how='all').dropna(axis=1, how='all')
            
            # Try to find a reasonable header row (first row with at least 3 non-null values)
            header_row = 0
            for i in range(min(5, len(df_cleaned))):
                if df_cleaned.iloc[i].dropna().shape[0] >= 3:
                    header_row = i
                    break
            
            # Set header and clean
            if header_row > 0:
                df_cleaned.columns = df_cleaned.iloc[header_row]
                df_cleaned = df_cleaned[header_row+1:].reset_index(drop=True)
            
            # Ensure column names are unique
            cols = pd.Series(df_cleaned.columns)
            for dup in cols[cols.duplicated()].unique():
                # For duplicate columns, append a counter to make them unique
                count = 1
                for i, col_name in enumerate(cols):
                    if col_name == dup:
                        cols[i] = f"{dup}_{count}"
                        count += 1
            df_cleaned.columns = cols
            
            # Clean numeric columns (convert currency strings to numbers)
            for col in df_cleaned.columns:
                # Check if the column exists and is of object type (likely strings)
                if isinstance(df_cleaned[col], pd.Series) and df_cleaned[col].dtype == 'object':
                    # Try to convert currency-like strings to numbers
                    temp_series = df_cleaned[col].astype(str).str.replace('R$', '').str.replace('%', '').str.replace(',', '.').str.strip()
                    numeric_series = pd.to_numeric(temp_series, errors='coerce')
                    # If a significant portion of values are numeric after conversion, update the column
                    if numeric_series.notna().sum() / len(numeric_series) > 0.3:
                        df_cleaned[col] = numeric_series
            
            # Save cleaned data
            output_path = os.path.join(output_dir, f'{sheet_name}_cleaned.csv')
            df_cleaned.to_csv(output_path, index=False)
            print(f"Cleaned data saved to {output_path}")
            
        except Exception as e:
            print(f"Error processing {sheet_name}: {e}")
            # Save raw data as fallback if cleaning fails
            output_path = os.path.join(output_dir, f'{sheet_name}_raw.csv')
            df.to_csv(output_path, index=False)
            print(f"Raw data saved to {output_path}")

    # Generate a summary of all cleaned files
    summary_data = []
    for f in os.listdir(output_dir):
        if f.endswith(".csv"):
            try:
                df = pd.read_csv(os.path.join(output_dir, f))
                summary_data.append({
                    'File': f,
                    'Rows': df.shape[0],
                    'Columns': df.shape[1],
                    'Column_Names': ", ".join(df.columns.tolist()[:10])  # First 10 columns
                })
            except Exception as e:
                print(f"Error reading {f} for summary: {e}")
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(os.path.join(output_dir, 'data_summary.csv'), index=False)
    print("Data summary saved to cleaned_data/data_summary.csv")

if __name__ == '__main__':
    clean_and_save_individual_sheets()

