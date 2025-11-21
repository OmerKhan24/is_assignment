"""
Database initialization and management module for Hospital Management System
Implements secure database operations with proper schema design
"""

import sqlite3
import hashlib
from datetime import datetime
import os

class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_name='hospital.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Create and return a database connection"""
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('admin', 'doctor', 'receptionist'))
                )
            ''')
            
            # Create patients table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    diagnosis TEXT NOT NULL,
                    anonymized_name TEXT,
                    anonymized_contact TEXT,
                    encrypted_name TEXT,
                    encrypted_contact TEXT,
                    encrypted_diagnosis TEXT,
                    date_added TEXT NOT NULL,
                    is_anonymized INTEGER DEFAULT 0,
                    is_encrypted INTEGER DEFAULT 0
                )
            ''')
            
            # Create logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT,
                    role TEXT,
                    action TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    details TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Create GDPR consent table (bonus feature)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS gdpr_consent (
                    consent_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER,
                    consent_given INTEGER DEFAULT 0,
                    consent_date TEXT,
                    data_retention_days INTEGER DEFAULT 365,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            ''')
            
            conn.commit()
            
            # Insert default users if not exist
            self._insert_default_users(cursor)
            
            conn.commit()
            print("Database initialized successfully!")
            
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def _insert_default_users(self, cursor):
        """Insert default users for the system"""
        default_users = [
            ('admin', 'admin123', 'admin'),
            ('Dr.Bob', 'doc123', 'doctor'),
            ('Alice_recep', 'rec123', 'receptionist')
        ]
        
        for username, password, role in default_users:
            try:
                # Hash password for security
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute('''
                    INSERT OR IGNORE INTO users (username, password, role)
                    VALUES (?, ?, ?)
                ''', (username, hashed_password, role))
            except sqlite3.IntegrityError:
                pass  # User already exists
    
    def verify_user(self, username, password):
        """Verify user credentials and return user data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute('''
                SELECT user_id, username, role 
                FROM users 
                WHERE username = ? AND password = ?
            ''', (username, hashed_password))
            
            user = cursor.fetchone()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Error verifying user: {e}")
            return None
        finally:
            conn.close()
    
    def add_log(self, user_id, username, role, action, details=""):
        """Add an activity log entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO logs (user_id, username, role, action, timestamp, details)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, username, role, action, timestamp, details))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding log: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def get_logs(self):
        """Retrieve all logs (Admin only)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT log_id, user_id, username, role, action, timestamp, details
                FROM logs
                ORDER BY timestamp DESC
            ''')
            logs = cursor.fetchall()
            return [dict(log) for log in logs]
        except sqlite3.Error as e:
            print(f"Error retrieving logs: {e}")
            return []
        finally:
            conn.close()
    
    def add_patient(self, name, contact, diagnosis):
        """Add a new patient record (NOT anonymized by default)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Insert patient with raw data, NOT anonymized yet
            cursor.execute('''
                INSERT INTO patients (name, contact, diagnosis, date_added, is_anonymized)
                VALUES (?, ?, ?, ?, 0)
            ''', (name, contact, diagnosis, date_added))
            conn.commit()
            patient_id = cursor.lastrowid
            
            # Add GDPR consent entry
            cursor.execute('''
                INSERT INTO gdpr_consent (patient_id, consent_given, consent_date, data_retention_days)
                VALUES (?, 1, ?, 365)
            ''', (patient_id, date_added))
            conn.commit()
            
            return patient_id
        except sqlite3.Error as e:
            print(f"Error adding patient: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def get_patients(self, anonymized=False):
        """Retrieve patient records"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT patient_id, name, contact, diagnosis, 
                       anonymized_name, anonymized_contact, 
                       encrypted_name, encrypted_contact, encrypted_diagnosis,
                       date_added, is_anonymized, is_encrypted
                FROM patients
                ORDER BY patient_id DESC
            ''')
            patients = cursor.fetchall()
            return [dict(patient) for patient in patients]
        except sqlite3.Error as e:
            print(f"Error retrieving patients: {e}")
            return []
        finally:
            conn.close()
            
            
    def get_patients_doc(self, anonymized=False):
        """Retrieve patient records"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT patient_id,  
                       anonymized_name, anonymized_contact, diagnosis, date_added, is_anonymized
                FROM patients
                ORDER BY patient_id DESC
            ''')
            patients = cursor.fetchall()
            return [dict(patient) for patient in patients]
        except sqlite3.Error as e:
            print(f"Error retrieving patients: {e}")
            return []
        finally:
            conn.close()        
            
            
    
    def update_patient(self, patient_id, name=None, contact=None, diagnosis=None):
        """Update patient information (anonymization status reset)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            updates = []
            params = []
            
            if name:
                updates.append("name = ?")
                params.append(name)
            if contact:
                updates.append("contact = ?")
                params.append(contact)
            if diagnosis:
                updates.append("diagnosis = ?")
                params.append(diagnosis)
            
            if updates:
                # Reset anonymization when data is updated
                updates.append("is_anonymized = 0")
                updates.append("anonymized_name = NULL")
                updates.append("anonymized_contact = NULL")
                
                params.append(patient_id)
                query = f"UPDATE patients SET {', '.join(updates)} WHERE patient_id = ?"
                cursor.execute(query, params)
                conn.commit()
                return True
            return False
        except sqlite3.Error as e:
            print(f"Error updating patient: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def anonymize_patients(self):
        """Anonymize all patient records"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT patient_id, name, contact FROM patients WHERE is_anonymized = 0")
            patients = cursor.fetchall()
            
            for patient in patients:
                patient_id = patient['patient_id']
                # Create anonymized identifiers
                anon_name = f"ANON_{patient_id:04d}"
                # Mask contact: keep last 4 digits
                contact = patient['contact']
                anon_contact = f"XXX-XXX-{contact[-4:]}" if len(contact) >= 4 else "XXX-XXX-XXXX"
                
                cursor.execute('''
                    UPDATE patients 
                    SET anonymized_name = ?, anonymized_contact = ?, is_anonymized = 1
                    WHERE patient_id = ?
                ''', (anon_name, anon_contact, patient_id))
            
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error anonymizing patients: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def update_patient_anonymization(self, patient_id, anonymized_name, anonymized_contact):
        """Update patient anonymization fields (for encryption display)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE patients 
                SET anonymized_name = ?, anonymized_contact = ?, is_anonymized = 1
                WHERE patient_id = ?
            ''', (anonymized_name, anonymized_contact, patient_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating anonymization: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def encrypt_patient(self, patient_id, encrypted_name, encrypted_contact, encrypted_diagnosis):
        """Store encrypted patient data in database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE patients 
                SET encrypted_name = ?, 
                    encrypted_contact = ?, 
                    encrypted_diagnosis = ?,
                    anonymized_name = '🔐 ENCRYPTED',
                    anonymized_contact = '🔐 ENCRYPTED',
                    is_encrypted = 1,
                    is_anonymized = 1
                WHERE patient_id = ?
            ''', (encrypted_name, encrypted_contact, encrypted_diagnosis, patient_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error encrypting patient: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_encrypted_data(self, patient_id):
        """Retrieve encrypted data for a patient"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT encrypted_name, encrypted_contact, encrypted_diagnosis
                FROM patients
                WHERE patient_id = ? AND is_encrypted = 1
            ''', (patient_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error as e:
            print(f"Error retrieving encrypted data: {e}")
            return None
        finally:
            conn.close()
    
    def delete_patient(self, patient_id):
        """Delete a patient record (GDPR right to be forgotten)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Delete consent record first
            cursor.execute("DELETE FROM gdpr_consent WHERE patient_id = ?", (patient_id,))
            # Delete patient record
            cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting patient: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def cleanup_expired_data(self):
        """Delete patient records that have exceeded their retention period (GDPR compliance)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Find patients whose retention period has expired
            cursor.execute('''
                SELECT p.patient_id, p.name, p.date_added, c.data_retention_days
                FROM patients p
                LEFT JOIN gdpr_consent c ON p.patient_id = c.patient_id
                WHERE julianday('now') - julianday(p.date_added) > COALESCE(c.data_retention_days, 365)
            ''')
            
            expired_patients = cursor.fetchall()
            deleted_count = 0
            
            for patient in expired_patients:
                # Delete consent record
                cursor.execute("DELETE FROM gdpr_consent WHERE patient_id = ?", (patient['patient_id'],))
                # Delete patient record
                cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient['patient_id'],))
                deleted_count += 1
            
            conn.commit()
            return deleted_count, [dict(p) for p in expired_patients]
        except sqlite3.Error as e:
            print(f"Error cleaning up expired data: {e}")
            conn.rollback()
            return 0, []
        finally:
            conn.close()
    
    def get_expiring_patients(self, days_threshold=30):
        """Get patients that will expire within the specified number of days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT p.patient_id, p.name, p.date_added, 
                       COALESCE(c.data_retention_days, 365) as retention_days,
                       CAST((julianday('now') - julianday(p.date_added)) AS INTEGER) as days_stored,
                       CAST((COALESCE(c.data_retention_days, 365) - (julianday('now') - julianday(p.date_added))) AS INTEGER) as days_until_expiry
                FROM patients p
                LEFT JOIN gdpr_consent c ON p.patient_id = c.patient_id
                WHERE (COALESCE(c.data_retention_days, 365) - (julianday('now') - julianday(p.date_added))) <= ?
                  AND (COALESCE(c.data_retention_days, 365) - (julianday('now') - julianday(p.date_added))) > 0
                ORDER BY days_until_expiry ASC
            ''', (days_threshold,))
            
            expiring = cursor.fetchall()
            return [dict(p) for p in expiring]
        except sqlite3.Error as e:
            print(f"Error getting expiring patients: {e}")
            return []
        finally:
            conn.close()

# Initialize database when module is imported
if __name__ == "__main__":
    db = DatabaseManager()
    print("Database setup complete!")
