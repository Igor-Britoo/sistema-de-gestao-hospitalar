from faker import Faker
from pymongo import MongoClient
import mysql.connector
from cassandra.cluster import Cluster
from random import randint, choice, sample
from decimal import Decimal
from datetime import datetime, timedelta

list_of_hospitals = [
    "City General Hospital", "St. Mary's Medical Center", "River Valley Hospital", "Greenwood Community Hospital", 
    "Mountainview Health Center", "Lakeside Regional Medical", "Sunrise Children's Hospital", "Maple Grove Hospital", 
    "Hilltop Memorial Hospital", "Seaside General", "Pinecrest Hospital", "Oceanview Medical Center", 
    "Brighton Health Institute", "Silver Oak Hospital", "Grandview Medical Center", "Westside General Hospital", 
    "Riverside Community Hospital", "Blue Ridge Hospital", "Summit Medical Center", "Northside Health System", 
    "South City General", "Eastwood Medical Clinic", "Palm Valley Hospital", "Cedar Hills Medical", 
    "Elmwood General", "Golden Valley Hospital", "Parkview Medical", "Highland Community Hospital", 
    "Central Plains Medical", "Willow Creek Health Center", "Redwood Memorial Hospital", "Meadowbrook Hospital", 
    "Sunset Valley Medical", "Fairview Regional Hospital", "Evergreen Medical Center", "Springfield General", 
    "Canyon Ridge Hospital", "Stonebridge Health Clinic", "Forest Hill Hospital", "Clearwater Medical Center", 
    "Harborview Hospital", "Meadowlands Medical", "Shady Grove Hospital", "Brightwater Medical", 
    "Silverlake Health Center", "Sunnyside General", "Mountain Peak Hospital", "Eagleview Medical Center", 
    "Parklands Hospital", "East River General"
]

list_of_medical_conditions = [
    "Hypertension", "Diabetes", "Asthma", "Chronic Kidney Disease", "Cardiovascular Disease", 
    "Obesity", "Hypothyroidism", "Hyperthyroidism", "Arthritis", "COPD", 
    "Depression", "Anxiety", "Cancer", "HIV/AIDS", "Alzheimer's Disease", 
    "Parkinson's Disease", "Stroke", "Osteoporosis", "Epilepsy", "Liver Cirrhosis", 
    "Multiple Sclerosis", "Anemia", "Tuberculosis", "Cystic Fibrosis", "Sleep Apnea", 
    "Irritable Bowel Syndrome", "Crohn's Disease", "Ulcerative Colitis", "Migraines", "Chronic Fatigue Syndrome", 
    "Glaucoma", "Macular Degeneration", "Endometriosis", "Polycystic Ovary Syndrome", "Fibromyalgia", 
    "Eczema", "Psoriasis", "Lupus", "Sickle Cell Disease", "Hemophilia", 
    "Leukemia", "Lymphoma", "ALS", "Celiac Disease", "Peptic Ulcer", 
    "Bipolar Disorder", "Schizophrenia", "Panic Disorder", "ADHD", "Autism Spectrum Disorder"
]

list_of_allergies = [
    "Peanuts", "Penicillin", "Shellfish", "Pollen", "Latex", 
    "Dairy", "Gluten", "Eggs", "Soy", "Bee Stings", 
    "Tree Nuts", "Dust Mites", "Mold", "Animal Dander", "Wheat", 
    "Sesame", "Corn", "Strawberries", "Bananas", "Kiwi", 
    "Avocado", "Tomatoes", "Citrus Fruits", "Coconut", "Sulfites", 
    "Nickel", "Fragrance", "Iodine", "NSAIDs", "Aspirin", 
    "Codeine", "Sulfa Drugs", "Amoxicillin", "Lactose", "Detergents", 
    "Hair Dyes", "Sunlight (Photosensitivity)", "Perfume", "Insect Bites", "Chocolate", 
    "Red Meat", "Alcohol", "Barley", "Fish", "Mustard", 
    "Artificial Sweeteners", "Food Additives", "Pine Nuts", "Shellac", "Preservatives"
]

