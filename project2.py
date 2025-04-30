import re
from datetime import datetime
import csv

class MedicalTest:
    def __init__(self, patient_id, test_name, test_datetime, result_value, result_unit, status, result_datetime=None):
        self.patient_id = self.validate_patient_id(patient_id)
        self.test_name = self.validate_test_name(test_name)
        self.test_datetime = self.validate_datetime(test_datetime)
        self.result_value = self.validate_result_value(result_value)
        self.result_unit = self.validate_result_unit(result_unit)
        self.status = self.validate_status(status)
        self.result_datetime = self.validate_result_datetime(result_datetime) if status.lower() == 'completed' else None

    @staticmethod
    def validate_patient_id(patient_id):
        if re.fullmatch(r"\d{7}", patient_id):
            return patient_id
        else:
            raise ValueError("Invalid Patient ID. It must be a 7-digit number.")

    @staticmethod
    def validate_test_name(test_name):
        if re.fullmatch(r"[A-Za-z\s]+", test_name):
            return test_name
        else:
            raise ValueError("Invalid Test Name. It must contain only letters and spaces.")

    @staticmethod
    def validate_datetime(dt):
        try:
            return datetime.strptime(dt, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Invalid DateTime format. It must be YYYY-MM-DD hh:mm.")

    @staticmethod
    def validate_result_value(result_value):
        if re.fullmatch(r"\d+(\.\d+)?", result_value):
            return result_value
        else:
            raise ValueError("Invalid Result Value. It must be a number.")

    @staticmethod
    def validate_result_unit(result_unit):
        if re.fullmatch(r"[A-Za-z/]+", result_unit):
            return result_unit
        else:
            raise ValueError("Invalid Result Unit. It must contain only letters and slashes.")

    @staticmethod
    def validate_status(status):
        valid_statuses = ["pending", "completed", "reviewed"]
        if status.lower() in valid_statuses:
            return status.capitalize()
        else:
            raise ValueError(f"Invalid Status. It must be one of {', '.join(valid_statuses)}.")

    @staticmethod
    def validate_result_datetime(result_datetime):
        try:
            return datetime.strptime(result_datetime, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Invalid Result DateTime format. It must be YYYY-MM-DD hh:mm.")

    def get_turnaround_time(self):
        if self.result_datetime:
            return int((self.result_datetime - self.test_datetime).total_seconds() // 60)
        return None


    def is_abnormal(self, load_test_definitions):
        if self.test_name in load_test_definitions:
            test_def = load_test_definitions[self.test_name]
            range_val = test_def['range']
            result_value = float(self.result_value)

            if self.test_name == "Hemoglobin (Hgb)":
                if not (13.8 < result_value < 17.2):
                    return True

            elif self.test_name == "Blood Glucose Test (BGT)":
                if not (70 < result_value < 99):
                    return True

            elif self.test_name == "LDL Cholesterol Low-Density Lipoprotein (LDL)":
                if not (result_value < 100):
                    return True

            elif self.test_name == "Systolic Blood Pressure (systole)":
                if not (result_value < 120):
                    return True

            elif self.test_name == "Diastolic Blood Pressure (diastole)":
                if not (result_value < 80):
                    return True
        pass

    def __str__(self):
        return f"{self.patient_id}: {self.test_name}, {self.test_datetime.strftime('%Y-%m-%d %H:%M')}, {self.result_value}, {self.result_unit}, {self.status.lower()}, {self.result_datetime.strftime('%Y-%m-%d %H:%M') if self.result_datetime else ''}"


def load_medical_tests():
    tests = {}
    try:
        with open('medicalTest.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(';')
                if len(parts) >= 3:
                    name = parts[0].replace('Name:', '').strip()
                    range_val = parts[1].replace('Range:', '').strip()
                    unit = parts[2].replace('Unit:', '').strip()
                    duration = parts[3].replace('Turnaround Time:', '').strip() if len(parts) > 3 else ''
                    tests[name] = {
                        'range': range_val,
                        'unit': unit,
                        'duration': duration
                    }
    except FileNotFoundError:
        pass
    return tests


class PatientRecordSystem:
    def __init__(self):
        self.patients = {}
        self.medical_tests = load_medical_tests()
        self.load_patient_data()

    @staticmethod
    def load_test_definitions(self):
        definitions = {}
        try:
            with open('medicalTest.txt', 'r') as file:
                for line in file:
                    parts = line.strip().split(';')
                    if len(parts) >= 3:
                        test_name = parts[0].split(':')[1].strip()
                        range_def = parts[1].split(':')[1].strip()
                        turnaround_time = parts[2].split(':')[1].strip()
                        definitions[test_name] = {
                            'range': range_def,
                            'turnaround_time': turnaround_time
                        }
        except FileNotFoundError:
            print("The test definitions file was not found.")
        return definitions

    def save_medical_tests(self):
        with open('medicalTest.txt', 'w') as file:
            for name, info in self.medical_tests.items():
                file.write(
                    f"Name: {name}; Range: {info['range']}; Unit: {info['unit']}; Turnaround Time: {info['duration']}\n")

    def add_medical_test(self):
        name = input("Enter the medical test name: ").strip()
        range_val = input("Enter the normal range: ").strip()
        unit = input("Enter the unit: ").strip()
        duration = input("Enter the nominal duration (DD-hh-mm): ").strip()

        if name in self.medical_tests:
            print("Test already exists.")
        else:
            self.medical_tests[name] = {'range': range_val, 'unit': unit, 'duration': duration}
            self.save_medical_tests()
            print("Medical test added successfully.")

    def update_medical_test(self):
        name = input("Enter the medical test name to update: ").strip()
        if name in self.medical_tests:
            range_val = input("Enter the new normal range: ").strip()
            unit = input("Enter the new unit: ").strip()
            duration = input("Enter the new nominal duration (DD-hh-mm): ").strip()
            self.medical_tests[name] = {'range': range_val, 'unit': unit, 'duration': duration}
            self.save_medical_tests()
            print("Medical test updated successfully.")
        else:
            print("Medical test not found.")

    def add_medical_test_record(self):
        print("Enter details for the new medical test record:")
        patient_id = input("Enter Patient ID (7 digits): ").strip()
        test_name = input("Enter Test Name: ").strip()
        test_datetime = input("Enter Test Date and Time (YYYY-MM-DD hh:mm): ").strip()
        result_value = input("Enter Result Value: ").strip()
        result_unit = input("Enter Result Unit: ").strip()
        status = input("Enter Test Status (Pending/Completed/Reviewed): ").strip()
        result_datetime = input(
            "Enter Result Date and Time (YYYY-MM-DD hh:mm) (only if status is 'Completed'): ").strip() if status.lower() == 'completed' else None

        try:
            test = MedicalTest(patient_id, test_name, test_datetime, result_value, result_unit, status, result_datetime)

            # Append the new test record to the file
            with open('medicalRecord.txt', 'a') as file:
                file.write(
                    f"{patient_id}: {test_name}, {test_datetime}, {result_value}, {result_unit}, {status.lower()}, {result_datetime if result_datetime else ''}\n")

            if patient_id not in self.patients:
                self.patients[patient_id] = []
            self.patients[patient_id].append(test)
            self.save_patient_data()
            print("Medical test record added successfully.")
        except ValueError as e:
            print(e)

    def update_patient_record(self):
        patient_id = input("Enter Patient ID to update: ").strip()
        if patient_id not in self.patients:
            print("Patient ID not found.")
            return

        # Display current records
        print("Current records for Patient ID", patient_id)
        for idx, test in enumerate(self.patients[patient_id]):
            print(f"{idx + 1}: {test}")

        # Select record to update
        record_index = int(input("Enter the number of the record to update: ").strip()) - 1
        if not (0 <= record_index < len(self.patients[patient_id])):
            print("Invalid record number.")
            return

        # Get the current test details
        test = self.patients[patient_id][record_index]
        print(f"Updating record: {test}")

        # Prompt for new details
        new_test_name = input(
            f"Enter new Test Name (or press Enter to keep '{test.test_name}'): ").strip() or test.test_name
        new_test_datetime = input(
            f"Enter new Test Date and Time (YYYY-MM-DD hh:mm) (or press Enter to keep ").strip() or test.test_datetime.strftime(
            '%Y-%m-%d %H:%M')
        new_result_value = input(
            f"Enter new Result Value (or press Enter to keep '{test.result_value}'): ").strip() or test.result_value
        new_result_unit = input(
            f"Enter new Result Unit (or press Enter to keep '{test.result_unit}'): ").strip() or test.result_unit
        new_status = input(
            f"Enter new Test Status (Pending/Completed/Reviewed) (or press Enter to keep '{test.status}'): ").strip() or test.status
        new_result_datetime = input(
            f"Enter new Result Date and Time (YYYY-MM-DD hh:mm) (only if status is 'Completed', or press Enter to keep '{test.result_datetime}'): ").strip() if new_status.lower() == 'completed' else None

        try:
            updated_test = MedicalTest(
                patient_id,
                new_test_name,
                new_test_datetime,
                new_result_value,
                new_result_unit,
                new_status,
                new_result_datetime
            )

            # Update in-memory data
            self.patients[patient_id][record_index] = updated_test

            # Rewrite the medicalRecord.txt file
            with open('medicalRecord.txt', 'w') as file:
                for patient_id, tests in self.patients.items():
                    for test in tests:
                        file.write(
                            f"{patient_id}: {test.test_name}, {test.test_datetime.strftime('%Y-%m-%d %H:%M')}, {test.result_value}, {test.result_unit}, {test.status.lower()}, {test.result_datetime.strftime('%Y-%m-%d %H:%M') if test.result_datetime else ''}\n")

            print("Patient record updated successfully.")
        except ValueError as e:
            print(f"Error updating patient record: {e}")

    def load_patient_data(self):
        try:
            with open('medicalRecord.txt', 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(': ', 1)
                    if len(parts) != 2:
                        continue
                    patient_id = parts[0].strip()
                    details = parts[1].split(', ')
                    if len(details) < 5:
                        continue

                    try:
                        test = MedicalTest(
                            patient_id,
                            details[0],
                            details[1],
                            details[2],
                            details[3],
                            details[4],
                            details[5] if len(details) > 5 else None
                        )
                        if patient_id not in self.patients:
                            self.patients[patient_id] = []
                        self.patients[patient_id].append(test)
                    except ValueError as e:
                        print(f"Error loading patient data: {e}")
        except FileNotFoundError:
            pass


    def filter_medical_tests(self):
        print("\n--- Filter Medical Tests ---")
        criteria = {
            'patient_id': input("Enter Patient ID (or leave blank): ").strip(),
            'test_name': input("Enter Test Name (or leave blank): ").strip(),
            'abnormal': input("Filter Abnormal Tests? (yes/no, or leave blank): ").strip().lower(),
            'start_date': input("Enter start date (YYYY-MM-DD, or leave blank): ").strip(),
            'end_date': input("Enter end date (YYYY-MM-DD, or leave blank): ").strip(),
            'status': input("Enter Test Status (Pending/Completed/Reviewed, or leave blank): ").strip().capitalize(),
            'min_turnaround_time': input("Enter minimum turnaround time in minutes (or leave blank): ").strip(),
            'max_turnaround_time': input("Enter maximum turnaround time in minutes (or leave blank): ").strip()
        }

        start_date = datetime.strptime(criteria['start_date'], "%Y-%m-%d") if criteria['start_date'] else None
        end_date = datetime.strptime(criteria['end_date'], "%Y-%m-%d") if criteria['end_date'] else None
        min_turnaround_time = float(criteria['min_turnaround_time']) if criteria['min_turnaround_time'] else None
        max_turnaround_time = float(criteria['max_turnaround_time']) if criteria['max_turnaround_time'] else None

        abnormal = criteria['abnormal'] == 'no'

        with open('medicalRecord.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(':', 1)
                if len(parts) > 1:
                    patient_id = parts[0].strip()
                    test_data = parts[1].strip().split(',')
                    if len(test_data) >= 5:
                        test_name = test_data[0].strip()
                        test_datetime = test_data[1].strip()
                        result_value = test_data[2].strip()
                        result_unit = test_data[3].strip()
                        status = test_data[4].strip()
                        result_datetime = test_data[5].strip() if len(test_data) == 6 else None
                        try:
                            test = MedicalTest(patient_id, test_name, test_datetime, result_value, result_unit, status,
                                               result_datetime)
                            turnaround_time = test.get_turnaround_time()

                            # Apply filters including the turnaround time range
                            if (
                                    (not criteria['patient_id'] or test.patient_id == criteria['patient_id']) and
                                    (not criteria['test_name'] or test.test_name == criteria['test_name']) and
                                    (not abnormal or test.is_abnormal(self.load_test_definitions(self))) and
                                    (not start_date or test.test_datetime >= start_date) and
                                    (not end_date or test.test_datetime <= end_date) and
                                    (not criteria['status'] or test.status == criteria['status']) and
                                    (not min_turnaround_time or (
                                            turnaround_time and turnaround_time >= min_turnaround_time)) and
                                    (not max_turnaround_time or (
                                            turnaround_time and turnaround_time <= max_turnaround_time))
                            ):
                                if abnormal and not test.is_abnormal(self.load_test_definitions(self)):
                                    continue  # Skip normal tests if abnormal filtering is enabled
                                print(test)
                        except ValueError:
                            continue

                            

    def save_patient_data(self):
        with open('medicalRecord.txt', 'w') as file:
            for patient_id, tests in self.patients.items():
                for test in tests:
                    file.write(
                        f"{patient_id}: {test.test_name}, {test.test_datetime.strftime('%Y-%m-%d %H:%M')}, {test.result_value}, {test.result_unit}, {test.status.lower()}, {test.result_datetime.strftime('%Y-%m-%d %H:%M') if test.result_datetime else ''}\n")




    def generate_summary_report(self, filters):
        pass

    def import_medical_records(self):
        input_filename = input("Enter the input filename (e.g., 'import_records.csv'): ").strip()
        output_filename = input("Enter the output filename (default is 'medicalRecord.txt'): ").strip()
        if not output_filename:
            output_filename = "medicalRecord.txt"

        try:
            with open(input_filename, 'r') as infile, open(output_filename, 'a') as outfile:
                next(infile)  # Skip header line
                for line in infile:
                    fields = line.strip().split(',')
                    formatted_line = ', '.join(fields) + '\n'
                    outfile.write(formatted_line)

            print(f"Records successfully imported from {input_filename} to {output_filename}")
        except FileNotFoundError:
            print(f"Error: {input_filename} not found.")
        except Exception as e:
            print(f"An error occurred during import: {e}")

    def export_medical_records(self):
        input_filename = input("Enter the input filename (default is 'medicalRecord.txt'): ").strip()
        if not input_filename:
            input_filename = "medicalRecord.txt"

        output_filename = input("Enter the output filename (e.g., 'exported_records.csv'): ").strip()

        try:
            with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
                outfile.write(
                    "Patient ID,Test Name,Test Date Time,Result Value,Results Unit,Status,Results Date Time\n")
                for line in infile:
                    fields = line.strip().split(', ')
                    csv_line = ','.join(fields) + '\n'
                    outfile.write(csv_line)

            print(f"Records successfully exported to {output_filename}")
        except FileNotFoundError:
            print(f"Error: {input_filename} not found.")
        except Exception as e:
            print(f"An error occurred during export: {e}")


def main_menu():
    while True:
        print("\n--- Patient Record Management System ---")
        print("1. Add New Medical Test")
        print("2. Update Medical Test")
        print("3. Add New Medical Test Record")
        print("4. Update Medical Test Record")
        print("5. Filter Medical Tests")
        print("6. Generate Summary Report")
        print("7. Import Records from CSV")
        print("8. Export Records to CSV")
        print("9. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            system.add_medical_test()
        elif choice == '2':
            system.update_medical_test()
        elif choice == '3':
            system.add_medical_test_record()
        elif choice == '4':
            system.update_patient_record()
        elif choice == '5':
            system.filter_medical_tests()
        elif choice == '6':
            system.generate_summary_report()
        elif choice == '7':
            system.import_medical_records()
        elif choice == '8':
            system.export_medical_records()
        elif choice == '9':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
        system = PatientRecordSystem()
        main_menu()