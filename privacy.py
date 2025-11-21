"""
Privacy and Security Module for Hospital Management System
Implements data anonymization, encryption, and masking (Confidentiality)
"""

import hashlib
from cryptography.fernet import Fernet
import base64
import os

class PrivacyManager:
    """Handles data anonymization, encryption, and masking"""
    
    def __init__(self):
        # Generate or load encryption key
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _get_or_create_key(self):
        """Get existing encryption key or create a new one"""
        key_file = 'encryption.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def hash_data(self, data):
        """Hash data using SHA-256 (irreversible)"""
        return hashlib.sha256(str(data).encode()).hexdigest()
    
    def encrypt_data(self, data):
        """Encrypt data using Fernet (reversible)"""
        try:
            if data is None:
                return None
            encrypted = self.cipher.encrypt(str(data).encode())
            return encrypted.decode()
        except Exception as e:
            print(f"Encryption error: {e}")
            return None
    
    def decrypt_data(self, encrypted_data):
        """Decrypt data using Fernet"""
        try:
            if encrypted_data is None:
                return None
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            return None
    
    def mask_name(self, name, patient_id):
        """Mask patient name with anonymous identifier"""
        return f"ANON_{patient_id:04d}"
    
    def mask_contact(self, contact):
        """Mask contact information, keeping last 4 digits"""
        if not contact or len(contact) < 4:
            return "XXX-XXX-XXXX"
        # Remove any non-digit characters
        digits = ''.join(filter(str.isdigit, contact))
        if len(digits) >= 4:
            return f"XXX-XXX-{digits[-4:]}"
        return "XXX-XXX-XXXX"
    
    def mask_diagnosis(self, diagnosis):
        """Mask diagnosis information"""
        if not diagnosis:
            return "CONFIDENTIAL"
        # Show only first word or category
        words = diagnosis.split()
        if len(words) > 0:
            return f"{words[0]}***"
        return "CONF***"
    
    def anonymize_patient_data(self, patient_data, patient_id):
        """Complete patient data anonymization"""
        anonymized = patient_data.copy()
        anonymized['name'] = self.mask_name(patient_data.get('name', ''), patient_id)
        anonymized['contact'] = self.mask_contact(patient_data.get('contact', ''))
        anonymized['diagnosis'] = self.mask_diagnosis(patient_data.get('diagnosis', ''))
        return anonymized
    
    def encrypt_sensitive_fields(self, patient_data):
        """Encrypt sensitive patient fields"""
        encrypted = patient_data.copy()
        if 'name' in encrypted:
            encrypted['name'] = self.encrypt_data(encrypted['name'])
        if 'contact' in encrypted:
            encrypted['contact'] = self.encrypt_data(encrypted['contact'])
        if 'diagnosis' in encrypted:
            encrypted['diagnosis'] = self.encrypt_data(encrypted['diagnosis'])
        return encrypted
    
    def decrypt_sensitive_fields(self, patient_data):
        """Decrypt sensitive patient fields"""
        decrypted = patient_data.copy()
        if 'name' in decrypted and decrypted['name']:
            decrypted['name'] = self.decrypt_data(decrypted['name'])
        if 'contact' in decrypted and decrypted['contact']:
            decrypted['contact'] = self.decrypt_data(decrypted['contact'])
        if 'diagnosis' in decrypted and decrypted['diagnosis']:
            decrypted['diagnosis'] = self.decrypt_data(decrypted['diagnosis'])
        return decrypted


class AccessControl:
    """Implements Role-Based Access Control (RBAC)"""
    
    # Define permissions for each role
    PERMISSIONS = {
        'admin': {
            'view_raw_data': True,
            'view_anonymized_data': True,
            'add_patient': True,
            'edit_patient': True,
            'delete_patient': True,
            'anonymize_data': True,
            'view_logs': True,
            'export_data': True,
            'manage_users': True
        },
        'doctor': {
            'view_raw_data': False,
            'view_anonymized_data': True,
            'add_patient': False,
            'edit_patient': False,
            'delete_patient': False,
            'anonymize_data': False,
            'view_logs': False,
            'export_data': True,
            'manage_users': False
        },
        'receptionist': {
            'view_raw_data': False,
            'view_anonymized_data': False,
            'add_patient': True,
            'edit_patient': True,
            'delete_patient': False,
            'anonymize_data': False,
            'view_logs': False,
            'export_data': False,
            'manage_users': False
        }
    }
    
    @staticmethod
    def has_permission(role, permission):
        """Check if a role has a specific permission"""
        if role not in AccessControl.PERMISSIONS:
            return False
        return AccessControl.PERMISSIONS[role].get(permission, False)
    
    @staticmethod
    def filter_patient_data(patient_data, role):
        """Filter patient data based on role permissions"""
        privacy_mgr = PrivacyManager()
        
        if role == 'admin':
            # Admin sees raw data
            return patient_data
        elif role == 'doctor':
            # Doctor sees anonymized data
            if patient_data.get('is_anonymized'):
                # Return anonymized version
                filtered = patient_data.copy()
                filtered['name'] = patient_data.get('anonymized_name', 'ANON_XXXX')
                filtered['contact'] = patient_data.get('anonymized_contact', 'XXX-XXX-XXXX')
                return filtered
            else:
                # Apply masking
                return privacy_mgr.anonymize_patient_data(patient_data, patient_data.get('patient_id', 0))
        elif role == 'receptionist':
            # Receptionist sees no sensitive data
            filtered = {
                'patient_id': patient_data.get('patient_id', ''),
                'name': '***CONFIDENTIAL***',
                'contact': '***CONFIDENTIAL***',
                'diagnosis': '***CONFIDENTIAL***',
                'date_added': patient_data.get('date_added', '')
            }
            return filtered
        
        return {}
    
    @staticmethod
    def get_allowed_actions(role):
        """Get list of allowed actions for a role"""
        actions = []
        if role in AccessControl.PERMISSIONS:
            perms = AccessControl.PERMISSIONS[role]
            for action, allowed in perms.items():
                if allowed:
                    actions.append(action)
        return actions


# Data validation functions (Integrity)
def validate_patient_data(name, contact, diagnosis):
    """Validate patient data before insertion"""
    errors = []
    
    if not name or len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters long")
    
    if not contact or len(contact.strip()) < 10:
        errors.append("Contact must be at least 10 characters long")
    
    if not diagnosis or len(diagnosis.strip()) < 3:
        errors.append("Diagnosis must be at least 3 characters long")
    
    return len(errors) == 0, errors


def sanitize_input(text):
    """Sanitize user input to prevent SQL injection"""
    if not text:
        return ""
    # Remove potentially dangerous characters
    dangerous_chars = [';', '--', '/*', '*/', 'xp_', 'sp_', 'DROP', 'DELETE', 'INSERT', 'UPDATE']
    sanitized = str(text)
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    return sanitized.strip()
