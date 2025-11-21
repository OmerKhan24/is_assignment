"""
Database migration script to add encryption columns
Run this once to update the existing database schema
"""

import sqlite3

def migrate_database():
    """Add encryption columns to existing patients table"""
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(patients)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print("Current columns:", columns)
        
        # Add encrypted columns if they don't exist
        if 'encrypted_name' not in columns:
            print("Adding encrypted_name column...")
            cursor.execute("ALTER TABLE patients ADD COLUMN encrypted_name TEXT")
            
        if 'encrypted_contact' not in columns:
            print("Adding encrypted_contact column...")
            cursor.execute("ALTER TABLE patients ADD COLUMN encrypted_contact TEXT")
            
        if 'encrypted_diagnosis' not in columns:
            print("Adding encrypted_diagnosis column...")
            cursor.execute("ALTER TABLE patients ADD COLUMN encrypted_diagnosis TEXT")
            
        if 'is_encrypted' not in columns:
            print("Adding is_encrypted column...")
            cursor.execute("ALTER TABLE patients ADD COLUMN is_encrypted INTEGER DEFAULT 0")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        print("New columns added: encrypted_name, encrypted_contact, encrypted_diagnosis, is_encrypted")
        
        # Show updated schema
        cursor.execute("PRAGMA table_info(patients)")
        columns = cursor.fetchall()
        print("\nUpdated table schema:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
    except sqlite3.Error as e:
        print(f"❌ Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE MIGRATION SCRIPT")
    print("=" * 60)
    migrate_database()
