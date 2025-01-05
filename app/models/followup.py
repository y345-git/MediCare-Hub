from app.models.user import get_db_connection
from datetime import datetime

def create_followup(followup_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO followups (
            patient_id, visit_date, complaints, examination, 
            diagnosis, treatment, next_visit_date, doctor_name,
            created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (
        followup_data['patient_id'],
        followup_data['visit_date'],
        followup_data['complaints'],
        followup_data['examination'],
        followup_data['diagnosis'],
        followup_data['treatment'],
        followup_data['next_visit_date'],
        followup_data['doctor_name'],
        datetime.now()
    )
    
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.lastrowid

def get_patient_followups(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get all followups for the patient
    query = """
        SELECT * FROM followups 
        WHERE patient_id = %s 
        ORDER BY visit_date DESC
    """
    cursor.execute(query, (patient_id,))
    followups = cursor.fetchall()
    
    # Get prescriptions for each followup
    for followup in followups:
        query = """
            SELECT * FROM prescriptions 
            WHERE followup_id = %s 
            ORDER BY created_at
        """
        cursor.execute(query, (followup['id'],))
        followup['prescriptions'] = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return followups

def get_followup_by_id(followup_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get followup details
    query = "SELECT * FROM followups WHERE id = %s"
    cursor.execute(query, (followup_id,))
    followup = cursor.fetchone()
    
    if followup:
        # Get prescriptions for this followup
        query = """
            SELECT * FROM prescriptions 
            WHERE followup_id = %s 
            ORDER BY created_at
        """
        cursor.execute(query, (followup_id,))
        followup['prescriptions'] = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return followup

def delete_followup_record(followup_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # First delete associated prescriptions
        cursor.execute("DELETE FROM prescriptions WHERE followup_id = %s", (followup_id,))
        
        # Then delete the followup
        cursor.execute("DELETE FROM followups WHERE id = %s", (followup_id,))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close() 