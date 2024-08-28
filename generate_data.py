from faker import Faker
from mongoengine import connect, Document, StringField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField, DateField
from cassandra.cluster import Cluster
import mysql.connector
from random import randint, choice
from decimal import Decimal
from datetime import datetime, timedelta

fake = Faker()

# MongoDB Configuration with MongoEngine
connect('hospital_management', host='localhost', port=27017)

class CriticalAlert(EmbeddedDocument):
    alert_type = StringField(required=True)
    description = StringField()
    date = DateField()

class Patient(Document):
    name = StringField(required=True)
    cpf = StringField(required=True, unique=True)
    age = IntField()
    gender = StringField()
    blood_type = StringField()
    medical_condition = StringField()
    allergies = ListField(StringField())
    medication = ListField(StringField())
    critical_alerts = ListField(EmbeddedDocumentField(CriticalAlert))
    last_consultation_date = DateField()

# Cassandra Configuration
cassandra_cluster = Cluster(['localhost'])
cassandra_session = cassandra_cluster.connect()
cassandra_session.execute("""
CREATE KEYSPACE IF NOT EXISTS hospital_management WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': '1'
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
    room_number text,
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

# MySQL Configuration
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
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

# Generate and Insert Data
def generate_data(n):
    for _ in range(n):
        # MongoDB (via MongoEngine)
        patient = Patient(
            name=fake.name(),
            cpf=fake.unique.random_number(digits=11, fix_len=True),
            age=randint(20, 80),
            gender=choice(['M', 'F']),
            blood_type=choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
            medical_condition=fake.sentence(nb_words=5),
            allergies=[fake.word() for _ in range(randint(0, 3))],
            medication=[fake.word() for _ in range(randint(0, 5))],
            critical_alerts=[
                CriticalAlert(alert_type=fake.word(), description=fake.sentence(), date=fake.date_this_decade())
                for _ in range(randint(0, 2))
            ],
            last_consultation_date=fake.date_this_year()
        )
        patient.save()

        # Cassandra
        date_of_admission = fake.date_this_year()
        discharge_date = date_of_admission + timedelta(days=randint(1, 15))

        cassandra_session.execute("""
        INSERT INTO patient_admission (cpf, date_of_admission, discharge_date, doctor, crm, hospital, room_number, admission_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            patient.cpf,
            date_of_admission,
            discharge_date,
            fake.name(),
            fake.random_number(digits=8),
            fake.company(),
            fake.random_number(digits=3),
            choice(['Emergency', 'Elective Surgery', 'Observation'])
        ))

        exams = {fake.date_time_this_year(): fake.sentence(nb_words=5) for _ in range(randint(1, 5))}
        prescriptions = {fake.date_time_this_year(): fake.sentence(nb_words=3) for _ in range(randint(1, 5))}

        cassandra_session.execute("""
        INSERT INTO exams_prescriptions (cpf, exams, prescriptions)
        VALUES (%s, %s, %s)
        """, (patient.cpf, exams, prescriptions))

        # MySQL
        mysql_cursor.execute("""
        INSERT INTO financial_info (cpf, insurance_provider, billing_amount)
        VALUES (%s, %s, %s)
        """, (
            patient.cpf,
            fake.company(),
            Decimal(randint(1000, 50000))
        ))

    mysql_conn.commit()

# Generate 100 records
generate_data(100)

# Close connections
mysql_cursor.close()
mysql_conn.close()
cassandra_cluster.shutdown()
