"""
Test script to verify automatic anonymization
"""

from database import DatabaseManager

print("=" * 60)
print("Testing Automatic Anonymization")
print("=" * 60)

# Initialize database
db = DatabaseManager()
print("\n✅ Database initialized")

# Test 1: Add a patient
print("\n[TEST 1] Adding a new patient...")
patient_id = db.add_patient(
    name="John Doe",
    contact="123-456-7890",
    diagnosis="Common Cold"
)

if patient_id:
    print(f"✅ Patient added with ID: {patient_id}")
    
    # Get the patient back
    patients = db.get_patients()
    new_patient = [p for p in patients if p['patient_id'] == patient_id][0]
    
    print("\n📋 Patient Data:")
    print(f"  Raw Name: {new_patient['name']}")
    print(f"  Raw Contact: {new_patient['contact']}")
    print(f"  Anonymized Name: {new_patient['anonymized_name']}")
    print(f"  Anonymized Contact: {new_patient['anonymized_contact']}")
    print(f"  Is Anonymized: {'Yes ✅' if new_patient['is_anonymized'] else 'No ❌'}")
    
    if new_patient['is_anonymized'] == 1:
        print("\n✅ TEST 1 PASSED: Patient automatically anonymized!")
    else:
        print("\n❌ TEST 1 FAILED: Patient not anonymized!")
else:
    print("❌ Failed to add patient")

# Test 2: Update a patient
print("\n" + "=" * 60)
print("[TEST 2] Updating patient...")
success = db.update_patient(
    patient_id=patient_id,
    name="Jane Smith",
    contact="555-123-4567"
)

if success:
    print("✅ Patient updated")
    
    # Get the updated patient
    patients = db.get_patients()
    updated_patient = [p for p in patients if p['patient_id'] == patient_id][0]
    
    print("\n📋 Updated Patient Data:")
    print(f"  Raw Name: {updated_patient['name']}")
    print(f"  Raw Contact: {updated_patient['contact']}")
    print(f"  Anonymized Name: {updated_patient['anonymized_name']}")
    print(f"  Anonymized Contact: {updated_patient['anonymized_contact']}")
    print(f"  Is Anonymized: {'Yes ✅' if updated_patient['is_anonymized'] else 'No ❌'}")
    
    if updated_patient['is_anonymized'] == 1:
        print("\n✅ TEST 2 PASSED: Patient re-anonymized after update!")
    else:
        print("\n❌ TEST 2 FAILED: Patient not re-anonymized!")
else:
    print("❌ Failed to update patient")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
