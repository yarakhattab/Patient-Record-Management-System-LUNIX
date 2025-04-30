## 🏥 Patient Record Management System 🩺
This project implements a Patient Record Management System that allows healthcare professionals to efficiently store, manage, and retrieve medical test data. The system supports various operations such as adding new records, updating existing ones, validating patient information, and more.

## 🎯 Features
📋 Medical Test Records Management: Add, update, and manage patient test records.

🩺 Test Definition Management: Load, update, and save test definitions (range, unit, and turnaround time).

🛠️ Validation: All inputs are validated to ensure correct formats and data integrity.

📊 Filtering: Filter records based on criteria like Patient ID, Test Name, Test Status, Abnormal Results, and Turnaround Time.

📄 Report Generation: Generate summary reports for medical test data.

💾 Data Storage: Records are stored in medicalRecord.txt and test definitions in medicalTest.txt.

🔄 Import & Export: Supports importing and exporting medical records in CSV format.

⚠️ Error Handling: Robust error handling to ensure data integrity.

## 📜 How to Use
1. Add a New Medical Test Record
Input patient details such as Patient ID, Test Name, Test Date/Time, Result, Status, and Result Date/Time if the status is "Completed".

2. Update an Existing Medical Test Record
Search for a record by Patient ID and update the details.

3. Add or Update Test Definitions
Add or update medical test definitions (e.g., range, unit, turnaround time) for different tests.

4. Filter Records
Filter test records by criteria such as Test Name, Patient ID, Abnormal Results, and Turnaround Time.

## 🚀 Key Features
✨ Validation: Ensures all inputs are correct and formatted properly. Includes checks for:

🆔 Patient ID (7 digits)

📝 Test Name (only letters and spaces)

🕒 Test Date & Time (correct format)

🔢 Result Value (must be a number)

📊 Result Unit (letters and slashes only)

✅ Status (Pending, Completed, Reviewed)

## 🔍 Abnormal Test Detection: Identifies abnormal results based on predefined ranges for common tests like:

🩸 Hemoglobin

🩺 Blood Glucose

🫀 LDL Cholesterol

💖 Blood Pressure

## 📊 Sample Record Format
Patient ID: 1234567

Test Name: Hemoglobin

Test Date/Time: 2025-04-30 14:30

Result Value: 13.5

Result Unit: g/dL

Status: Completed

Result Date/Time: 2025-04-30 16:00

## ✍️ Author:
---

Name: Yara Khattab

📧 Email: yarakhattab16@gmail.com



🔗 GitHub: github.com/yarakhattab

