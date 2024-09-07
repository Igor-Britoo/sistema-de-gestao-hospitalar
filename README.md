# Databases Setup and Population Guide

This repository contains the necessary files to set up and populate databases using Docker and Python. Follow these steps to get everything up and running.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Python**: [Install Python](https://www.python.org/downloads/) (Version 3.6 or higher recommended)
- **pip**: [Install pip](https://pip.pypa.io/en/stable/installation/)
- **virtualenv**: Install it via pip:

  ```bash
  pip install virtualenv
  ```

## Steps to Set Up and Populate the Database

### 1. Clone the Repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/Igor-Britoo/sistema-de-gestao-hospitalar
```

### 2. Navigate to the Repository Directory

Change to the repository directory

```bash
cd sistema-de-gestao-hospitalar
```

### 3. Start the Docker Containers

Run the Docker Compose command to start the database containers in detached mode:

```bash
docker-compose up -d
```

This command will run the containers in the background, initializing your databases.

### 4. Wait for the Databases to Stabilize

Wait approximately 1 minute for the databases to fully initialize and stabilize. This ensures they are ready for use.

### 5. Access the `database_population` Directory

Navigate to the `database_population` directory, where the Python script and requirements file are located:

```bash
cd database_population
```

### 6. Create a Python Virtual Environment

Set up a Python virtual environment to manage project dependencies:

```bash
virtualenv venv
```

### 7. Activate the Virtual Environment

Activate the virtual environment with the following commands:

- **On Windows**:

  ```bash
  venv\Scripts\activate
  ```

- **On macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

### 8. Install Required Python Packages

Install the necessary Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 9. Run the Data Generation Script

Execute the `generate_data.py` script to populate the database:

```bash
python generate_data.py
```