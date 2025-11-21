"""
System Diagram Generator
Creates a visual representation of the Hospital Management System architecture
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# Check if matplotlib is available
try:
    import matplotlib
    print("Matplotlib available - can generate diagrams")
except ImportError:
    print("Matplotlib not installed. Install with: pip install matplotlib")
    exit(1)

def create_cia_diagram():
    """Create CIA Triad implementation diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Hospital Management System - CIA Triad', 
            ha='center', va='top', fontsize=20, fontweight='bold')
    
    # Confidentiality box
    conf_box = FancyBboxPatch((0.5, 6), 2.5, 2.5, 
                               boxstyle="round,pad=0.1", 
                               edgecolor='blue', facecolor='lightblue', linewidth=2)
    ax.add_patch(conf_box)
    ax.text(1.75, 7.8, 'CONFIDENTIALITY', ha='center', fontsize=12, fontweight='bold')
    ax.text(1.75, 7.4, '🔒 Data Anonymization', ha='center', fontsize=9)
    ax.text(1.75, 7.1, '🔐 Fernet Encryption', ha='center', fontsize=9)
    ax.text(1.75, 6.8, '🔑 RBAC', ha='center', fontsize=9)
    ax.text(1.75, 6.5, '👤 User Roles', ha='center', fontsize=9)
    
    # Integrity box
    int_box = FancyBboxPatch((3.75, 6), 2.5, 2.5, 
                              boxstyle="round,pad=0.1", 
                              edgecolor='green', facecolor='lightgreen', linewidth=2)
    ax.add_patch(int_box)
    ax.text(5, 7.8, 'INTEGRITY', ha='center', fontsize=12, fontweight='bold')
    ax.text(5, 7.4, '📝 Activity Logging', ha='center', fontsize=9)
    ax.text(5, 7.1, '✅ Audit Trail', ha='center', fontsize=9)
    ax.text(5, 6.8, '🛡️ Input Validation', ha='center', fontsize=9)
    ax.text(5, 6.5, '⏰ Timestamps', ha='center', fontsize=9)
    
    # Availability box
    avail_box = FancyBboxPatch((7, 6), 2.5, 2.5, 
                                boxstyle="round,pad=0.1", 
                                edgecolor='red', facecolor='lightcoral', linewidth=2)
    ax.add_patch(avail_box)
    ax.text(8.25, 7.8, 'AVAILABILITY', ha='center', fontsize=12, fontweight='bold')
    ax.text(8.25, 7.4, '🔄 Error Handling', ha='center', fontsize=9)
    ax.text(8.25, 7.1, '💾 Data Backup', ha='center', fontsize=9)
    ax.text(8.25, 6.8, '📊 Export (CSV/JSON)', ha='center', fontsize=9)
    ax.text(8.25, 6.5, '⏱️ Uptime Monitor', ha='center', fontsize=9)
    
    # System layers
    # UI Layer
    ui_box = FancyBboxPatch((1.5, 4), 7, 1, 
                             boxstyle="round,pad=0.1", 
                             edgecolor='purple', facecolor='lavender', linewidth=2)
    ax.add_patch(ui_box)
    ax.text(5, 4.5, 'Streamlit Web Interface | Admin | Doctor | Receptionist', 
            ha='center', fontsize=10, fontweight='bold')
    
    # Application Layer
    app_box = FancyBboxPatch((1.5, 2.5), 7, 1, 
                              boxstyle="round,pad=0.1", 
                              edgecolor='orange', facecolor='peachpuff', linewidth=2)
    ax.add_patch(app_box)
    ax.text(5, 3, 'Application Layer (app.py) | Authentication | Session Management', 
            ha='center', fontsize=10, fontweight='bold')
    
    # Module Layer
    privacy_box = FancyBboxPatch((1.5, 1), 3, 1, 
                                  boxstyle="round,pad=0.1", 
                                  edgecolor='teal', facecolor='lightcyan', linewidth=2)
    ax.add_patch(privacy_box)
    ax.text(3, 1.5, 'Privacy Module\n(privacy.py)', ha='center', fontsize=9)
    
    db_box = FancyBboxPatch((5.5, 1), 3, 1, 
                             boxstyle="round,pad=0.1", 
                             edgecolor='brown', facecolor='wheat', linewidth=2)
    ax.add_patch(db_box)
    ax.text(7, 1.5, 'Database Module\n(database.py)', ha='center', fontsize=9)
    
    # Database
    db_circle = mpatches.Circle((5, 0.3), 0.3, color='gray', ec='black', linewidth=2)
    ax.add_patch(db_circle)
    ax.text(5, 0.3, 'DB', ha='center', va='center', fontsize=10, color='white', fontweight='bold')
    ax.text(5, -0.2, 'hospital.db (SQLite)', ha='center', fontsize=8)
    
    # Add GDPR badge
    gdpr_box = FancyBboxPatch((8.5, 9), 1.2, 0.5, 
                               boxstyle="round,pad=0.05", 
                               edgecolor='darkgreen', facecolor='lightgreen', linewidth=2)
    ax.add_patch(gdpr_box)
    ax.text(9.1, 9.25, 'GDPR\nCompliant', ha='center', fontsize=8, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('system_architecture.png', dpi=300, bbox_inches='tight')
    print("✅ System architecture diagram saved as 'system_architecture.png'")
    plt.close()

def create_role_diagram():
    """Create role-based access control diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Role-Based Access Control (RBAC)', 
            ha='center', va='top', fontsize=18, fontweight='bold')
    
    # Admin role
    admin_box = FancyBboxPatch((0.5, 6.5), 2.5, 2, 
                                boxstyle="round,pad=0.1", 
                                edgecolor='darkred', facecolor='lightcoral', linewidth=3)
    ax.add_patch(admin_box)
    ax.text(1.75, 8, '👨‍💼 ADMIN', ha='center', fontsize=14, fontweight='bold')
    ax.text(1.75, 7.5, '✅ Full Access', ha='center', fontsize=9)
    ax.text(1.75, 7.2, '✅ View Raw Data', ha='center', fontsize=8)
    ax.text(1.75, 6.9, '✅ Anonymize', ha='center', fontsize=8)
    
    # Doctor role
    doctor_box = FancyBboxPatch((3.75, 6.5), 2.5, 2, 
                                 boxstyle="round,pad=0.1", 
                                 edgecolor='darkblue', facecolor='lightblue', linewidth=3)
    ax.add_patch(doctor_box)
    ax.text(5, 8, '👨‍⚕️ DOCTOR', ha='center', fontsize=14, fontweight='bold')
    ax.text(5, 7.5, '⚠️ Limited Access', ha='center', fontsize=9)
    ax.text(5, 7.2, '✅ Anonymized Only', ha='center', fontsize=8)
    ax.text(5, 6.9, '❌ No Raw Data', ha='center', fontsize=8)
    
    # Receptionist role
    recep_box = FancyBboxPatch((7, 6.5), 2.5, 2, 
                                boxstyle="round,pad=0.1", 
                                edgecolor='darkgreen', facecolor='lightgreen', linewidth=3)
    ax.add_patch(recep_box)
    ax.text(8.25, 8, '👩‍💼 RECEPTIONIST', ha='center', fontsize=14, fontweight='bold')
    ax.text(8.25, 7.5, '⚠️ Minimal Access', ha='center', fontsize=9)
    ax.text(8.25, 7.2, '✅ Add/Edit', ha='center', fontsize=8)
    ax.text(8.25, 6.9, '❌ No View Rights', ha='center', fontsize=8)
    
    # Data access levels
    raw_box = FancyBboxPatch((1, 4), 3, 1, 
                              boxstyle="round,pad=0.1", 
                              edgecolor='black', facecolor='white', linewidth=2)
    ax.add_patch(raw_box)
    ax.text(2.5, 4.5, '📄 RAW DATA\n(Admin Only)', ha='center', fontsize=10, fontweight='bold')
    
    anon_box = FancyBboxPatch((4.5, 4), 3, 1, 
                               boxstyle="round,pad=0.1", 
                               edgecolor='black', facecolor='lightyellow', linewidth=2)
    ax.add_patch(anon_box)
    ax.text(6, 4.5, '🔒 ANONYMIZED\n(Doctor View)', ha='center', fontsize=10, fontweight='bold')
    
    # Examples
    ex_box = FancyBboxPatch((1, 1.5), 8, 2, 
                             boxstyle="round,pad=0.1", 
                             edgecolor='gray', facecolor='whitesmoke', linewidth=1)
    ax.add_patch(ex_box)
    ax.text(5, 3, 'Data Masking Examples', ha='center', fontsize=12, fontweight='bold')
    ax.text(2.5, 2.5, 'Original:', ha='left', fontsize=9, fontweight='bold')
    ax.text(2.5, 2.2, 'Name: John Doe', ha='left', fontsize=8)
    ax.text(2.5, 1.9, 'Contact: 123-456-7890', ha='left', fontsize=8)
    
    ax.text(6.5, 2.5, 'Anonymized:', ha='left', fontsize=9, fontweight='bold')
    ax.text(6.5, 2.2, 'Name: ANON_0001', ha='left', fontsize=8)
    ax.text(6.5, 1.9, 'Contact: XXX-XXX-7890', ha='left', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('rbac_diagram.png', dpi=300, bbox_inches='tight')
    print("✅ RBAC diagram saved as 'rbac_diagram.png'")
    plt.close()

if __name__ == "__main__":
    print("Generating system diagrams...")
    print("-" * 50)
    
    try:
        create_cia_diagram()
        create_role_diagram()
        print("-" * 50)
        print("✅ All diagrams generated successfully!")
        print("\nUse these diagrams in your PDF report!")
    except Exception as e:
        print(f"❌ Error generating diagrams: {e}")
        print("Note: Install matplotlib if needed: pip install matplotlib")
