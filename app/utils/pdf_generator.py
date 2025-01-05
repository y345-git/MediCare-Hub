from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO

def create_patient_pdf(patient):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30
    )
    story.append(Paragraph(f"Patient Report - {patient['name']}", title_style))

    # Define section style
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=10,
        spaceBefore=20
    )
    
    # General Information
    story.append(Paragraph("General Information", section_style))
    general_info = [
        ["Name", patient['name']],
        ["OPD/UID", patient['opd_uid']],
        ["Age", str(patient['age'])],
        ["Gender", patient['gender']],
        ["Doctor Referred", patient.get('doctor_referred', '')],
        ["Address", patient['address']],
        ["Husband's Occupation", patient.get('occupation_husband', '')],
        ["Wife's Occupation", patient.get('occupation_wife', '')],
        ["Education", patient.get('education', '')],
        ["Phone 1", patient['phone1']],
        ["Phone 2", patient.get('phone2', '')],
        ["Email", patient.get('email', '')],
        ["Has Insurance", "Yes" if patient.get('has_insurance') else "No"],
        ["Registration Date", patient['registration_date'].strftime('%Y-%m-%d') if patient['registration_date'] else ''],
    ]
    story.append(create_table(general_info))

    # Family Information
    story.append(Paragraph("Family Information", section_style))
    family_info = [
        ["Years of Marriage", str(patient.get('years_of_marriage', ''))],
        ["Number of Boys", str(patient.get('boys_count', 0))],
        ["Number of Girls", str(patient.get('girls_count', 0))],
        ["Previous Abortion", "Yes" if patient.get('had_abortion') else "No"],
        ["Number of Abortions", str(patient.get('abortion_count', 0))],
        ["Delivery Type", patient.get('delivery_type', '')],
    ]
    story.append(create_table(family_info))

    # Menstrual Information
    story.append(Paragraph("Menstrual Information", section_style))
    menstrual_info = [
        ["Last Menstruation Date", patient.get('last_menstruation_date', '').strftime('%Y-%m-%d') if patient.get('last_menstruation_date') else ''],
        ["Days of Bleeding", str(patient.get('menstruation_days', ''))],
        ["Cycle Length (days)", str(patient.get('menstruation_cycle_length', ''))],
        ["Age When Started", str(patient.get('menstruation_start_age', ''))],
    ]
    story.append(create_table(menstrual_info))

    # Medical History
    story.append(Paragraph("Medical History", section_style))
    medical_conditions = []
    if patient.get('has_thyroid'): medical_conditions.append("Thyroid")
    if patient.get('has_diabetes'): medical_conditions.append("Diabetes")
    if patient.get('has_asthma'): medical_conditions.append("Asthma")
    if patient.get('has_bp'): medical_conditions.append("High Blood Pressure")
    if patient.get('has_epilepsy'): medical_conditions.append("Epilepsy")
    
    medical_history = [
        ["Medical Conditions", ", ".join(medical_conditions) if medical_conditions else "None"],
        ["Currently on Medication", "Yes" if patient.get('on_medication') else "No"],
        ["Medication Names", patient.get('medication_names', '')],
        ["Previous Surgeries", patient.get('previous_surgeries', '')],
        ["Previous Pap Smear", "Yes" if patient.get('had_pap_smear') else "No"],
        ["Days since Pap Smear", str(patient.get('pap_smear_days', ''))],
        ["Medicine Allergies", patient.get('medicine_allergies', '')],
        ["Family History of Cancer", "Yes" if patient.get('has_cancer_history') else "No"],
        ["Previous Reports", patient.get('previous_reports', '')],
    ]
    story.append(create_table(medical_history))

    # Symptoms & Complaints
    story.append(Paragraph("Symptoms & Complaints", section_style))
    symptoms = [
        ["Blood Clots", f"{'Yes' if patient.get('has_blood_clots') else 'No'} ({patient.get('blood_clots_days', '')} days)"],
        ["White Discharge", f"{'Yes' if patient.get('has_white_discharge') else 'No'} ({patient.get('white_discharge_days', '')} days)"],
        ["Red Discharge", f"{'Yes' if patient.get('has_red_discharge') else 'No'} ({patient.get('red_discharge_days', '')} days)"],
        ["Abdominal Pain", f"{'Yes' if patient.get('has_abdominal_pain') else 'No'} ({patient.get('abdominal_pain_days', '')} days)"],
        ["Vaginal Discharge", f"{'Yes' if patient.get('has_vaginal_discharge') else 'No'} ({patient.get('vaginal_discharge_days', '')} days)"],
        ["Bleeding After Intercourse", f"{'Yes' if patient.get('has_bleeding_intercourse') else 'No'} ({patient.get('bleeding_intercourse_days', '')} days)"],
        ["Urine Leakage", f"{'Yes' if patient.get('has_urine_leakage') else 'No'} ({patient.get('urine_leakage_days', '')} days)"],
        ["Post Menopausal Bleeding", f"{'Yes' if patient.get('has_postmenopausal_bleeding') else 'No'} ({patient.get('postmenopausal_bleeding_days', '')} days)"],
        ["Breast Lump", f"{'Yes' if patient.get('has_breast_lump') else 'No'} ({patient.get('breast_lump_days', '')} days)"],
        ["Infertility", f"{'Yes' if patient.get('has_infertility') else 'No'} ({patient.get('infertility_days', '')} days)"],
        ["Other Troubles", patient.get('other_troubles', '')],
        ["Other Troubles Days", str(patient.get('other_troubles_days', ''))],
    ]
    story.append(create_table(symptoms))

    # General Examination
    story.append(Paragraph("General Examination", section_style))
    examination = [
        ["Height", f"{patient.get('height', '')} cm"],
        ["Weight", f"{patient.get('weight', '')} kg"],
        ["Blood Pressure", patient.get('blood_pressure', '')],
        ["Pulse Rate", str(patient.get('pulse_rate', ''))],
        ["Pallar", patient.get('pallar', '')],
        ["Edema", patient.get('edema', '')],
        ["Thyroid Exam", patient.get('thyroid_exam', '')],
        ["Lymph Nodes", patient.get('lymph_nodes', '')],
        ["Breast Exam", patient.get('breast_exam', '')],
        ["RS Exam", patient.get('rs_exam', '')],
        ["CVS Exam", patient.get('cvs_exam', '')],
        ["P/A Exam", patient.get('pa_exam', '')],
        ["P/S/V Exam", patient.get('psv_exam', '')],
        ["P/R Exam", patient.get('pr_exam', '')],
    ]
    story.append(create_table(examination))

    # Surgery Details
    story.append(Paragraph("Surgery Details", section_style))
    surgery = [
        ["Surgery Name", patient.get('surgery_name', '')],
        ["Surgery Date", patient.get('surgery_date', '').strftime('%Y-%m-%d') if patient.get('surgery_date') else ''],
        ["Hospital", patient.get('surgery_hospital', '')],
        ["Pre-op Investigation", patient.get('preop_investigation', '')],
        ["Pre-op Fitness", patient.get('preop_fitness', '')],
    ]
    story.append(create_table(surgery))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

def create_table(data):
    table = Table(data, colWidths=[2.5*inch, 4*inch])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Align text to top for multi-line cells
    ]))
    return table 