list_of_medications = [
    "Metformin", "Lisinopril", "Albuterol", "Aspirin", "Atorvastatin", 
    "Levothyroxine", "Metoprolol", "Omeprazole", "Simvastatin", "Prednisone", 
    "Warfarin", "Insulin", "Ibuprofen", "Gabapentin", "Citalopram", 
    "Amlodipine", "Furosemide", "Hydrochlorothiazide", "Losartan", "Clopidogrel", 
    "Sertraline", "Amoxicillin", "Azithromycin", "Hydrocodone", "Oxycodone", 
    "Doxycycline", "Paracetamol", "Tramadol", "Alprazolam", "Lorazepam", 
    "Diazepam", "Fluoxetine", "Bupropion", "Montelukast", "Allopurinol", 
    "Carvedilol", "Crestor", "Pantoprazole", "Lantus", "Humalog", 
    "Januvia", "Xarelto", "Eliquis", "Advair", "Symbicort", 
    "Zoloft", "Propranolol", "Ranitidine", "Cymbalta", "Plavix"
]

list_of_patient_critical_alerts = [
    "Severe allergic reaction to penicillin", "History of heart attacks", "Chronic renal failure", 
    "Immunocompromised", "Recent surgery", "Uncontrolled diabetes", "History of stroke", 
    "Pacemaker", "Severe asthma", "Late-stage cancer", "Severe anemia", "Liver transplant recipient", 
    "Dialysis-dependent", "High risk of blood clots", "Severe dehydration", "Extreme hypertension", 
    "History of seizures", "Severe psychiatric instability", "Advanced osteoporosis", 
    "Severe drug interaction risk", "Pregnancy", "Unstable angina", "Recent organ transplant", 
    "Hemorrhaging risk", "HIV positive", "History of severe infection", "Ongoing chemotherapy", 
    "Complicated pregnancy", "Extreme malnutrition", "Mental health crisis", "Severe bleeding disorder", 
    "Allergic to anesthesia", "Heart failure risk", "Imminent labor", "Severe hypoglycemia", 
    "High fever", "Uncontrolled thyroid condition", "Life-threatening sepsis", "COVID-19 positive", 
    "Extreme fatigue", "Dangerously high cholesterol", "Kidney stone history", "Transplant rejection risk", 
    "Malignant hypertension", "Severe electrolyte imbalance", "Abnormal heart rhythm", 
    "Blood transfusion needed", "Major infection", "Decreased oxygen saturation", "Trauma injury"
]

list_of_insurance_providers = ["Blue Cross", "UnitedHealthcare", "Aetna", "Cigna", "Medicare"]

list_of_exam_names = [
    "Complete Blood Count", "X-ray", "MRI Scan", "Liver Function Test", "Electrocardiogram", 
    "Urinalysis", "Thyroid Function Test", "CT Scan", "Cardiac Stress Test", "Chest X-ray", 
    "Colonoscopy", "Endoscopy", "Bone Density Scan", "Pap Smear", "Mammogram", 
    "PSA Test", "Lipids Panel", "Fasting Blood Glucose", "Hemoglobin A1C", "EKG", 
    "Pulmonary Function Test", "Kidney Function Test", "Lung Biopsy", "Liver Biopsy", "CT Angiogram", 
    "DEXA Scan", "Abdominal Ultrasound", "Renal Ultrasound", "Pelvic Ultrasound", "Skin Biopsy", 
    "Liver Enzymes Test", "C-Reactive Protein Test", "Bilirubin Test", "Hepatitis Panel", "HIV Test", 
    "STD Panel", "Holter Monitor", "Echocardiogram", "Ankle-Brachial Index", "Sleep Study", 
    "Cervical Screening", "EEG", "Ophthalmology Exam", "Glucose Tolerance Test", "Allergy Skin Test", 
    "Spirometry", "Blood Urea Nitrogen", "Creatinine Test", "Calcium Test", "Blood Gas Test"
]

