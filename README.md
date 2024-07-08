# Automated Email Notification

This Python script is designed to automate the process of fetching data from a database, checking last_upload_time of each case, and then emailing customer to update the report.

## Overview

The script performs the following steps:
1. Connects to a MySQL database.
2. Executes a predefined SQL query to extract specific data.
3. Notify clients to update reports via emails.

## Setup

1. **Database Configuration:**
   - Configure your database connection parameters in the `config.ini` file.

2. **Email Settings:**
   - Configure your email settings in the `config.ini` file.

3. **Dependencies:**
   - Install the required Python libraries using pip:
     ```
     pip install pandas pymysql configparser
     ```

4. **Google API Credentials:**
   - Step 1: Enable the Gmail API
        Go to the Google Developers Console.
        Create a new project.
        Navigate to “API & Services” > “Dashboard”.
        Click “ENABLE APIS AND SERVICES”.
        Search for “Gmail API”, select it, and click “Enable”.
   - Step 2: Create Credentials
        On the Gmail API page, go to “Credentials”.
        Click “Create credentials” and choose “OAuth client ID”.
        If prompted, configure the consent screen by entering the necessary information. For testing purposes, you can select "External" and fill in the required fields. Remember to add your email as a test user.
        Select the application type as “Desktop app” and give it a name.
        Click “Create”, and you will receive your client ID and client secret. Save these.
        Save the `credentials.json` file in the project directory.
   - Step 3: Install Required Libraries
        Install the required libraries with pip:
        ```pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
        ```


## Configuration File Format

The `config.ini` file should have the following format:

```ini
[ssh_tunnel]
ssh_host = 52.204.162.192
ssh_port = 22
ssh_username = openvpnas
ssh_pem_key = "replace with your ssh_pem_key path"

[database]
db_host = bl-venture-rds-production-replica.calntbnktffy.us-east-1.rds.amazonaws.com
db_port = 3306
db_user = "replace with your username"
db_password = "replace with your db password"


[email]
my_email = "replace with your email"
my_password = "replace with your email password"


## send email. 
use send2.py to send email. So that people in the same org will be put in the same email as recepients.

