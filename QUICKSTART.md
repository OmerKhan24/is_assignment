# 🚀 Quick Start Guide
## Hospital Management System - GDPR Compliant

### ⚡ Fast Setup (3 Steps)

#### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

#### Step 2: Initialize Database
```powershell
python database.py
```

#### Step 3: Run Application
```powershell
streamlit run app.py
```

---

### 🎯 OR Use Automated Setup

```powershell
.\setup.ps1
```

---

### 🔑 Login Credentials

| Role | Username | Password |
|------|----------|----------|
| 👨‍💼 Admin | admin | admin123 |
| 👨‍⚕️ Doctor | Dr.Bob | doc123 |
| 👩‍💼 Receptionist | Alice_recep | rec123 |

---

### 📋 What to Test

#### As Admin:
1. ✅ Login with admin credentials
2. ✅ View dashboard metrics
3. ✅ Add new patient
4. ✅ Click "Anonymize All Patients"
5. ✅ View audit logs
6. ✅ Export data to CSV

#### As Doctor:
1. ✅ Login with doctor credentials
2. ✅ View anonymized patient data
3. ✅ Export anonymized data

#### As Receptionist:
1. ✅ Login with receptionist credentials
2. ✅ Add new patient
3. ✅ Edit patient record
4. ✅ Notice sensitive data is hidden

---

### 📁 Project Files

```
Assignment_04/
├── app.py              # Main application
├── database.py         # Database operations
├── privacy.py          # Security & privacy
├── requirements.txt    # Dependencies
├── Assignment4.ipynb   # Documentation
├── README.md          # Full documentation
└── setup.ps1          # Setup script
```

---

### 🎥 Demo Video Checklist

Record a 2-3 minute video showing:
- [ ] Login with different roles
- [ ] Adding a patient
- [ ] Anonymizing data
- [ ] Viewing audit logs
- [ ] Role-based access control
- [ ] Data export

Upload to Google Drive and add link to PDF report!

---

### 📊 Features to Highlight in Report

#### Confidentiality ✅
- Data anonymization (ANON_XXXX)
- Contact masking (XXX-XXX-XXXX)
- Fernet encryption
- Role-based access

#### Integrity ✅
- Activity logging
- Audit trail
- Input validation
- Timestamps

#### Availability ✅
- Error handling
- Data backup/export
- System uptime monitoring
- Session management

#### GDPR Compliance ✅
- Consent banner
- Data retention (365 days)
- Right to be forgotten
- Transparency

#### Bonus Features ✅
- Real-time graphs
- Fernet encryption
- GDPR features

---

### 📝 PDF Report Structure

1. **System Overview Diagram** (CIA layers)
2. **Screenshots**:
   - Login page with GDPR banner
   - Admin dashboard
   - Anonymization before/after
   - Audit logs
   - Doctor view (anonymized)
3. **CIA Implementation Discussion**
4. **GDPR Alignment**
5. **Demo Video Link**

---

### 🔧 Troubleshooting

**Error: Module not found**
```powershell
pip install streamlit pandas cryptography plotly
```

**Error: Database not found**
```powershell
python database.py
```

**Error: Port in use**
```powershell
streamlit run app.py --server.port 8502
```

---

### ✅ Submission Checklist

- [ ] All .py files
- [ ] hospital.db file
- [ ] Assignment4.ipynb
- [ ] PDF Report (3-5 pages)
- [ ] Demo Video Link
- [ ] README.md

---

### 🎓 Grading Rubric (100 + 2 Bonus)

| Component | Marks | Status |
|-----------|-------|--------|
| Privacy & GDPR | 20 | ✅ |
| Confidentiality | 20 | ✅ |
| Integrity | 20 | ✅ |
| Availability | 15 | ✅ |
| Dashboard | 10 | ✅ |
| Documentation | 10 | ✅ |
| Presentation | 5 | ✅ |
| **Bonus** | +2 | ✅ |

---

### 💡 Tips

1. **Run Jupyter Notebook** for detailed walkthrough
   ```powershell
   jupyter notebook Assignment4.ipynb
   ```

2. **Take Screenshots** while testing different roles

3. **Record Video** showing all features

4. **Export Audit Logs** to show integrity

5. **Show Anonymization** before and after

---

### 🏆 Success Criteria

✅ All three roles working  
✅ Data anonymization functional  
✅ Audit logs recording actions  
✅ GDPR compliance features  
✅ Export functionality  
✅ Error handling working  
✅ Clean UI/UX  

---

**Ready to Submit!** 🎉

*Make sure to include Google Drive link for demo video in your PDF report.*
