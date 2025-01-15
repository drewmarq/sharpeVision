import requests
import pandas as pd
from datetime import datetime

#convert all company facts from SEC EDGAR .json to flat .csv file for specific CIK

def parse_sec_facts(cik):
    """
    Parse SEC XBRL facts into a properly flattened dataframe where each fact is a row
    with all its metadata as columns
    """
    # Format CIK to 10 digits
    cik_padded = str(cik).zfill(10)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_padded}.json"
    
    headers = {
        'User-Agent': 'Meow parker@protonmail.com',  
        'Accept': 'application/json'
    }
    
    try:
        # Fetch data
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Store all facts
        all_facts = []
        
        # Process each taxonomy and concept
        for taxonomy in data['facts']:
            for concept, concept_data in data['facts'][taxonomy].items():
                # Process each unit type
                for unit_type, facts in concept_data.get('units', {}).items():
                    # Process each individual fact
                    for fact in facts:
                        # Create a record for this fact
                        record = {
                            'taxonomy': taxonomy,
                            'concept': concept,
                            'unit': unit_type,
                            'start': fact.get('start', None),
                            'end': fact.get('end', None),
                            'val': fact.get('val'),
                            'accn': fact.get('accn'),
                            'fy': fact.get('fy'),
                            'fp': fact.get('fp'),
                            'form': fact.get('form'),
                            'filed': fact.get('filed'),
                            'frame': fact.get('frame', None)
                        }
                        
                        # Add any segment/dimension information if present
                        if 'dimensions' in fact:
                            for dim_key, dim_value in fact['dimensions'].items():
                                record[f'dimension_{dim_key}'] = dim_value
                        
                        all_facts.append(record)
        
        # Convert to DataFrame
        df = pd.DataFrame(all_facts)
        
        # Convert date fields
        date_fields = ['start', 'end', 'filed']
        for field in date_fields:
            if field in df.columns:
                df[field] = pd.to_datetime(df[field], errors='coerce')
        
        # Sort by filed date, taxonomy, and concept
        df = df.sort_values(['filed', 'taxonomy', 'concept'], ascending=[False, True, True])
        
        # Save to CSV with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f'sec_facts_CIK{cik_padded}_{timestamp}.csv'
        df.to_csv(output_filename, index=False)
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def process_companies(cik_list):
    """Process multiple CIKs and combine results"""
    all_dfs = []
    
    for cik in cik_list:
        print(f"Processing CIK: {cik}")
        df = parse_sec_facts(cik)
        if df is not None:
            # Add CIK to dataframe
            df['cik'] = cik
            all_dfs.append(df)
    
    if all_dfs:
        # Combine all dataframes
        combined_df = pd.concat(all_dfs, ignore_index=True)
        
        # Save combined results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f'sec_facts_combined_{timestamp}.csv'
        combined_df.to_csv(output_filename, index=False)
        
        return combined_df
    
    return None

if __name__ == "__main__":
    ciks = ["1326380"]  #example CIK
    df = process_companies(ciks)
    
    if df is not None:
        # Print some summary info
        print("\nDataset Summary:")
        print(f"Total facts: {len(df)}")
        print("\nUnique concepts:")
        concepts = df.groupby(['taxonomy', 'concept']).size().sort_values(ascending=False)
        print(concepts.head(10))
        print("\nForm types:")
        print(df['form'].value_counts())