list_of_patient_prescriptions = [
    "Metformin 500mg daily", "Lisinopril 10mg daily", "Albuterol inhaler as needed", 
    "Atorvastatin 20mg daily", "Levothyroxine 75mcg daily", "Metoprolol 50mg twice daily", 
    "Omeprazole 20mg daily", "Prednisone 5mg daily", "Gabapentin 300mg three times daily", 
    "Insulin injection before meals", "Citalopram 20mg daily", "Losartan 50mg daily", 
    "Clopidogrel 75mg daily", "Ibuprofen 400mg as needed", "Sertraline 50mg daily", 
    "Amoxicillin 500mg three times daily", "Oxycodone 10mg as needed for pain", 
    "Doxycycline 100mg twice daily", "Montelukast 10mg daily", "Allopurinol 100mg daily", 
    "Bupropion 150mg twice daily", "Aspirin 81mg daily", "Furosemide 40mg daily", 
    "Carvedilol 12.5mg twice daily", "Pantoprazole 40mg daily", "Symbicort inhaler twice daily", 
    "Xarelto 20mg daily", "Eliquis 5mg twice daily", "Advair Diskus twice daily", 
    "Plavix 75mg daily", "Zoloft 50mg daily", "Ranitidine 150mg twice daily", 
    "Lantus insulin at bedtime", "Januvia 100mg daily", "Propranolol 40mg daily", 
    "Tramadol 50mg as needed", "Lorazepam 1mg as needed", "Alprazolam 0.5mg as needed", 
    "Diazepam 5mg as needed", "Fluoxetine 20mg daily", "Cymbalta 60mg daily", 
    "Hydrochlorothiazide 25mg daily", "Simvastatin 20mg daily", "Folic Acid 1mg daily", 
    "Vitamin D 2000 IU daily", "Iron supplement 325mg daily", "Zinc supplement 50mg daily", 
    "Calcium supplement 1200mg daily", "Melatonin 5mg at bedtime"
]


fake = Faker()

def configure_mongodb():
    client = MongoClient('mongodb://root:example@localhost:27017/')
    db = client['hospital_management']
    return db

def configure_cassandra():
    cassandra_cluster = Cluster(['localhost'])
    cassandra_session = cassandra_cluster.connect()

    # Create keyspace and tables for Cassandra
    cassandra_session.execute("""
    CREATE KEYSPACE IF NOT EXISTS hospital_management WITH replication = {
        'class': 'SimpleStrategy', 'replication_factor': '1'
    }
    """)
    cassandra_session.set_keyspace("hospital_management")

    cassandra_session.execute("""
    CREATE TABLE IF NOT EXISTS patient_admission (
        cpf text PRIMARY KEY,
        date_of_admission date,
        discharge_date date,
        doctor text,
        crm text,
        hospital text,
        room_number smallint,
        admission_type text
    )
    """)

    cassandra_session.execute("""
    CREATE TABLE IF NOT EXISTS exams_prescriptions (
        cpf text PRIMARY KEY,
        exams map<timestamp, text>,
        prescriptions map<timestamp, text>
    )
    """)

    return cassandra_cluster, cassandra_session

def configure_mysql():
    mysql_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="example",
        database="hospital_management"
    )
    mysql_cursor = mysql_conn.cursor()

    mysql_cursor.execute("""
    CREATE TABLE IF NOT EXISTS financial_info (
        cpf VARCHAR(11) PRIMARY KEY,
        insurance_provider VARCHAR(255),
        billing_amount DECIMAL(10, 2)
    )
    """)

    return mysql_conn, mysql_cursor

