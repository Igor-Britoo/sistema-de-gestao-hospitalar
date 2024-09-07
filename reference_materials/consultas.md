### **Consultas no MongoDB (Informações Médicas e Pessoais dos Pacientes)**

1. **Buscar o perfil completo de um paciente pelo CPF:**
   ```python
   patient = Patient.objects(cpf="12345678901").first()
   ```

2. **Listar pacientes por grupo sanguíneo:**
   ```python
   patients = Patient.objects(blood_type="O+")
   ```

3. **Buscar pacientes com um histórico de determinada condição médica:**
   ```python
   patients = Patient.objects(medical_condition__icontains="hipertensão")
   ```

4. **Listar pacientes que têm alergias múltiplas:**
   ```python
   patients = Patient.objects(__raw__={"$where": "this.allergies.length > 1"})
   ```

5. **Identificar pacientes que não tiveram consulta nos últimos 6 meses:**
   ```python
   from datetime import datetime, timedelta

   no_recent_consultations = Patient.objects(last_consultation_date__lte=datetime.now() - timedelta(days=180))
   ```

### **Consultas no Cassandra (Histórico de Internações, Exames e Prescrições dos Pacientes)**

1. **Obter o histórico completo de internações de um paciente:**
   ```cql
   SELECT * FROM patient_admission WHERE cpf = '12345678901';
   ```

2. **Buscar exames realizados por um paciente em uma data específica:**
   ```cql
   SELECT exams FROM exams_prescriptions WHERE cpf = '12345678901' AND exams CONTAINS KEY '2024-08-01';
   ```

3. **Consultar prescrições emitidas para um paciente nos últimos 3 meses:**
   ```cql
   SELECT prescriptions FROM exams_prescriptions WHERE cpf = '12345678901';
   ```

4. **Listar pacientes internados em um período específico:**
   ```cql
   SELECT * FROM patient_admission WHERE date_of_admission >= '2024-01-01' AND date_of_admission <= '2024-03-31';
   ```

5. **Identificar internações repetidas para um paciente (mais de uma internação):**
   ```cql
   SELECT COUNT(*) FROM patient_admission WHERE cpf = '12345678901';
   ```

### **Consultas no MySQL (Informações Financeiras dos Pacientes)**

1. **Verificar se um paciente está associado a um provedor de seguro específico:**
   ```sql
   SELECT * FROM financial_info WHERE cpf = '12345678901' AND insurance_provider = 'Health Insurance Co';
   ```

2. **Consultar o total faturado para um paciente específico:**
   ```sql
   SELECT billing_amount FROM financial_info WHERE cpf = '12345678901';
   ```

3. **Identificar pacientes com faturas acima de um determinado valor:**
   ```sql
   SELECT * FROM financial_info WHERE billing_amount > 5000;
   ```

4. **Listar todos os pacientes com provedor de seguro X e fatura acima de Y:**
   ```sql
   SELECT * FROM financial_info WHERE insurance_provider = 'Health Insurance Co' AND billing_amount > 10000;
   ```

5. **Consultar a média dos valores faturados para um grupo de pacientes:**
   ```sql
   SELECT AVG(billing_amount) FROM financial_info WHERE insurance_provider = 'Health Insurance Co';
   ```

### **Consultas Combinadas (Foco no Paciente)**

1. **Obter todas as informações (médicas, de internação, exames, prescrições, financeiras) de um paciente:**
   - **MongoDB:** Buscar informações médicas e pessoais.
   - **Cassandra:** Buscar histórico de internações, exames e prescrições.
   - **MySQL:** Buscar informações financeiras.

   Exemplo de pseudocódigo:
   ```python
   patient_info = {
       "medical_info": Patient.objects(cpf="12345678901").first(),
       "admission_info": cassandra_session.execute("SELECT * FROM patient_admission WHERE cpf = %s", ('12345678901',)).one(),
       "exam_prescriptions": cassandra_session.execute("SELECT * FROM exams_prescriptions WHERE cpf = %s", ('12345678901',)).one(),
       "financial_info": mysql_cursor.execute("SELECT * FROM financial_info WHERE cpf = %s", ('12345678901',)).fetchone()
   }
   ```

2. **Identificar pacientes com condições médicas críticas que necessitaram de internações recentes:**
   - **MongoDB:** Filtrar pacientes com condições críticas.
   - **Cassandra:** Verificar internações nos últimos 6 meses.

   Exemplo de pseudocódigo:
   ```python
   critical_patients = Patient.objects(medical_condition__icontains="crítico")
   recent_admissions = []
   for patient in critical_patients:
       admission = cassandra_session.execute("SELECT * FROM patient_admission WHERE cpf = %s AND date_of_admission >= %s", (patient.cpf, datetime.now() - timedelta(days=180))).one()
       if admission:
           recent_admissions.append((patient, admission))
   ```

3. **Listar pacientes com alto custo de faturamento que realizaram muitos exames nos últimos 6 meses:**
   - **MySQL:** Filtrar pacientes com alto faturamento.
   - **Cassandra:** Verificar a quantidade de exames realizados.

   Exemplo de pseudocódigo:
   ```python
   high_billing_patients = mysql_cursor.execute("SELECT cpf FROM financial_info WHERE billing_amount > %s", (10000,)).fetchall()
   frequent_exam_patients = []
   for patient in high_billing_patients:
       exam_count = cassandra_session.execute("SELECT COUNT(*) FROM exams_prescriptions WHERE cpf = %s AND exams CONTAINS KEY >= %s", (patient[0], datetime.now() - timedelta(days=180))).one()
       if exam_count > 5:
           frequent_exam_patients.append(patient[0])
   ```

4. **Consultar pacientes com histórico de internações e alta frequência de alertas críticos:**
   - **MongoDB:** Filtrar pacientes com alertas críticos frequentes.
   - **Cassandra:** Verificar histórico de internações.

   Exemplo de pseudocódigo:
   ```python
   critical_alert_patients = Patient.objects(__raw__={"$where": "this.critical_alerts.length > 3"})
   frequent_admissions = []
   for patient in critical_alert_patients:
       admissions = cassandra_session.execute("SELECT COUNT(*) FROM patient_admission WHERE cpf = %s", (patient.cpf,)).one()
       if admissions > 2:
           frequent_admissions.append((patient, admissions))
   ```

Essas consultas ajudam a analisar a saúde e o histórico financeiro dos pacientes, fornecendo uma visão abrangente e integrada que considera todas as facetas do atendimento hospitalar.