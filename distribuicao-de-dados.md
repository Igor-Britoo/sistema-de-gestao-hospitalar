### **MongoDB: Data Types**

**Patient ID:** `ObjectId` (Primary Key)  
**Name:** `String`  
**CPF:** `String` (set as unique and indexed)  
**Age:** `Integer`  
**Gender:** `String`  
**Blood Type:** `String`  
**Medical Condition:** `String`  
**Allergies:** `Array` of `String`  
**Medication:** `Array` of `String`  
**Critical Alerts:** `Array` of `Document` (e.g., `{ alertType, description, date }`)  
**Last Consultation Date:** `Date`

### **MySQL: Data Types (Apenas Informações Financeiras)**

**Tabela: Financial_Info**

- **CPF:** `VARCHAR(11)` (Primary Key)
- **Insurance_Provider:** `VARCHAR(255)`
- **Billing Amount:** `DECIMAL(10, 2)`

### **Cassandra: Data Types**

**Tabela: Patient_Admission**

- **CPF:** `text` (Primary Key)
- **Date_of_Admission:** `date`
- **Discharge_Date:** `date`
- **Doctor:** `text`
- **CRM:** `text`
- **Hospital:** `text`
- **Room_Number:** `text`
- **Admission_Type:** `text`
