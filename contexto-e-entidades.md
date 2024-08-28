### **Minimundo de Gestão Hospitalar**

**Contextualização:**

O sistema de gestão hospitalar foi desenvolvido para gerenciar eficientemente as informações de pacientes, consultas, internações, exames, prescrições e condições críticas. Utilizando uma abordagem de persistência poliglota, o sistema armazena diferentes tipos de dados em diferentes bancos de dados, garantindo desempenho e escalabilidade. O MongoDB é usado para armazenar dados médicos detalhados, Cassandra para gerenciar informações de internação e consultas, e MySQL para informações financeiras.

**Entidades:**

1. **Paciente (Patient)**
   - **ID:** Identificador único no sistema.
   - **Nome:** Nome completo do paciente.
   - **CPF:** Cadastro de Pessoa Física, único e utilizado como chave para relacionar informações em diferentes bancos de dados.
   - **Idade:** Idade do paciente.
   - **Gênero:** Gênero do paciente.
   - **Tipo Sanguíneo:** Tipo sanguíneo do paciente.
   - **Condição Médica:** Condições médicas atuais do paciente.
   - **Alergias:** Lista de alergias que o paciente possui.
   - **Medicação:** Lista de medicações que o paciente está tomando.
   - **Alertas Críticos:** Alertas médicos críticos, como reações alérgicas graves ou condições que requerem atenção imediata.
   - **Data da Última Consulta:** Data da última consulta do paciente.

2. **Internação (Patient_Admission)**
   - **CPF:** Cadastro de Pessoa Física, utilizado como chave primária.
   - **Data de Admissão:** Data em que o paciente foi internado.
   - **Data de Alta:** Data em que o paciente recebeu alta.
   - **Médico:** Nome do médico responsável pela internação.
   - **CRM:** Registro no Conselho Regional de Medicina do médico.
   - **Hospital:** Nome do hospital onde a internação ocorreu.
   - **Número do Quarto:** Número do quarto onde o paciente está internado.
   - **Tipo de Admissão:** Tipo de admissão, como emergência, cirurgia eletiva, etc.

3. **Exames e Prescrições (Exams and Prescriptions)**
   - **CPF:** Cadastro de Pessoa Física, utilizado como chave primária.
   - **Exames:** Mapa de exames realizados, com a data e a descrição do exame.
   - **Prescrições:** Mapa de prescrições médicas, com a data e a descrição da prescrição.

4. **Informações Financeiras (Financial_Info)**
   - **CPF:** Cadastro de Pessoa Física, utilizado como chave primária.
   - **Provedor de Seguro:** Nome da seguradora do paciente.
   - **Valor da Fatura:** Valor cobrado pela internação ou consulta.

**Cenário Operacional:**

1. **Cadastro de Pacientes:** Ao ser admitido no hospital, o paciente tem seus dados básicos cadastrados no sistema, incluindo informações pessoais e de saúde. Esses dados são armazenados no MongoDB para permitir a fácil consulta e atualização.

2. **Internações e Consultas:** Quando o paciente é internado ou realiza uma consulta, os dados da internação, como datas, médico responsável e hospital, são registrados no Cassandra, que permite consultas rápidas e escaláveis. Informações sobre exames e prescrições são armazenadas no mesmo banco de dados, garantindo que o histórico médico do paciente esteja sempre acessível.

3. **Gestão Financeira:** As informações financeiras, como o valor das faturas e o provedor de seguro, são armazenadas no MySQL. Isso permite a integração com sistemas de faturamento e relatórios financeiros.

4. **Alertas Críticos e Monitoramento:** O sistema envia alertas críticos para os profissionais de saúde com base nas informações médicas armazenadas no MongoDB. Isso pode incluir alertas sobre alergias graves ou condições médicas que requerem atenção imediata.

**Vantagens da Persistência Poliglota:**

- **Desempenho:** Utilizar Cassandra para as informações de internação e consultas permite uma escalabilidade horizontal eficiente, garantindo que o sistema possa lidar com grandes volumes de dados sem perda de desempenho.
- **Flexibilidade:** MongoDB permite o armazenamento de dados médicos complexos e semi-estruturados, como alertas críticos e registros de medicação, sem a necessidade de um esquema fixo.
- **Confiabilidade Financeira:** Manter as informações financeiras no MySQL garante integridade referencial e facilidade na integração com sistemas financeiros existentes.