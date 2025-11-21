"""
SQLite Database Viewer
Simple tool to view and query the hospital.db database
"""

import sqlite3
import pandas as pd

def view_database():
    """View all tables and their contents"""
    
    print("=" * 80)
    print(" " * 25 + "HOSPITAL DATABASE VIEWER")
    print("=" * 80)
    
    try:
        # Connect to database
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n📊 Found {len(tables)} tables in database:")
        for i, table in enumerate(tables, 1):
            print(f"  {i}. {table[0]}")
        
        print("\n" + "=" * 80)
        
        # Display each table
        for table in tables:
            table_name = table[0]
            print(f"\n📋 TABLE: {table_name}")
            print("-" * 80)
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            schema = cursor.fetchall()
            
            print("\nColumns:")
            for col in schema:
                col_id, col_name, col_type, not_null, default, pk = col
                pk_marker = " (PRIMARY KEY)" if pk else ""
                print(f"  - {col_name} ({col_type}){pk_marker}")
            
            # Get table data
            try:
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                
                print(f"\nRecords: {len(df)}")
                if len(df) > 0:
                    print("\nData:")
                    print(df.to_string(index=False))
                else:
                    print("\n  (No records)")
                    
            except Exception as e:
                print(f"\n  Error reading table: {e}")
            
            print("\n" + "=" * 80)
        
        conn.close()
        
        print("\n✅ Database viewer completed!")
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except FileNotFoundError:
        print("❌ Database file 'hospital.db' not found!")
        print("   Run 'python database.py' to create it.")

def query_database(sql_query):
    """Execute a custom SQL query"""
    try:
        conn = sqlite3.connect('hospital.db')
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        
        print("\n📊 Query Results:")
        print("-" * 80)
        print(df.to_string(index=False))
        print(f"\n✅ Found {len(df)} rows")
        
        return df
    except Exception as e:
        print(f"❌ Query error: {e}")
        return None

def interactive_menu():
    """Interactive menu for database operations"""
    
    while True:
        print("\n" + "=" * 80)
        print(" " * 25 + "DATABASE VIEWER MENU")
        print("=" * 80)
        print("\n1. View All Tables")
        print("2. View Users Table")
        print("3. View Patients Table")
        print("4. View Logs Table")
        print("5. View GDPR Consent Table")
        print("6. Run Custom Query")
        print("7. Exit")
        print("\n" + "-" * 80)
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            view_database()
        
        elif choice == '2':
            print("\n📋 USERS TABLE:")
            print("-" * 80)
            query_database("SELECT user_id, username, role FROM users")
        
        elif choice == '3':
            print("\n📋 PATIENTS TABLE:")
            print("-" * 80)
            query_database("SELECT * FROM patients")
        
        elif choice == '4':
            print("\n📋 LOGS TABLE:")
            print("-" * 80)
            query_database("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 20")
        
        elif choice == '5':
            print("\n📋 GDPR CONSENT TABLE:")
            print("-" * 80)
            query_database("SELECT * FROM gdpr_consent")
        
        elif choice == '6':
            print("\n📝 Custom Query Mode")
            print("-" * 80)
            sql = input("Enter SQL query: ").strip()
            if sql:
                query_database(sql)
        
        elif choice == '7':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid choice. Please enter 1-7.")

if __name__ == "__main__":
    print("\n🏥 Hospital Management System - Database Viewer")
    
    # Check if database exists
    try:
        conn = sqlite3.connect('hospital.db')
        conn.close()
        interactive_menu()
    except:
        print("\n❌ Database 'hospital.db' not found!")
        print("   Please run 'python database.py' first to create the database.")
