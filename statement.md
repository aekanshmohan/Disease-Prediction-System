# Disease Prediction System

## 1. Problem Statement

The increasing accessibility of digital tools has created opportunities to support individuals in understanding basic health conditions. However, many existing solutions depend heavily on internet connectivity, machine learning models, or complex user interfaces. These limitations make them less suitable for academic learning environments or offline usage.

The **Disease Prediction System** aims to address this by providing a simple, transparent, rule-based diagnostic assistant. The system predicts possible diseases based on user-selected symptoms and helps users understand their health condition using clear, predefined logic. The solution avoids machine learning complexity and focuses on fundamental algorithmic reasoning.

---

## 2. Scope of the Project

1. The project focuses on predicting diseases solely based on symptom–disease mappings stored in a database.
2. The system allows users to register, log in, select symptoms, and receive disease predictions.
3. The system supports offline usage and relies only on a local MySQL database.
4. Diagnosis history and support requests are stored persistently.
5. The system does **not** include real-time medical diagnosis, clinical validation, or any form of machine learning.
6. This solution is intended strictly for educational and demonstration purposes.

---

## 3. Target Users

1. **Healthcare Professionals**

   * Individuals in the medical field who want a quick, offline tool to analyze symptoms.
   * Useful for educational demonstrations, training, or quick rule-based reference.

2. **General Public**

   * Anyone who wants to understand potential medical conditions based on symptoms.
   * Helpful for gaining awareness before seeking professional medical advice.

3. **Students and Educators**

   * Suitable for academic learning in health informatics, databases, or rule-based expert systems.

4. **Developers and Researchers**

   * Useful for those exploring simple diagnostic systems or working on prototype medical tools.

*Note:* This project is not intended for real medical decision-making.* This project is not intended for real medical decision-making.

---

## 4. High-Level Features

1. **Email-Based User Registration and Login**

   * Simple onboarding without passwords.

2. **Symptom Selection Interface**

   * Comprehensive list of symptoms stored in the database.
   * User selects multiple symptoms using numeric IDs.

3. **Rule-Based Disease Prediction**

   * Compares user symptoms with disease profiles.
   * Generates top three most probable diseases.
   * Displays match percentage and confidence scores.

4. **Medication and Care Suggestions**

   * Provides general non-prescription guidance.

5. **Diagnosis History Storage**

   * Stores all past predictions for each user.
   * Easy retrieval for review.

6. **Support Request Logging**

   * Users can submit feedback if predictions seem inaccurate.

7. **Offline and Database-Driven Operation**

   * No internet required.
   * Fully functional using a local MySQL database.

---

