from app.data.incidents import get_all_incidents, get_incidents_by_type
from app.data.datasets import get_all_datasets, get_datasets_by_department
from app.data.tickets import get_all_tickets, get_tickets_by_status

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def test_incidents():
    """Test incident operations."""
    print_header("CYBER INCIDENTS")
    
    # Get all incidents
    df = get_all_incidents()
    print(f"\nTotal incidents in database: {len(df)}")
    print("\nFirst 5 incidents:")
    print(df.head()[['date', 'incident_type', 'severity', 'status']])
    
    # Filter by type
    print("\n--- Phishing Incidents ---")
    df_phishing = get_incidents_by_type('Phishing')
    print(f"Total Phishing incidents: {len(df_phishing)}")
    
    # Status distribution
    print("\n--- Incident Status Distribution ---")
    print(df['status'].value_counts())

def test_datasets():
    """Test dataset operations."""
    print_header("DATASETS METADATA")
    
    # Get all datasets
    df = get_all_datasets()
    print(f"\nTotal datasets in database: {len(df)}")
    print("\nAll datasets:")
    print(df[['dataset_name', 'department', 'size_mb', 'row_count']])
    
    # Get unique departments
    departments = df['department'].unique()
    print(f"\nDepartments: {', '.join(departments)}")

def test_tickets():
    """Test ticket operations."""
    print_header("IT TICKETS")
    
    # Get all tickets
    df = get_all_tickets()
    print(f"\nTotal tickets in database: {len(df)}")
    print("\nFirst 5 tickets:")
    print(df.head()[['id', 'title', 'priority', 'status', 'assigned_to']])
    
    # Get open tickets
    df_open = get_tickets_by_status('Open')
    print(f"\n--- Open Tickets ---")
    print(f"Total open tickets: {len(df_open)}")
    
    # Priority distribution
    print("\n--- Ticket Priority Distribution ---")
    print(df['priority'].value_counts())
    
    # Average resolution time
    resolved = df[df['status'] == 'Resolved']
    if len(resolved) > 0:
        avg_time = resolved['resolution_time_hours'].mean()
        print(f"\n--- Average Resolution Time ---")
        print(f"Average: {avg_time:.2f} hours")

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print(" WEEK 8: DATABASE & CRUD OPERATIONS TEST")
    print(" Multi-Domain Intelligence Platform")
    print("="*60)
    
    test_incidents()
    test_datasets()
    test_tickets()
    
    print("\n" + "="*60)
    print(" ALL TESTS COMPLETE!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()