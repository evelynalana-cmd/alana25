import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("DATA") / "intelligence_platform.db"

def load_cyber_incidents():
    """Load cyber incidents from CSV."""
    csv_path = Path("DATA/cyber_incidents.csv")
    
    if not csv_path.exists():
        print(f"✗ File not found: {csv_path}")
        return 0
    
    conn = sqlite3.connect(str(DB_PATH))
    
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Rename columns to match database schema
    column_mapping = {
        'incident_id': 'id',
        'timestamp': 'date',
        'category': 'incident_type'
    }
    
    df = df.rename(columns=column_mapping)
    
    # Select only relevant columns
    columns_to_insert = ['date', 'incident_type', 'severity', 'status', 'description']
    df_to_insert = df[columns_to_insert]
    
    # Insert into database
    df_to_insert.to_sql('cyber_incidents', conn, if_exists='append', index=False)
    
    rows_inserted = len(df_to_insert)
    conn.close()
    
    print(f"✓ Loaded {rows_inserted} cyber incidents")
    return rows_inserted

def load_datasets_metadata():
    """Load datasets metadata from CSV."""
    csv_path = Path("DATA/datasets_metadata.csv")
    
    if not csv_path.exists():
        print(f"✗ File not found: {csv_path}")
        return 0
    
    conn = sqlite3.connect(str(DB_PATH))
    
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Rename columns to match database schema
    column_mapping = {
        'dataset_id': 'id',
        'name': 'dataset_name',
        'rows': 'row_count',
        'uploaded_by': 'department'
    }
    
    df = df.rename(columns=column_mapping)
    
    # Add missing columns
    if 'size_mb' not in df.columns:
        df['size_mb'] = df['row_count'] * 0.001  # Estimate
    
    if 'last_accessed' not in df.columns:
        df['last_accessed'] = None
    
    # Select only relevant columns
    columns_to_insert = ['dataset_name', 'department', 'size_mb', 'row_count', 'upload_date', 'last_accessed']
    df_to_insert = df[columns_to_insert]
    
    # Insert into database
    df_to_insert.to_sql('datasets_metadata', conn, if_exists='append', index=False)
    
    rows_inserted = len(df_to_insert)
    conn.close()
    
    print(f"✓ Loaded {rows_inserted} datasets")
    return rows_inserted

def load_it_tickets():
    """Load IT tickets from CSV."""
    csv_path = Path("DATA/it_tickets.csv")
    
    if not csv_path.exists():
        print(f"✗ File not found: {csv_path}")
        return 0
    
    conn = sqlite3.connect(str(DB_PATH))
    
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Rename columns to match database schema
    column_mapping = {
        'ticket_id': 'id',
        'description': 'title',
        'created_at': 'created_date'
    }
    
    df = df.rename(columns=column_mapping)
    
    # Add missing columns
    if 'resolved_date' not in df.columns:
        df['resolved_date'] = None
    
    # Select only relevant columns
    columns_to_insert = ['title', 'priority', 'status', 'assigned_to', 'created_date', 'resolved_date', 'resolution_time_hours']
    df_to_insert = df[columns_to_insert]
    
    # Insert into database
    df_to_insert.to_sql('it_tickets', conn, if_exists='append', index=False)
    
    rows_inserted = len(df_to_insert)
    conn.close()
    
    print(f"✓ Loaded {rows_inserted} IT tickets")
    return rows_inserted

def main():
    """Main data loading function."""
    print("\n" + "="*60)
    print(" WEEK 8 - STEP 5: LOADING CSV DATA")
    print("="*60)
    
    incidents = load_cyber_incidents()
    datasets = load_datasets_metadata()
    tickets = load_it_tickets()
    
    print("\n" + "="*60)
    print(" DATA LOADING COMPLETE")
    print("="*60)
    print(f"✓ Cyber incidents loaded: {incidents}")
    print(f"✓ Datasets loaded: {datasets}")
    print(f"✓ IT tickets loaded: {tickets}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()