def generate_data(n, mysql_cursor, mysql_conn, cassandra_session, mongo_db):
    # MongoDB Collections
    patient_collection = mongo_db['patients']
    doctors_list = []

    for _ in range(n/4):
        new_doctor = {
            'name': fake.name(),
            'crm': str(fake.random_number(digits=8))
        }
        doctors_list.append(new_doctor)
        print(new_doctor, '\n')
    
    print('================================================================\n')

    for _ in range(n):
        # MongoDB (via pymongo)
        patient = {
            'name': fake.name(),
            'cpf': str(fake.unique.random_number(digits=11, fix_len=True)),
            'age': randint(20, 80),
            'gender': choice(['M', 'F']),
            'blood_type': choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
            'allergies': sample(list_of_allergies, randint(0, 3)),
            'medication': sample(list_of_medications, randint(0, 5)),
            'critical_alerts': [
                {
                    'alert_type': choice(list_of_patient_critical_alerts),
                    'description': fake.sentence(nb_words=6),
                    'date': fake.date_this_decade()
                } for _ in range(randint(0, 2))
            ],
            'last_consultation_date': fake.date_this_year()
        }

        # Add medical condition to patient
        if randint(0, 1) == 1:
           patient['medical_condition'] =  choice(list_of_medical_conditions)

        # Convert date fields to datetime
        patient['last_consultation_date'] = patient['last_consultation_date'].strftime('%Y-%m-%d')
        for alert in patient['critical_alerts']:
            alert['date'] = alert['date'].strftime('%Y-%m-%d')

        patient_collection.insert_one(patient)

        # Print MongoDB Data
        print(f"MongoDB Patient Data: {patient}\n")

        # Cassandra - Patient Admission
        doctor = choice(doctors_list)
        date_of_admission = fake.date_this_year().strftime('%Y-%m-%d')
        discharge_date = (datetime.strptime(date_of_admission, '%Y-%m-%d') + timedelta(days=randint(1, 15))).strftime('%Y-%m-%d')
        doctor_name = doctor['name']
        doctor_crm = doctor['crm']
        hospital_name = choice(list_of_hospitals)
        room_number = fake.random_number(digits=3)
        admission_type = choice(['Emergency', 'Elective Surgery', 'Observation'])

        cassandra_session.execute("""
        INSERT INTO patient_admission (cpf, date_of_admission, discharge_date, doctor, crm, hospital, room_number, admission_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            patient['cpf'],
            date_of_admission,
            discharge_date,
            doctor_name,
            doctor_crm,
            hospital_name,
            room_number,
            admission_type
        ))

        # Print Cassandra Data
        print(f"Cassandra Patient Admission Data: "
              f"{{'cpf': {patient['cpf']}, 'date_of_admission': {date_of_admission}, 'discharge_date': {discharge_date}, "
              f"'doctor': {doctor_name}, 'crm': {doctor_crm}, 'hospital': {hospital_name}, "
              f"'room_number': {room_number}, 'admission_type': {admission_type}}}\n")
        
        # Cassandra - Exams and Prescriptions
        exams = {
            fake.date_time_this_year(): f"{choice(list_of_exam_names)}: {fake.sentence(nb_words=10)}"
            for _ in range(randint(1, 5))
        }

        prescriptions = {
            fake.date_time_this_year(): choice(list_of_patient_prescriptions)
            for _ in range(randint(1, 5))
        }

        cassandra_session.execute("""
        INSERT INTO exams_prescriptions (cpf, exams, prescriptions)
        VALUES (%s, %s, %s)
        """, (patient['cpf'], exams, prescriptions))

        # Print Cassandra Exams and Prescriptions Data
        print(f"Cassandra Exams and Prescriptions Data: "
              f"{{'cpf': {patient['cpf']}, 'exams': {exams}, 'prescriptions': {prescriptions}}}\n")

        # MySQL - Financial Info
        patient_insurance_provider = choice(list_of_insurance_providers)
        patient_billing_amount = Decimal(randint(1000, 50000))

        mysql_cursor.execute("""
        INSERT INTO financial_info (cpf, insurance_provider, billing_amount)
        VALUES (%s, %s, %s)
        """, (
            patient['cpf'],
            patient_insurance_provider,
            patient_billing_amount
        ))

        # Print MySQL Data
        print(f"MySQL Financial Info Data: {{'cpf': {patient['cpf']}, 'insurance_provider': {patient_insurance_provider}, 'billing_amount': {patient_billing_amount}}}\n")
        print('================================================================\n')

    mysql_conn.commit()

# Configure MongoDB
mongo_db = configure_mongodb()

# Configure Cassandra
cassandra_cluster, cassandra_session = configure_cassandra()

# Configure MySQL
mysql_conn, mysql_cursor = configure_mysql()

# Generate and Insert Data
generate_data(10, mysql_cursor, mysql_conn, cassandra_session, mongo_db)

# Close connections
mysql_cursor.close()
mysql_conn.close()
cassandra_cluster.shutdown()
