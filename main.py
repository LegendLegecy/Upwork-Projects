import os
import pandas as pd

# Input and output folders
input_folder = "input"
output_folder = "output"

# Function to process CSV files
def process_csv(file_path):
    while True:
        try:
            df = pd.read_csv(file_path)
            
            # Check if required columns exist
            required_columns = {'ordered', 'total-weight', 'delivery-phone', 'phone', 'actual-shipping-type'}
            if not required_columns.issubset(df.columns):
                missing_columns = required_columns - set(df.columns)
                print(f"Skipping file {file_path} due to missing columns: {missing_columns}")
                break
            
            # Process the file
            df['invoicenumber'] = 'RC' + df['ordered'].astype(str)  # Add "RC" before "ordered" data
            df = df.replace('-', '')  # Remove dashes from columns
            df['parcelno'] = (df['total-weight'] / 8.00).apply(lambda x: int(x) + (1 if x % 1 != 0 else 0))  # Calculate parcel number
            df['delivery-phone'] = df['delivery-phone'].replace('-', '').fillna(df['phone'])  # Duplicate data from "phone" to "delivery-phone" if "delivery-phone" is blank or contains "-"
            df['phone'] = df['phone'].astype(str).str.replace(' ', '').str.replace('+44', '').str.strip()  # Format phone numbers
            df['delivery-phone'] = df['delivery-phone'].astype(str).str.replace(' ', '').str.replace('+44', '').str.strip()  # Format phone numbers
            courier_mapping = {
                "FREE! DPD Tracked Delivery - Weekdays 7am-7pm": "PARCEL-ND",
                "Upgrade to DPD Pre-noon delivery - 8am – noon": "PARCEL-12PM",
                "Upgrade to DPD Pre-10:30am delivery - 8am-10:30am": "PARCEL-1030AM"
            }
            df['actual-shipping-type'] = df['actual-shipping-type'].map(courier_mapping)  # Replace actual-shipping-type with couriers product code

            # Write the processed data to a new CSV file
            output_file_path = os.path.join(output_folder, os.path.basename(file_path))
            df.to_csv(output_file_path, index=False)

            print(f"File processed: {file_path}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
        

# Process all CSV files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_folder, file_name)
        process_csv(file_path)
