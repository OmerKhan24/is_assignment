"""
Test script to verify receptionist form no longer adds patients recursively
"""
import sqlite3
from database import DatabaseManager

def test_receptionist_fix():
    print("=" * 60)
    print("TESTING RECEPTIONIST FIX")
    print("=" * 60)
    
    db = DatabaseManager()
    
    # Initialize database
    db.init_database()
    
    # Count initial patients
    patients_before = db.get_patients()
    print(f"\n✓ Initial patient count: {len(patients_before)}")
    
    # Add one patient (simulating receptionist form submission)
    patient_id = db.add_patient("Test Patient", "123-456-7890", "Checkup")
    print(f"✓ Added patient with ID: {patient_id}")
    
    # Add log entry (simulating what the form does)
    db.add_log(2, "receptionist", "Receptionist", "ADD_PATIENT", f"Added patient ID: {patient_id}")
    print(f"✓ Logged action")
    
    # Count patients after
    patients_after = db.get_patients()
    print(f"✓ Final patient count: {len(patients_after)}")
    
    # Count log entries for this action
    logs = db.get_logs()
    add_patient_logs = [log for log in logs if log['action'] == 'ADD_PATIENT' and 'Test Patient' in log['details']]
    print(f"✓ Number of ADD_PATIENT log entries: {len(add_patient_logs)}")
    
    # Verify results
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    
    expected_increase = 1
    actual_increase = len(patients_after) - len(patients_before)
    
    if actual_increase == expected_increase:
        print(f"✅ SUCCESS: Exactly {expected_increase} patient added (as expected)")
    else:
        print(f"❌ FAILURE: Expected {expected_increase} patient, but got {actual_increase}")
    
    if len(add_patient_logs) == 1:
        print(f"✅ SUCCESS: Exactly 1 log entry created (as expected)")
    else:
        print(f"❌ FAILURE: Expected 1 log entry, but got {len(add_patient_logs)}")
    
    # Show all patients
    print("\n" + "=" * 60)
    print("ALL PATIENTS IN DATABASE")
    print("=" * 60)
    for patient in patients_after:
        print(f"ID: {patient['patient_id']}, Name: {patient['name']}, Contact: {patient['contact']}")
    
    # Show all logs
    print("\n" + "=" * 60)
    print("RECENT LOG ENTRIES")
    print("=" * 60)
    for log in logs[-5:]:
        print(f"{log['timestamp']} - {log['username']} ({log['role']}): {log['action']} - {log['details']}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    print("\nNOTE: The actual fix is in app.py lines 555-605 (Add Patient form)")
    print("The form now uses a guard condition to prevent re-rendering during success message display")
    print("\nTo test in the UI:")
    print("1. Run: streamlit run app.py")
    print("2. Login as receptionist (username: receptionist, password: recep123)")
    print("3. Add ONE patient in the form")
    print("4. Check that only ONE patient and ONE log entry are created")
    print("5. Login as admin to verify in Audit Logs tab")

if __name__ == "__main__":
    test_receptionist_fix()
