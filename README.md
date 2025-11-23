# Disease-Prediction-System
Overview  
  The Disease Prediction System is a rule-based medical diagnosis application developed using Python and MySQL.
  Users enter symptoms, and the system predicts the top three most likely diseases based on predefined symptom–disease         mappings. 
  
Features
 1. User Management  
  Email-only registration  
  Email-only login  
  No password requirement for simplicity  

 2. Symptom Checker  
  Users can select symptoms from a detailed list  
  The system compares user-selected symptoms with disease profiles  
  The system produces:  
    1. Top 3 disease predictions       
    2. Symptom match percentage  
    3. Confidence level (High or Low)  
    4. General care and medication suggestions  
    
 3. Diagnosis History  
  Stores all past diagnoses  
  Displays clean, readable history entries  
  Preserves data across sessions  

 4. Support Request System  
  Users can submit feedback or request help  
  Support requests are saved in the database  

 5. Database-Driven and Offline  
  All data stored in MySQL  
  No internet connection required  
  Automatic setup of tables and inputs data  

 6. Transparent Rule-Based Logic  
  No machine learning  
  Easy to understand  
  Easy to modify  

Technologies Used  

 Python 3  
 MySQL  
 mysql-connector-python library  
 Command-Line Interface    
 Works on Windows, macOS, and Linux  
 
Steps to Install & Run the Project 

  -Install Python and Required Packages:   
   1. Ensure Python 3 is installed on your system.  
   2. Open a terminal or command prompt.  
   3. Install the required Python package using:  
      pip install mysql-connector-python  

-Install and Configure MySQL:  
  1. Install MySQL Server on your system  
  2. Open the MySQL client or MySQL Workbench.  
  3. Create a new database using:  
     CREATE DATABASE "databasename";    
  Run the Application: python disease_prediction_system.py  
  The app becomes ready for use immediately

Testing Instructions  
 1. Register a User  
  .Select “Register” in the main menu  
  .Enter your full name and email  

2. Login  
 .Enter the registered email  
 .Access the user dashboard  

3. Run the Symptom Checker  
 .Select symptoms by entering their numeric IDs  
  .Review:  
  Predicted diseases  
  Match percentages  
  Medication suggestions  

4. View Diagnosis History  
  .Select “View my diagnosis history”  
  .Verify that your recent diagnosis is displayed  

5. Submit Support Request  
 .Select “Submit support request”  
 .Enter a short message describing your issue  

6. Re-run the Application  
  .Restart the script  
  .Confirm that:  
  No duplicate medications appear  
  History is preserved  
  Symptoms do not duplicate  
  User login remains functional  
 
