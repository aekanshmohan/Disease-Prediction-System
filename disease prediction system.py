#
"""
Disease-Prediction-System 
"""

import sys
import mysql.connector
from typing import List, Tuple
from datetime import datetime

# CONFIGURATION
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'disease_prediction_system'}

MIN_MATCH = 3
TOP_N = 3

# DB CONNECTION

def connect_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as e:
        print("Could not connect to the database:", e)
        sys.exit(1)

# UTILITIES 

def placeholders(n):
    if n < 1:
        raise ValueError("Number of placeholders must be at least 1.")
    return ','.join(['%s'] * n)


# DB SETUP

def setup_database(conn):
    cur = conn.cursor()
    try:
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE ) """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS symptoms (
                symptom_id INT AUTO_INCREMENT PRIMARY KEY,
                symptom_name VARCHAR(200) NOT NULL UNIQUE)""")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS diseases (
                disease_id INT AUTO_INCREMENT PRIMARY KEY,
                disease_name VARCHAR(200) NOT NULL UNIQUE,
                description TEXT ) """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS disease_symptoms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                disease_id INT NOT NULL,
                symptom_id INT NOT NULL,
                UNIQUE (disease_id, symptom_id),
                FOREIGN KEY (disease_id) REFERENCES diseases(disease_id) ON DELETE CASCADE,
                FOREIGN KEY (symptom_id) REFERENCES symptoms(symptom_id) ON DELETE CASCADE )""")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS disease_medications (
                med_id INT AUTO_INCREMENT PRIMARY KEY,
                disease_id INT NOT NULL,
                medication_text TEXT,
                FOREIGN KEY (disease_id) REFERENCES diseases(disease_id) ON DELETE CASCADE ) """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS diagnosis_history (
                history_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                selected_symptoms TEXT,
                possible_diseases TEXT,
                match_percentages TEXT,
                date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE) """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS support_requests (
                support_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                symptoms_text TEXT,
                system_suggestions TEXT,
                user_message TEXT,
                status ENUM('Pending','Closed') DEFAULT 'Pending',
                resolution_text TEXT,
                timestamp_request TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                timestamp_resolved TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE )""")
        conn.commit()

        # symptoms
        sample_symptoms = [
            "Fever","High fever","Chills","Sweating","Headache","Severe headache","Body pain","Joint pain",
            "Muscle pain","Cough","Dry cough","Cough with mucus","Sore throat","Nasal congestion","Runny nose",
            "Sneezing","Shortness of breath","Chest pain","Fatigue","Weakness","Nausea","Vomiting","Diarrhea",
            "Stomach pain","Loss of appetite","Rash","Skin redness","Itching","Dizziness","Light sensitivity",
            "Sound sensitivity","Blurred vision","Abdominal cramps","Yellow urine","Dark urine","Jaundice",
            "Swollen lymph nodes","Back pain","Loss of smell","Loss of taste","Mild fever","Painful urination","Frequent urination",
            "Watery eyes","Local pain","Swelling","Ear pain","Hearing reduction","Blood in urine"
        ]
        for s in sample_symptoms:
            cur.execute("INSERT IGNORE INTO symptoms (symptom_name) VALUES (%s)", (s,))
        conn.commit()

        # diseases
        sample_diseases = [
            ("Common Cold","Viral infection of upper respiratory tract."),
            ("Influenza (Flu)","Viral respiratory infection with fever and body aches."),
            ("COVID-19","Viral infection that may cause fever, cough, loss of smell/taste."),
            ("Dengue","Viral infection spread by mosquitoes causing high fever and body pain."),
            ("Malaria","Parasite infection with cyclical high fever, chills, sweating."),
            ("Typhoid","Bacterial infection causing sustained high fever and abdominal pain."),
            ("Gastroenteritis / Food poisoning","Stomach infection causing vomiting and diarrhea."),
            ("Pneumonia","Lung infection producing cough, fever, chest pain."),
            ("Migraine","Severe headache often with nausea and light/sound sensitivity."),
            ("Urinary Tract Infection (UTI)","Bladder/kidney infection causing painful urination."),
            ("Hepatitis (Viral)","Inflammation of liver causing jaundice and dark urine."),
            ("Allergic Rhinitis","Allergic reaction causing sneezing and runny nose."),
            ("Bronchitis","Inflammation of bronchi with cough and sputum."),
            ("Hypertension (Symptomatic)","High blood pressure symptoms such as headache (note: diagnosis needs BP measurement)."),
            ("Vitamin D Deficiency","Generalized body pain and fatigue; diagnosis requires blood test."),
            ("Sprain/Strain","Local muscle or joint pain after injury."),
            ("Ear Infection","Ear pain often with fever and reduced hearing."),
            ("Food Allergy","Immediate reactions like itching, rash, vomiting after food."),
            ("Urinary Stones","Severe abdominal/back pain and dark urine."),
            ("Viral Fever / Non-specific viral infection","Fever with body aches and fatigue.")
        ]
        for name, desc in sample_diseases:
            cur.execute("INSERT IGNORE INTO diseases (disease_name, description) VALUES (%s, %s)", (name, desc))
        conn.commit()

        # disease -symptoms mapping
        ds_map = {
            "Common Cold": ["Sneezing","Runny nose","Sore throat","Nasal congestion","Cough","Mild fever"],
            "Influenza (Flu)": ["Fever","Headache","Body pain","Fatigue","Cough","Sore throat"],
            "COVID-19": ["Fever","Cough","Loss of smell","Loss of taste","Shortness of breath","Fatigue"],
            "Dengue": ["High fever","Headache","Severe headache","Body pain","Joint pain","Rash"],
            "Malaria": ["High fever","Chills","Sweating","Body pain","Headache","Nausea"],
            "Typhoid": ["High fever","Abdominal cramps","Weakness","Headache","Loss of appetite","Diarrhea"],
            "Gastroenteritis / Food poisoning": ["Vomiting","Diarrhea","Stomach pain","Abdominal cramps","Nausea"],
            "Pneumonia": ["High fever","Cough with mucus","Chest pain","Shortness of breath","Fatigue"],
            "Migraine": ["Severe headache","Nausea","Vomiting","Light sensitivity","Sound sensitivity"],
            "Urinary Tract Infection (UTI)": ["Painful urination","Frequent urination","Dark urine","Abdominal cramps","Fever"],
            "Hepatitis (Viral)": ["Jaundice","Dark urine","Weakness","Loss of appetite","Abdominal cramps"],
            "Allergic Rhinitis": ["Sneezing","Runny nose","Itching","Nasal congestion","Watery eyes"],
            "Bronchitis": ["Cough","Cough with mucus","Chest pain","Fatigue","Shortness of breath"],
            "Hypertension (Symptomatic)": ["Headache","Dizziness","Blurred vision","Nosebleed"],
            "Vitamin D Deficiency": ["Body pain","Muscle pain","Fatigue","Weakness"],
            "Sprain/Strain": ["Local pain","Swelling","Back pain"],
            "Ear Infection": ["Ear pain","Hearing reduction","Dizziness"],
            "Food Allergy": ["Rash","Itching","Nausea","Vomiting","Swelling"],
            "Urinary Stones": ["Severe abdominal/back pain","Dark urine","Vomiting","Blood in urine"],
            "Viral Fever / Non-specific viral infection": ["Fever","Headache","Body pain","Fatigue","Mild cough"]
        }

        # symptom mapping
        cur.execute("SELECT symptom_id, symptom_name FROM symptoms")
        symptom_rows = cur.fetchall()
        symptom_map = {name.strip().lower(): sid for sid, name in symptom_rows}

        for disease_name, symptom_list in ds_map.items():
            cur.execute("SELECT disease_id FROM diseases WHERE disease_name=%s", (disease_name,))
            row = cur.fetchone()
            if not row:
                continue
            disease_id = row[0]
            for sym in symptom_list:
                key = sym.strip().lower()
                sid = symptom_map.get(key)
                if not sid:
                    cur.execute("INSERT IGNORE INTO symptoms (symptom_name) VALUES (%s)", (sym,))
                    conn.commit()
                    cur.execute("SELECT symptom_id FROM symptoms WHERE symptom_name=%s", (sym,))
                    sid = cur.fetchone()[0]
                    symptom_map[key] = sid
                cur.execute("INSERT IGNORE INTO disease_symptoms (disease_id, symptom_id) VALUES (%s, %s)", (disease_id, sid))
        conn.commit()

        # medications
        meds_map = {
            "Common Cold": ["Rest and fluids", "Paracetamol for fever/pain", "Steam inhalation"],
            "Influenza (Flu)": ["Rest and fluids", "Paracetamol for fever", "Consult doctor if breathing difficulty"],
            "COVID-19": ["Isolate & monitor symptoms", "Paracetamol for fever", "Seek medical care if breathing difficulty"],
            "Dengue": ["Plenty of fluids / ORS", "Paracetamol for fever (avoid aspirin/ibuprofen)", "Seek immediate medical attention for high fever"],
            "Malaria": ["Seek medical attention/prescription antimalarials", "Paracetamol for fever", "Hydration"],
            "Typhoid": ["Consult doctor for antibiotics", "Hydration", "Avoid self-medication"],
            "Gastroenteritis / Food poisoning": ["Hydration/ORS", "BRAT diet (bananas, rice, applesauce, toast)", "See doctor if severe vomiting or bloody diarrhea"],
            "Pneumonia": ["Seek medical care (may require antibiotics)", "Rest and fluids", "Follow physician instructions"],
            "Migraine": ["Paracetamol / OTC analgesic as tolerated", "Rest in dark quiet room", "Hydration"],
            "Urinary Tract Infection (UTI)": ["Consult doctor for antibiotics", "Increase fluids", "Urine test recommended"],
            "Hepatitis (Viral)": ["Seek medical evaluation", "Rest and avoid alcohol", "Hydration and nutrition"],
            "Allergic Rhinitis": ["Antihistamines (OTC)", "Avoid allergens", "Saline nasal rinse"],
            "Bronchitis": ["Rest and fluids", "Steam inhalation", "See doctor if persistent cough or fever"],
            "Hypertension (Symptomatic)": ["Check blood pressure", "See physician for BP monitoring", "Avoid salt and stress"],
            "Vitamin D Deficiency": ["Sun exposure", "Dietary sources (milk, egg yolk)", "Medical test & supplements if advised by doctor"],
            "Sprain/Strain": ["Rest, ice, compression, elevation (RICE)", "Pain relievers like paracetamol"],
            "Ear Infection": ["See physician for ear exam", "Pain relief with paracetamol", "Avoid self ear irrigation"],
            "Food Allergy": ["Avoid triggering food", "Antihistamines for mild reactions", "Seek emergency care for breathing difficulty"],
            "Urinary Stones": ["Seek immediate medical attention", "Pain control under supervision", "Hydration"],
            "Viral Fever / Non-specific viral infection": ["Rest and fluids", "Paracetamol for fever/pain", "Monitor symptoms and seek care if worsening"]
        }
        for disease_name, meds in meds_map.items():
            cur.execute("SELECT disease_id FROM diseases WHERE disease_name=%s", (disease_name,))
            r = cur.fetchone()
            if not r:
                continue
            did = r[0]
            for m in meds:
                m_clean = m.strip()
                cur.execute("SELECT COUNT(*) FROM disease_medications WHERE disease_id=%s AND medication_text=%s", (did, m_clean))
                if cur.fetchone()[0] == 0:
                    cur.execute("INSERT INTO disease_medications (disease_id, medication_text) VALUES (%s, %s)", (did, m_clean))
                
        conn.commit()

    finally:
        cur.close()

# AUTH user
#REGISTRATION
def register_user(conn):
    cur = conn.cursor()
    print("--- Register new user ---")
    name = input("Full name: ").strip()
    email = input("Email (login): ").strip().lower()
    if not name or not email:
        print("Name and email are required.")
        return
    try:
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        print("Registration successful — please login with your email.")
    except mysql.connector.IntegrityError:
        print("That email is already registered.")
    except Exception as e:
        print("Registration failed:", e)
    finally:
        cur.close()

#LOGIN
def login(conn):
    cur = conn.cursor(dictionary=True)
    print("--- Login (email only) ---")
    email = input("Email: ").strip().lower()
    if not email:
        print("Please enter an email to login.")
        return None
    try:
        cur.execute("SELECT user_id AS user_id, name, email FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        if user:
            print(f"Welcome {user['name']}!")
            return user
        print("No account found with that email — please register.")
        return None
    finally:
        cur.close()

# SYMPTOM CHECKER

def list_symptoms(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT symptom_id, symptom_name FROM symptoms ORDER BY symptom_id")
        return cur.fetchall()
    finally:
        cur.close()


def get_medications_for_disease(conn, disease_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT medication_text FROM disease_medications WHERE disease_id=%s", (disease_id,))
        return [r[0] for r in cur.fetchall()]
    finally:
        cur.close()


def diagnose(conn, user_id, selected_symptom_ids):
    cur = conn.cursor()
    try:
        cur.execute("SELECT disease_id, disease_name FROM diseases")
        diseases = cur.fetchall()
        results = []
        for did, dname in diseases:
            cur.execute("SELECT symptom_id FROM disease_symptoms WHERE disease_id=%s", (did,))
            disease_symptom_ids = [r[0] for r in cur.fetchall()]
            if not disease_symptom_ids:
                continue
            match_count = sum(1 for s in selected_symptom_ids if s in disease_symptom_ids)
            percent = (match_count / len(disease_symptom_ids)) * 100
            results.append({'disease_id': did, 'disease_name': dname, 'match_count': match_count, 'total_symptoms': len(disease_symptom_ids), 'percent': percent})
        results.sort(key=lambda x: x['percent'], reverse=True)
        final = []
        for r in results[:TOP_N]:
            r['confidence'] = 'High' if r['match_count'] >= MIN_MATCH else 'Low'
            final.append(r)

        if selected_symptom_ids:
            ph = placeholders(len(selected_symptom_ids))
            cur.execute(f"SELECT symptom_name FROM symptoms WHERE symptom_id IN ({ph})", tuple(selected_symptom_ids))
            symptom_names = [r[0] for r in cur.fetchall()]
        else:
            symptom_names = []
        possible_diseases_str = ', '.join([r['disease_name'] for r in final])
        match_percentages_str = ', '.join([f"{r['disease_name']}:{r['percent']:.1f}%" for r in final])
        query = "INSERT INTO diagnosis_history (user_id, selected_symptoms, possible_diseases, match_percentages) VALUES (%s,%s,%s,%s)"
        data = (user_id, ', '.join(symptom_names), possible_diseases_str, match_percentages_str)
        cur.execute(query, data)
        conn.commit()
        return final
    finally:
        cur.close()

# SUPPORT & HISTORY 

def submit_support(conn, user_id: int, symptoms_text: str, system_suggestions: str):
    cur = conn.cursor()
    try:
        print("\nDescribe why the suggestions were not helpful or what you'd like us to know:")
        note = input().strip()
        que = "INSERT INTO support_requests (user_id, symptoms_text, system_suggestions, user_message) VALUES (%s, %s, %s, %s)"
        dat = (user_id, symptoms_text, system_suggestions, note)
        cur.execute(que, dat)
        conn.commit()
        print("Support request saved. Admins can review it later.")
    finally:
        cur.close()


def view_user_history(conn, user_id: int):
    cur = conn.cursor()
    try:
        qu = """SELECT history_id, selected_symptoms, possible_diseases, match_percentages, date_time
                   FROM diagnosis_history WHERE user_id = %s ORDER BY date_time DESC"""
        cur.execute(qu, (user_id,))
        rows = cur.fetchall()
        if not rows:
            print("No diagnosis history found.")
            return
        for hid, sel_sym, pd, mp, dt in rows:
            print(f"\n[{hid}] {dt}\nSymptoms: {sel_sym}\nSuggestions:{pd}\nScores: {mp}\n")
    finally:
        cur.close()

# MENU

def user_menu(conn, user):
    while True:
        print("\nUser Menu:\n1) Run symptom checker\n2) View my diagnosis history\n3) Submit support request\n4) Logout")
        choice = input("Choice: ").strip()
        if choice == '1':
            symptoms = list_symptoms(conn)
            if not symptoms:
                print("No symptoms in database.")
                continue
            print("\nAvailable symptoms:")
            for sid, sname in symptoms:
                print(f" {sid}. {sname}")
            raw = input("Enter symptom numbers separated by commas (e.g. 1,4,12): ").strip()
            try:
                chosen = [int(x.strip()) for x in raw.split(',') if x.strip()]
            except Exception:
                print("Invalid input — use numbers separated by commas.")
                continue
            if not chosen:
                print("No symptoms chosen.")
                continue
            results = diagnose(conn, user['user_id'], chosen)
            if not results:
                print("No probable conditions found.")
                continue
            print("\nTop suggestions:")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r['disease_name']} — {r['percent']:.1f}% (Matches: {r['match_count']}/{r['total_symptoms']}) [{r['confidence']}]")
                meds = get_medications_for_disease(conn, r['disease_id'])
                if meds:
                    print("   Suggested care:")
                    for m in meds:
                        print(f"    - {m}")
            sat = input("\nSatisfied with suggestions? (y/n): ").strip().lower()
            if sat == 'n':
                cur = conn.cursor()
                try:
                    ph = placeholders(len(chosen))
                    cur.execute(f"SELECT symptom_name FROM symptoms WHERE symptom_id IN ({ph})", tuple(chosen))
                    names = [r[0] for r in cur.fetchall()]
                finally:
                    cur.close()
                suggestions_str = '; '.join([f"{r['disease_name']} ({r['percent']:.1f}%)" for r in results])
                submit_support(conn, user['user_id'], ', '.join(names), suggestions_str)
        elif choice == '2':
            view_user_history(conn, user['user_id'])
        elif choice == '3':
            st = input("Symptoms (text): ").strip()
            sg = input("System suggestions/context (optional): ").strip()
            submit_support(conn, user['user_id'], st, sg)
        elif choice == '4':
            print("Logging out goodbye.")
            break
        else:
            print("Please enter 1, 2, 3 or 4")

# MAIN 

def main():
    conn = connect_db()
    setup_database(conn)
    print("Welcome to the Disease-Prediction-System")
    while True:
        print("\nMain Menu:\n1) Register\n2) Login\n3) Exit")
        choice = input("Choice: ").strip()
        if choice == '1':
            register_user(conn)
        elif choice == '2':
            user = login(conn)
            if user:
                user_menu(conn, user)
        elif choice == '3':
            print("Goodbye — take care.")
            conn.close()
            break
        else:
            print("Please enter 1, 2, or 3.")

if __name__ == '__main__':
    main()
