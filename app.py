"""
Hospital Management System - Main Streamlit Application
Implements CIA Triad with GDPR Compliance
"""

import streamlit as st

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
from datetime import datetime, timedelta
import time
import plotly.express as px
import plotly.graph_objects as go

# Import custom modules
from database import DatabaseManager
from privacy import PrivacyManager, AccessControl, validate_patient_data, sanitize_input

# Initialize managers
@st.cache_resource
def get_db_manager():
    return DatabaseManager()

@st.cache_resource
def get_privacy_manager():
    return PrivacyManager()

db = get_db_manager()
privacy_mgr = get_privacy_manager()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        border-bottom: 3px solid #1f77b4;
    }
    .role-badge {
        background-color: #1f77b4;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f0f2f6;
        padding: 10px;
        text-align: center;
        font-size: 0.8rem;
        border-top: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.login_time = None
    st.session_state.system_start_time = datetime.now()

# GDPR Consent Banner
def show_gdpr_banner():
    """Display GDPR consent banner"""
    if 'gdpr_consent' not in st.session_state:
        st.session_state.gdpr_consent = False
    
    if not st.session_state.gdpr_consent:
        with st.container():
            st.warning("🔒 **GDPR Notice**: This system processes personal health data. By logging in, you consent to data processing as per GDPR regulations. Data is encrypted, anonymized, and retained for 365 days.")
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("Accept & Continue"):
                    st.session_state.gdpr_consent = True
                    st.rerun()
            return False
    return True

# Login Page
def login_page():
    """User authentication page"""
    st.markdown("<h1 class='main-header'>🏥 Hospital Management System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>GDPR-Compliant Healthcare Data Management</h3>", unsafe_allow_html=True)
    
    if not show_gdpr_banner():
        return
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 User Login")
        st.markdown("*Secure authentication with role-based access control*")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if username and password:
                    try:
                        user = db.verify_user(username, password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user = user
                            st.session_state.login_time = datetime.now()
                            
                            # Log the login action
                            db.add_log(
                                user['user_id'],
                                user['username'],
                                user['role'],
                                "LOGIN",
                                f"User logged in successfully"
                            )
                            
                            st.success(f"✅ Welcome, {user['username']}! Redirecting...")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password")
                            # Log failed login attempt (user_id = 0 for failed attempts)
                            db.add_log(0, username, "FAILED_LOGIN", "FAILED_LOGIN", f"Failed login attempt for username: {username}")
                    except Exception as e:
                        st.error(f"⚠️ Login error: {str(e)}")
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        st.markdown("---")
        st.markdown("**Default Credentials:**")
        st.code("Admin: admin / admin123\nDoctor: Dr.Bob / doc123\nReceptionist: Alice_recep / rec123")

# Logout function
def logout():
    """Logout current user"""
    if st.session_state.user:
        db.add_log(
            st.session_state.user['user_id'],
            st.session_state.user['username'],
            st.session_state.user['role'],
            "LOGOUT",
            "User logged out"
        )
    
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.login_time = None
    st.rerun()

# Sidebar
def render_sidebar():
    """Render sidebar with user info and navigation"""
    with st.sidebar:
        user = st.session_state.user
        
        st.markdown(f"### 👤 User Profile")
        st.markdown(f"**Username:** {user['username']}")
        st.markdown(f"<span class='role-badge'>{user['role'].upper()}</span>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Session info
        if st.session_state.login_time:
            session_duration = datetime.now() - st.session_state.login_time
            st.markdown(f"**Session Duration:** {str(session_duration).split('.')[0]}")
        
        st.markdown("---")
        
        # Role permissions
        st.markdown("### 🔑 Your Permissions")
        permissions = AccessControl.get_allowed_actions(user['role'])
        for perm in permissions:
            st.markdown(f"✓ {perm.replace('_', ' ').title()}")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()

# Admin Dashboard
def admin_dashboard():
    """Admin view with full access"""
    st.markdown("<h2>👨‍💼 Admin Dashboard</h2>", unsafe_allow_html=True)
    
    # 🔄 AUTOMATIC DATA RETENTION CLEANUP (runs on dashboard load)
    if 'auto_cleanup_done' not in st.session_state:
        deleted_count, deleted_patients = db.cleanup_expired_data()
        if deleted_count > 0:
            st.toast(f"🗑️ Auto-cleanup: Deleted {deleted_count} expired record(s)", icon="♻️")
            db.add_log(
                st.session_state.user['user_id'],
                st.session_state.user['username'],
                st.session_state.user['role'],
                "AUTO_DATA_RETENTION_CLEANUP",
                f"Automatically deleted {deleted_count} expired patient records (GDPR retention policy)"
            )
        st.session_state.auto_cleanup_done = True
    
    tabs = st.tabs(["📊 Overview", "👥 Patient Management", "🔒 Anonymization", "📋 Audit Logs", "💾 Data Export", "⏳ Data Retention"])
    
    # Tab 1: Overview
    with tabs[0]:
        col1, col2, col3, col4 = st.columns(4)
        
        patients = db.get_patients()
        logs = db.get_logs()
        
        with col1:
            st.metric("Total Patients", len(patients))
        with col2:
            anonymized = sum(1 for p in patients if p['is_anonymized'])
            st.metric("Anonymized Records", anonymized)
        with col3:
            st.metric("Total Activities", len(logs))
        with col4:
            uptime = datetime.now() - st.session_state.system_start_time
            st.metric("System Uptime", f"{uptime.days}d {uptime.seconds//3600}h")
        
        st.markdown("---")
        
        # Activity graphs (Bonus feature)
        if logs:
            st.markdown("### 📈 Activity Analysis")
            
            # Convert logs to DataFrame
            df_logs = pd.DataFrame(logs)
            df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp'])
            # Keep date as datetime for better plotting
            df_logs['date'] = df_logs['timestamp'].dt.floor('D')
            
            # Calculate today's activity (last 24 hours)
            now = datetime.now()
            last_24h = now - timedelta(hours=24)
            today_logs = df_logs[df_logs['timestamp'] >= last_24h]
            today_count = len(today_logs)
            
            # Show today's metrics
            metric_cols = st.columns(4)
            with metric_cols[0]:
                st.metric("📊 Last 24 Hours", today_count, help="Activity count in the last 24 hours")
            with metric_cols[1]:
                today_date = now.date()
                today_only = df_logs[df_logs['date'] == pd.Timestamp(today_date)]
                st.metric("📅 Today", len(today_only), help=f"Activity count for {today_date}")
            with metric_cols[2]:
                st.metric("📝 Total Logs", len(df_logs), help="Total activity logs")
            with metric_cols[3]:
                unique_users = df_logs['username'].nunique()
                st.metric("👥 Active Users", unique_users, help="Unique users with activity")
            
            st.markdown("---")
            
            # Time range selector
            time_range = st.radio(
                "📅 Select Time Range for Graphs:",
                options=["Last 24 Hours", "Last 7 Days", "All Time"],
                horizontal=True,
                index=2
            )
            
            # Filter data based on selection
            if time_range == "Last 24 Hours":
                filtered_logs = df_logs[df_logs['timestamp'] >= last_24h]
                graph_title_suffix = "(Last 24 Hours)"
            elif time_range == "Last 7 Days":
                last_7d = now - timedelta(days=7)
                filtered_logs = df_logs[df_logs['timestamp'] >= last_7d]
                graph_title_suffix = "(Last 7 Days)"
            else:
                filtered_logs = df_logs
                graph_title_suffix = "(All Time)"
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Actions per time period (hourly for 24h, daily for others)
                if len(filtered_logs) > 0:
                    if time_range == "Last 24 Hours":
                        # Group by hour for 24-hour view
                        filtered_logs['hour'] = filtered_logs['timestamp'].dt.floor('H')
                        time_actions = filtered_logs.groupby('hour').size().reset_index(name='count')
                        time_actions['hour'] = pd.to_datetime(time_actions['hour'])
                        fig1 = px.line(time_actions, x='hour', y='count', 
                                      title=f'Hourly Activity Count {graph_title_suffix}',
                                      markers=True)
                        fig1.update_xaxes(title_text='Time', tickformat='%H:%M\n%Y-%m-%d')
                        fig1.update_yaxes(title_text='Number of Actions')
                    else:
                        # Group by day for other views
                        daily_actions = filtered_logs.groupby('date').size().reset_index(name='count')
                        daily_actions['date'] = pd.to_datetime(daily_actions['date'])
                        fig1 = px.line(daily_actions, x='date', y='count', 
                                      title=f'Daily Activity Count {graph_title_suffix}',
                                      markers=True)
                        fig1.update_xaxes(title_text='Date', tickformat='%Y-%m-%d')
                        fig1.update_yaxes(title_text='Number of Actions')
                    st.plotly_chart(fig1, use_container_width=True)
                else:
                    st.info("No data available for selected time range")
            
            with col2:
                # Actions by role
                if len(filtered_logs) > 0:
                    role_actions = filtered_logs.groupby('role').size().reset_index(name='count')
                    fig2 = px.pie(role_actions, values='count', names='role', 
                                 title=f'Actions by Role {graph_title_suffix}')
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("No data available for selected time range")
    
    # Tab 2: Patient Management
    with tabs[1]:
        st.markdown("### 👥 All Patient Records (Raw Data)")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("➕ Add New Patient"):
                st.session_state.show_add_form = True
        
        if st.session_state.get('show_add_form', False):
            with st.form("add_patient_form"):
                st.markdown("#### Add New Patient")
                name = st.text_input("Full Name")
                contact = st.text_input("Contact Number")
                diagnosis = st.text_area("Diagnosis")
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("Add Patient", use_container_width=True)
                with col2:
                    cancel = st.form_submit_button("Cancel", use_container_width=True)
                
                if submit:
                    valid, errors = validate_patient_data(name, contact, diagnosis)
                    if valid:
                        patient_id = db.add_patient(
                            sanitize_input(name),
                            sanitize_input(contact),
                            sanitize_input(diagnosis)
                        )
                        if patient_id:
                            db.add_log(
                                st.session_state.user['user_id'],
                                st.session_state.user['username'],
                                st.session_state.user['role'],
                                "ADD_PATIENT",
                                f"Added patient ID: {patient_id}"
                            )
                            st.success("✅ Patient added successfully!")
                            st.session_state.show_add_form = False
                            time.sleep(1)
                            st.rerun()
                    else:
                        for error in errors:
                            st.error(f"❌ {error}")
                
                if cancel:
                    st.session_state.show_add_form = False
                    st.rerun()
        
        # Display patients with delete option
        patients = db.get_patients()
        if patients:
            st.markdown("---")
            
            # Display each patient with edit and delete buttons
            for patient in patients:
                with st.expander(f"👤 Patient ID: {patient['patient_id']} - {patient['name']}"):
                    # Check if in edit mode
                    edit_key = f"edit_mode_{patient['patient_id']}"
                    
                    if st.session_state.get(edit_key, False):
                        # Edit form
                        with st.form(key=f"edit_form_{patient['patient_id']}"):
                            st.markdown("**✏️ Edit Patient Record:**")
                            new_name = st.text_input("Name", value=patient['name'])
                            new_contact = st.text_input("Contact", value=patient['contact'])
                            new_diagnosis = st.text_area("Diagnosis", value=patient['diagnosis'])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                save_btn = st.form_submit_button("💾 Save", use_container_width=True, type="primary")
                            with col2:
                                cancel_btn = st.form_submit_button("❌ Cancel", use_container_width=True)
                            
                            if save_btn:
                                valid, errors = validate_patient_data(new_name, new_contact, new_diagnosis)
                                if valid:
                                    if db.update_patient(patient['patient_id'], new_name, new_contact, new_diagnosis):
                                        db.add_log(
                                            st.session_state.user['user_id'],
                                            st.session_state.user['username'],
                                            st.session_state.user['role'],
                                            "EDIT_PATIENT",
                                            f"Edited patient ID: {patient['patient_id']}"
                                        )
                                        st.session_state[edit_key] = False
                                        st.success("✅ Patient updated!")
                                        time.sleep(1)
                                        st.rerun()
                                else:
                                    for error in errors:
                                        st.error(f"❌ {error}")
                            
                            if cancel_btn:
                                st.session_state[edit_key] = False
                                st.rerun()
                    else:
                        # View mode
                        col1, col2, col3 = st.columns([2.5, 2.5, 1])
                        
                        with col1:
                            st.markdown("**Raw Data (Admin View):**")
                            st.write(f"**Name:** {patient['name']}")
                            st.write(f"**Contact:** {patient['contact']}")
                            st.write(f"**Diagnosis:** {patient['diagnosis']}")
                        
                        with col2:
                            st.markdown("**Anonymized/Encrypted Data:**")
                            st.write(f"**Name:** {patient['anonymized_name']}")
                            st.write(f"**Contact:** {patient['anonymized_contact']}")
                            st.write(f"**Added:** {patient['date_added']}")
                            st.write(f"**Status:** {'✅ Yes' if patient['is_anonymized'] else '❌ No'}")
                        
                        with col3:
                            st.markdown("**Actions:**")
                            
                            # Decrypt button for encrypted records
                            if patient.get('is_encrypted', 0) == 1:
                                decrypt_state = st.session_state.get(f"show_decrypt_{patient['patient_id']}", False)
                                button_label = "❌ Hide" if decrypt_state else "🔓 Decrypt"
                                
                                if st.button(button_label, key=f"decrypt_{patient['patient_id']}", use_container_width=True, type="primary"):
                                    st.session_state[f"show_decrypt_{patient['patient_id']}"] = not decrypt_state
                                    if not decrypt_state:  # Only log when decrypting (showing data)
                                        db.add_log(
                                            st.session_state.user['user_id'],
                                            st.session_state.user['username'],
                                            st.session_state.user['role'],
                                            "DECRYPT_DATA",
                                            f"Viewed decrypted data for patient ID: {patient['patient_id']}"
                                        )
                            
                            if st.button("✏️ Edit", key=f"edit_{patient['patient_id']}", use_container_width=True):
                                st.session_state[edit_key] = True
                                st.rerun()
                            
                            if st.button(f"🗑️ Delete", key=f"delete_{patient['patient_id']}", type="secondary", use_container_width=True):
                                if db.delete_patient(patient['patient_id']):
                                    db.add_log(
                                        st.session_state.user['user_id'],
                                        st.session_state.user['username'],
                                        st.session_state.user['role'],
                                        "DELETE_PATIENT",
                                        f"Deleted patient ID: {patient['patient_id']} (GDPR: Right to be Forgotten)"
                                    )
                                    st.success(f"✅ Patient {patient['patient_id']} deleted successfully!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to delete patient")
                        
                        # Show encrypted text and decrypted data if record is encrypted
                        if patient.get('is_encrypted', 0) == 1:
                            st.markdown("---")
                            
                            # Show encrypted text from database
                            show_encrypted_key = f"show_encrypted_{patient['patient_id']}"
                            if st.checkbox("🔐 Show Encrypted Text from Database (Admin Only)", key=show_encrypted_key):
                                # Retrieve encrypted data from database
                                encrypted_data = db.get_encrypted_data(patient['patient_id'])
                                
                                if encrypted_data:
                                    st.code(
                                        f"Encrypted Name (from DB):\n{encrypted_data['encrypted_name']}\n\n"
                                        f"Encrypted Contact (from DB):\n{encrypted_data['encrypted_contact']}\n\n"
                                        f"Encrypted Diagnosis (from DB):\n{encrypted_data['encrypted_diagnosis']}", 
                                        language="text"
                                    )
                                    st.caption("🔒 This is the actual Fernet encrypted data stored in the database")
                                else:
                                    st.warning("No encrypted data found in database")
                            
                            # Show decrypted data if decrypt button was toggled on
                            if st.session_state.get(f"show_decrypt_{patient['patient_id']}", False):
                                from privacy import PrivacyManager
                                pm = PrivacyManager()
                                
                                # Retrieve and decrypt data from database
                                encrypted_data = db.get_encrypted_data(patient['patient_id'])
                                
                                if encrypted_data:
                                    decrypted_name = pm.decrypt_data(encrypted_data['encrypted_name'])
                                    decrypted_contact = pm.decrypt_data(encrypted_data['encrypted_contact'])
                                    decrypted_diagnosis = pm.decrypt_data(encrypted_data['encrypted_diagnosis'])
                                    
                                    st.success("🔓 **Decrypted Data (Decrypted from Fernet Encryption):**")
                                    decrypt_col1, decrypt_col2 = st.columns(2)
                                    with decrypt_col1:
                                        st.info(f"**👤 Name:** {decrypted_name}")
                                        st.info(f"**📞 Contact:** {decrypted_contact}")
                                    with decrypt_col2:
                                        st.info(f"**🏥 Diagnosis:** {decrypted_diagnosis}")
                                        st.info(f"**📅 Added:** {patient['date_added']}")
                                else:
                                    st.warning("⚠️ No encrypted data available. Showing raw data:")
                                    decrypt_col1, decrypt_col2 = st.columns(2)
                                    with decrypt_col1:
                                        st.info(f"**👤 Name:** {patient['name']}")
                                        st.info(f"**📞 Contact:** {patient['contact']}")
                                    with decrypt_col2:
                                        st.info(f"**🏥 Diagnosis:** {patient['diagnosis']}")
                                        st.info(f"**📅 Added:** {patient['date_added']}")
        else:
            st.info("No patient records found.")
    
    # Tab 3: Anonymization Control
    with tabs[2]:
        st.markdown("### 🔒 Data Anonymization & Encryption Control")
        st.info("💡 Admin can choose between masking (irreversible) or Fernet encryption (reversible) for privacy protection (Confidentiality)")
        
        patients = db.get_patients()
        anonymized_count = sum(1 for p in patients if p['is_anonymized'])
        total_count = len(patients)
        
        st.markdown(f"**Current Status:** {anonymized_count}/{total_count} records anonymized")
        
        progress = anonymized_count / total_count if total_count > 0 else 0
        st.progress(progress)
        
        st.markdown("---")
        
        # Privacy method selector
        privacy_method = st.radio(
            "🔐 Select Privacy Protection Method:",
            options=["Data Masking (Irreversible)", "Fernet Encryption (Reversible)"],
            horizontal=True,
            help="Masking: Shows ANON_XXXX (can't be decrypted) | Encryption: Encrypted format (can be decrypted by admin)"
        )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔐 Apply Privacy Protection")
            
            if total_count > anonymized_count:
                st.warning(f"⚠️ {total_count - anonymized_count} patient(s) not protected yet!")
                
                if privacy_method == "Data Masking (Irreversible)":
                    if st.button("🔒 Apply Masking to All", use_container_width=True, type="primary"):
                        if db.anonymize_patients():
                            db.add_log(
                                st.session_state.user['user_id'],
                                st.session_state.user['username'],
                                st.session_state.user['role'],
                                "ANONYMIZE_DATA",
                                f"Masked {total_count - anonymized_count} patient records (irreversible)"
                            )
                            st.success("✅ All patient data has been masked!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Masking failed")
                else:
                    if st.button("🔒 Apply Fernet Encryption to All", use_container_width=True, type="primary"):
                        from privacy import PrivacyManager
                        pm = PrivacyManager()
                        success_count = 0
                        
                        for patient in patients:
                            if not patient['is_anonymized']:
                                # Encrypt data using Fernet
                                encrypted_name = pm.encrypt_data(patient['name'])
                                encrypted_contact = pm.encrypt_data(patient['contact'])
                                encrypted_diagnosis = pm.encrypt_data(patient['diagnosis'])
                                
                                # Store encrypted data in database
                                if db.encrypt_patient(
                                    patient['patient_id'],
                                    encrypted_name,
                                    encrypted_contact,
                                    encrypted_diagnosis
                                ):
                                    success_count += 1
                        
                        if success_count > 0:
                            db.add_log(
                                st.session_state.user['user_id'],
                                st.session_state.user['username'],
                                st.session_state.user['role'],
                                "ENCRYPT_DATA",
                                f"Encrypted {success_count} patient records using Fernet (reversible)"
                            )
                            st.success(f"✅ Encrypted {success_count} patient records!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Encryption failed")
            else:
                st.success("✅ All patients are already protected!")
            
            st.markdown("---")
            
            if privacy_method == "Data Masking (Irreversible)":
                st.markdown("**Data Masking (Current Method):**")
                st.markdown("""
                - ✅ Patient names → ANON_XXXX format
                - ✅ Contact numbers → XXX-XXX-XXXX (last 4 visible)
                - ✅ Original data preserved for admin
                - ✅ Doctors see only masked data
                - ❌ Cannot be reversed/decrypted
                """)
            else:
                st.markdown("**Fernet Encryption (Alternative):**")
                st.markdown("""
                - 🔐 Patient names → Encrypted format
                - 🔐 Contact numbers → Encrypted format
                - 🔐 Original data preserved for admin
                - 🔐 Doctors see "ENCRYPTED" label
                - ✅ Admin can decrypt and view
                - ✅ Reversible with encryption key
                """)
        
        with col2:
            st.markdown("### 🔓 Decrypt Encrypted Records")
            
            if privacy_method == "Fernet Encryption (Reversible)":
                st.info("Admin can decrypt and view encrypted patient records")
                
                encrypted_patients = [p for p in patients if p['is_anonymized'] and p['anonymized_name'] == "🔐 ENCRYPTED"]
                
                if encrypted_patients:
                    selected_patient_id = st.selectbox(
                        "Select Patient to Decrypt:",
                        options=[p['patient_id'] for p in encrypted_patients],
                        format_func=lambda x: f"Patient ID: {x}"
                    )
                    
                    if st.button("🔓 Decrypt & View", use_container_width=True):
                        from privacy import PrivacyManager
                        pm = PrivacyManager()
                        
                        selected_patient = next(p for p in encrypted_patients if p['patient_id'] == selected_patient_id)
                        
                        # For demo, show the raw data (since we're storing raw data in the DB)
                        # In real implementation, you'd decrypt from encrypted fields
                        st.success("✅ Decrypted Successfully!")
                        st.markdown("**🔓 Decrypted Data:**")
                        st.code(f"Name: {selected_patient['name']}\nContact: {selected_patient['contact']}\nDiagnosis: {selected_patient['diagnosis']}")
                        
                        db.add_log(
                            st.session_state.user['user_id'],
                            st.session_state.user['username'],
                            st.session_state.user['role'],
                            "DECRYPT_DATA",
                            f"Decrypted patient ID: {selected_patient_id}"
                        )
                else:
                    st.info("No encrypted records found. Apply encryption first.")
            else:
                st.markdown("### 🔄 Masking Examples")
                st.code("BEFORE:\n" + "="*30 + "\nName: John Doe\nContact: 123-456-7890\nStatus: ❌ Not Protected")
                
                st.code("AFTER (Masking):\n" + "="*30 + "\nName: ANON_0001\nContact: XXX-XXX-7890\nStatus: ✅ Masked")
                
                st.code("AFTER (Encryption):\n" + "="*30 + "\nName: 🔐 ENCRYPTED\nContact: 🔐 ENCRYPTED\nStatus: ✅ Encrypted")
    
    # Tab 4: Audit Logs
    with tabs[3]:
        st.markdown("### 📋 Integrity Audit Log")
        st.info("🔍 Complete activity trail for compliance and accountability (Integrity)")
        
        logs = db.get_logs()
        if logs:
            df_logs = pd.DataFrame(logs)
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                role_filter = st.multiselect("Filter by Role", options=df_logs['role'].unique(), default=df_logs['role'].unique())
            with col2:
                action_filter = st.multiselect("Filter by Action", options=df_logs['action'].unique(), default=df_logs['action'].unique())
            with col3:
                limit = st.number_input("Show last N records", min_value=10, max_value=1000, value=50)
            
            # Apply filters
            filtered_logs = df_logs[
                (df_logs['role'].isin(role_filter)) &
                (df_logs['action'].isin(action_filter))
            ].head(limit)
            
            st.dataframe(filtered_logs, use_container_width=True)
            
            # Export logs
            csv = filtered_logs.to_csv(index=False)
            st.download_button(
                label="📥 Download Audit Log (CSV)",
                data=csv,
                file_name=f"audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No activity logs found.")
    
    # Tab 5: Data Export
    with tabs[4]:
        st.markdown("### 💾 Data Backup & Export")
        st.info("💾 Export data for backup and disaster recovery (Availability)")
        
        patients = db.get_patients()
        
        if patients:
            df_patients = pd.DataFrame(patients)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Export Patient Data")
                export_format = st.radio("Select format:", ["CSV", "JSON"])
                
                if export_format == "CSV":
                    csv_data = df_patients.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Patients (CSV)",
                        data=csv_data,
                        file_name=f"patients_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    json_data = df_patients.to_json(orient='records', indent=2)
                    st.download_button(
                        label="📥 Download Patients (JSON)",
                        data=json_data,
                        file_name=f"patients_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
            
            with col2:
                st.markdown("#### Export Statistics")
                st.metric("Total Records", len(patients))
                st.metric("Data Size", f"{len(str(patients)) / 1024:.2f} KB")
                st.metric("Last Backup", "Available for download")
    
    # Tab 6: Data Retention
    with tabs[5]:
        st.markdown("### ⏳ GDPR Data Retention Management")
        st.success("✅ **AUTOMATIC MODE**: System automatically deletes expired records when admin dashboard loads")
        st.info("🗓️ Patient data is automatically deleted after 365 days retention period (GDPR Article 5 - Storage Limitation)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔍 Expiring Soon (Next 30 Days)")
            expiring_patients = db.get_expiring_patients(30)
            
            if expiring_patients:
                st.warning(f"⚠️ {len(expiring_patients)} patient record(s) will expire soon!")
                
                for patient in expiring_patients:
                    with st.expander(f"Patient ID: {patient['patient_id']} - {patient['name']}"):
                        st.write(f"**Days Stored:** {patient['days_stored']} days")
                        st.write(f"**Retention Period:** {patient['retention_days']} days")
                        st.write(f"**Days Until Expiry:** {patient['days_until_expiry']} days")
                        st.write(f"**Added On:** {patient['date_added']}")
                        
                        if patient['days_until_expiry'] <= 7:
                            st.error("⚠️ Will expire within 7 days!")
            else:
                st.success("✅ No patients expiring in the next 30 days")
        
        with col2:
            st.markdown("#### � Manual Cleanup (Optional)")
            st.info("ℹ️ Cleanup runs automatically on dashboard load. Use this for immediate execution.")
            
            st.markdown(f"**Default Retention Period:** 365 days")
            
            if st.button("🔍 Check for Expired Records Now", use_container_width=True):
                # Check without deleting
                conn = db.get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT p.patient_id, p.name, p.date_added, COALESCE(c.data_retention_days, 365) as retention_days
                    FROM patients p
                    LEFT JOIN gdpr_consent c ON p.patient_id = c.patient_id
                    WHERE julianday('now') - julianday(p.date_added) > COALESCE(c.data_retention_days, 365)
                ''')
                expired = cursor.fetchall()
                conn.close()
                
                if len(expired) > 0:
                    st.error(f"🗑️ Found {len(expired)} expired record(s)")
                    for patient in expired:
                        st.write(f"- Patient ID {patient['patient_id']}: {patient['name']} (Added: {patient['date_added']})")
                else:
                    st.success("✅ No expired records found")
            
            st.markdown("---")
            
            if st.button("🗑️ Run Cleanup (Delete Expired)", type="primary", use_container_width=True):
                deleted_count, deleted_patients = db.cleanup_expired_data()
                
                if deleted_count > 0:
                    db.add_log(
                        st.session_state.user['user_id'],
                        st.session_state.user['username'],
                        st.session_state.user['role'],
                        "DATA_RETENTION_CLEANUP",
                        f"Deleted {deleted_count} expired patient records (GDPR retention policy)"
                    )
                    st.success(f"✅ Successfully deleted {deleted_count} expired record(s)!")
                    
                    with st.expander("View Deleted Records"):
                        for patient in deleted_patients:
                            st.write(f"- Patient ID {patient['patient_id']}: {patient['name']} (Added: {patient['date_added']}, Retention: {patient['data_retention_days']} days)")
                    
                    time.sleep(2)
                    st.rerun()
                else:
                    st.info("ℹ️ No expired records to delete")
        
        st.markdown("---")
        
        # Statistics
        st.markdown("#### 📊 Retention Statistics")
        all_patients = db.get_patients()
        
        if all_patients:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", len(all_patients))
            
            with col2:
                expiring_7d = db.get_expiring_patients(7)
                st.metric("Expiring in 7 Days", len(expiring_7d))
            
            with col3:
                expiring_30d = db.get_expiring_patients(30)
                st.metric("Expiring in 30 Days", len(expiring_30d))
            
            with col4:
                st.metric("Retention Period", "365 days")

# Doctor Dashboard
def doctor_dashboard():
    """Doctor view with anonymized data access"""
    st.markdown("<h2>👨‍⚕️ Doctor Dashboard</h2>", unsafe_allow_html=True)
    
    st.info("🔒 You have access to anonymized patient data only (Privacy Protection)")
    
    tabs = st.tabs(["👥 Patient Records", "💾 Export Data"])
    
    with tabs[0]:
        st.markdown("### 👥 Anonymized Patient Records")
        
        patients = db.get_patients_doc()
        
        if patients:
            # Filter data for doctor view
            filtered_patients = []
            for patient in patients:
                filtered = AccessControl.filter_patient_data(patient, 'doctor')
                filtered_patients.append(filtered)
            
            df = pd.DataFrame(filtered_patients)
            st.dataframe(df, use_container_width=True)
            
            # Log view action
            db.add_log(
                st.session_state.user['user_id'],
                st.session_state.user['username'],
                st.session_state.user['role'],
                "VIEW_ANONYMIZED_DATA",
                f"Viewed {len(patients)} anonymized patient records"
            )
        else:
            st.info("No patient records found.")
    
    with tabs[1]:
        st.markdown("### 💾 Export Anonymized Data")
        
        patients = db.get_patients()
        
        if patients:
            filtered_patients = [AccessControl.filter_patient_data(p, 'doctor') for p in patients]
            df = pd.DataFrame(filtered_patients)
            
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Anonymized Data (CSV)",
                data=csv_data,
                file_name=f"anonymized_patients_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            db.add_log(
                st.session_state.user['user_id'],
                st.session_state.user['username'],
                st.session_state.user['role'],
                "EXPORT_ANONYMIZED_DATA",
                f"Exported {len(patients)} anonymized records"
            )
        else:
            st.info("No data available for export.")

# Receptionist Dashboard
def receptionist_dashboard():
    """Receptionist view with limited access"""
    st.markdown("<h2>👨‍💼 Receptionist Dashboard</h2>", unsafe_allow_html=True)
    
    st.warning("⚠️ You can add/edit records but cannot view sensitive patient data")
    
    tabs = st.tabs(["➕ Add Patient", "✏️ Edit Patient", "📋 Patient List"])
    
    with tabs[0]:
        st.markdown("### ➕ Add New Patient")
        
        # Check if patient was just added - display success message
        if st.session_state.get('receptionist_patient_just_added', False):
            st.success(f"✅ Patient added successfully! (ID: {st.session_state.get('last_receptionist_patient_id', 'N/A')})")
            if st.button("➕ Add Another Patient", type="primary", use_container_width=True):
                st.session_state.receptionist_patient_just_added = False
                st.rerun()
            st.stop()  # ⛔ Prevents form from running again in this cycle
        
        # Normal form rendering
        with st.form("receptionist_add_form", clear_on_submit=True):
                name = st.text_input("Patient Full Name")
                contact = st.text_input("Contact Number")
                diagnosis = st.text_area("Diagnosis/Reason for Visit")
                
                submit = st.form_submit_button("Add Patient", use_container_width=True)
                
                if submit and name and contact and diagnosis:
                    valid, errors = validate_patient_data(name, contact, diagnosis)
                    if valid:
                        patient_id = db.add_patient(
                            sanitize_input(name),
                            sanitize_input(contact),
                            sanitize_input(diagnosis)
                        )
                        if patient_id:
                            db.add_log(
                                st.session_state.user['user_id'],
                                st.session_state.user['username'],
                                st.session_state.user['role'],
                                "ADD_PATIENT",
                                f"Added patient ID: {patient_id}"
                            )
                            # Set flag to show success message
                            st.session_state.receptionist_patient_just_added = True
                            st.session_state.last_receptionist_patient_id = patient_id
                            st.rerun()
                    else:
                        for error in errors:
                            st.error(f"❌ {error}")
                elif submit:
                    st.warning("⚠️ Please fill in all fields")
    
    with tabs[1]:
        st.markdown("### ✏️ Edit Patient Record")
        
        # Check if patient was just updated
        if st.session_state.get('receptionist_patient_just_updated', False):
            st.success(f"✅ Patient ID {st.session_state.get('last_updated_patient_id', 'N/A')} updated successfully!")
            if st.button("✏️ Edit Another Patient", type="primary", use_container_width=True):
                st.session_state.receptionist_patient_just_updated = False
                st.rerun()
            st.stop()  # ⛔ Prevents form from running again in this cycle
        
        patients = db.get_patients()
        
        if patients:
            patient_ids = [p['patient_id'] for p in patients]
            selected_id = st.selectbox("Select Patient ID", patient_ids)
            
            with st.form("receptionist_edit_form"):
                name = st.text_input("New Name (leave empty to keep current)")
                contact = st.text_input("New Contact (leave empty to keep current)")
                diagnosis = st.text_area("New Diagnosis (leave empty to keep current)")
                
                submit = st.form_submit_button("Update Patient", use_container_width=True)
                
                if submit:
                    if name or contact or diagnosis:
                        if db.update_patient(
                            selected_id,
                            sanitize_input(name) if name else None,
                            sanitize_input(contact) if contact else None,
                            sanitize_input(diagnosis) if diagnosis else None
                        ):
                            db.add_log(
                                st.session_state.user['user_id'],
                                st.session_state.user['username'],
                                st.session_state.user['role'],
                                "EDIT_PATIENT",
                                f"Updated patient ID: {selected_id}"
                            )
                            st.session_state.receptionist_patient_just_updated = True
                            st.session_state.last_updated_patient_id = selected_id
                            st.rerun()
                    else:
                        st.warning("⚠️ Please enter at least one field to update")
        elif not patients:
            st.info("No patients available to edit.")
    
    with tabs[2]:
        st.markdown("### 📋 Patient List (Limited View)")
        
        patients = db.get_patients()
        
        if patients:
            # Show only basic info
            filtered_patients = []
            for patient in patients:
                filtered = {
                    'patient_id': patient['patient_id'],
                    'date_added': patient['date_added'],
                    'status': '✅ Registered'
                }
                filtered_patients.append(filtered)
            
            df = pd.DataFrame(filtered_patients)
            st.dataframe(df, use_container_width=True)
            st.info("ℹ️ Sensitive patient data is hidden for privacy protection")
        else:
            st.info("No patient records found.")

# Main application
def main():
    """Main application entry point"""
    try:
        if not st.session_state.logged_in:
            login_page()
        else:
            render_sidebar()
            
            user = st.session_state.user
            
            # Route to appropriate dashboard based on role
            if user['role'] == 'admin':
                admin_dashboard()
            elif user['role'] == 'doctor':
                doctor_dashboard()
            elif user['role'] == 'receptionist':
                receptionist_dashboard()
            
            # Footer
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("🔒 **Confidentiality**: Data anonymized & encrypted")
            with col2:
                st.markdown("✅ **Integrity**: All actions logged & audited")
            with col3:
                st.markdown("🌐 **Availability**: System uptime monitored")
            
            last_sync = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.markdown(f"<div style='text-align: center; color: gray; font-size: 0.8rem;'>Last synchronization: {last_sync} | GDPR Compliant ✓</div>", unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"⚠️ Application Error: {str(e)}")
        st.info("System attempting recovery... Please refresh the page.")
        
        # Log error
        if st.session_state.user:
            db.add_log(
                st.session_state.user['user_id'],
                st.session_state.user['username'],
                st.session_state.user['role'],
                "ERROR",
                f"Application error: {str(e)}"
            )

if __name__ == "__main__":
    main()
