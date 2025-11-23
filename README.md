# Disease-Prediction-System

## Overview

The Disease Prediction System is a rule-based medical diagnosis application developed using Python and MySQL. Users enter symptoms, and the system predicts the top three most likely diseases based on predefined symptom–disease mappings.



## Features

### User Management

* Email-only registration
* Email-only login
* No password requirement for simplicity

### Symptom Checker

* Users can select symptoms from a detailed list
* The system compares user-selected symptoms with disease profiles
* The system produces:

  * Top 3 disease predictions
  * Symptom match percentage
  * Confidence level (High or Low)
  * General care and medication suggestions

### Diagnosis History

* Stores all past diagnoses
* Displays clean, readable history entries
* Preserves data across sessions

### Support Request System

* Users can submit feedback or request help
* Support requests are saved in the database

### Database-Driven and Offline

* All data stored in MySQL
* No internet connection required
* Automatic setup of tables and inputs data

### Transparent Rule-Based Logic

* No machine learning
* Easy to understand
* Easy to modify



## Technologies Used

* Python 3
* MySQL
* mysql-connector-python library
* Command-Line Interface
* Works on Windows, macOS, and Linux



## Steps to Install & Run the Project

### Install Python and Required Packages

1. Ensure Python 3 is installed on your system.
2. Open a terminal or command prompt.
3. Install the required Python package using:

   bash
   pip install mysql-connector-python
   

### Install and Configure MySQL

1. Install MySQL Server on your system
2. Open the MySQL client or MySQL Workbench
3. Create a new database using:

   CREATE DATABASE "databasename";
   

### Run the Application

To run the application, :


python disease_prediction_system.py


The app becomes ready for use immediately.



## Testing Instructions

### Register a User

* Select “Register” in the main menu
* Enter your full name and email

### Login

* Enter the registered email
* Access the user dashboard

### Run the Symptom Checker

* Select symptoms by entering their numeric IDs
* Review:

  * Predicted diseases
  * Match percentages
  * Medication suggestions

### View Diagnosis History

* Select “View my diagnosis history”
* Verify that your recent diagnosis is displayed

### Submit Support Request

* Select “Submit support request”
* Enter a short message describing your issue

### Re-run the Application

Restart the script and confirm that:

* No duplicate medications appear
* History is preserved
* Symptoms do not duplicate
* User login remains functional

