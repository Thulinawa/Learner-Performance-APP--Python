import os
import csv
from pathlib import Path
from collections import Counter
from datetime import datetime
from statistics import mean, pstdev
from threading import active_count
# inmport all the necessary libraries from this practical


#Creating variables to hold space for input and output files
workspace_dir = Path(__file__).resolve().parent
input_file = "learners.csv"
output_file ="learner_results_report.txt"

#Initializing empty variables to hold the processed data from the input file
valid_scores = []
valid_records = {} 
valid_count = Counter()
outcomes = []
performance_count = Counter()
active_pass = Counter()
active_count = Counter()


def file_validation(file_path):
    """
    This function takes the input file path as an argument and checks if the 
    file exists and is a CSV file. If the file does not exist it prints an 
    error message and exits the program.
    """
    if not os.path.exists(file_path):
        print(f"Error: The input file '{file_path}' does not exist.")
        exit(1)
    


def format_csv_data(file_path):
    """
    This function takes the input file path as an argument and reads the CSV file.
    It processes each row of the CSV file, extracting the valid data and storing 
    it in a dictionary with student IDs as keys and the other data as an imbedded dictionary. 
    Each key represents a valid learner's record. the function returns a dictionary of valid records.
    """
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            name, learner_id, result, active = (row['name'], row['learner_id'], row['result'], (row["active"].strip().casefold() == "true"))

            try:
                #validate result to be a realistic number between 0 and 100
                result = float(result)
                if not (0 <= result <= 100):
                    print(f"Error: Invalid result for learner ID {learner_id}. Skipping record.")
                    continue

                else :
                    #store the valid records in a dictionary with learner ID as key and other data as an imbedded dictionary
                    valid_records[learner_id] = {'Name': name, 'Result': result, 'Active': active}
                    valid_scores.append(result)
                    valid_count['Total'] += 1
                    if active: 
                        active_count['Active'] += 1
                    else:
                        active_count['Inactive'] += 1

        
            except ValueError:
                print(f"Error: Invalid data format for learner ID {learner_id}. Skipping record.")
                continue
            except TypeError:
                print(f"Error: Invalid data type for learner ID {learner_id}. Skipping record.")
                continue
            except Exception as e:
                print(f"Error: An unexpected error occurred for learner ID {learner_id}: {e}. Skipping record.")
                continue

            valid_records[learner_id] = {'Name': name, 'Result': result, 'Active': active}
    return valid_records


def student_lookup(learner_id):
    """
    This function takes a learner ID as an argument and looks up the corresponding 
    record in the valid_records dictionary. If the learner ID is found, it prints 
    the record; otherwise, it prints an error message.
    """
    record = valid_records.get(learner_id, None)
    if record:
        status = "active" if record["Active"] else "inactive"
        mark = "passing mark" if record["Result"] >= 50 else "failing mark"
        print(
            f"Student ID {learner_id} belongs to {record['Name']}, "
            f"who got a {record['Result']}% {mark} and is an {status} student."
        )

    else:
        print(f"Error: Learner ID {learner_id} not found.")

def calculate_performance():
    """
    This function calculates the performance of each student based on their result.
    It categorizes the results into 'Fail', or 'Pass', and counts the number of
    students in each category. The results are stored in the 
    performance_count Counter object.
    """
    for learner_id, record in valid_records.items():
        result = record['Result']
        if result >= 50:
            performance_count['Pass'] += 1
        else:
            performance_count['Fail'] += 1

def calculate_statistics(scores):
    """
    This function takes a list of scores and calculates the mean, population standard 
    deviation, min and max of the valid scores. It returns a tuple containing the mean,
    standard deviation, min and max.
    """
    if scores:
        mean_score = mean(scores)
        std_dev = pstdev(scores)
        min_score = min(scores)
        max_score = max(scores)
        return mean_score, std_dev, min_score, max_score
    else:
        return 0, 0, 0, 0
def calculate_active_pass():
    """
    This function calculates the number of active students who passed.
    It iterates through the valid_records dictionary, checks if each student is active,
    and counts the number of active students who passed. The results are 
    stored in the active_pass Counter object.
    """
    for learner_id, record in valid_records.items():
        if record['Active'] and record['Result'] >= 50:
            active_pass['Active Pass'] += 1
        else:
             continue
        

def write_report_to_file():
    """
    This function writes the report to a text file. It with listing all of the 
    individual outcomes, the total number of valid records,the number of students
    who passed and failed, the mean, standard deviation, min and max scores,
    and the number of active students who passed.
    """
    mean_score, std_dev, min_score, max_score = calculate_statistics(valid_scores)
    
    with open(output_file, mode='w', encoding='utf-8') as file:
        file.write("Individual Outcomes:\n")    
        file.write("---------------------------------------\n")
        for learner_id, record in valid_records.items():
            mark = "passing mark" if record["Result"] >= 50 else "failing mark"
            status = "active" if record["Active"] else "inactive"
            outcome = (
                f"Student ID {learner_id} belongs to {record['Name']}, "
                f"who got a {record['Result']}% {mark} and is an {status} student."
            )
            outcomes.append(outcome)
            file.write(outcome + "\n")
        file.write("---------------------------------------\n")
        file.write("The Statistical Summary of this report follows:\n")
        file.write(f"Total valid records: {valid_count['Total']}\n")
        file.write(f"Number of students who passed: {performance_count['Pass']}\n")
        file.write(f"Number of students who failed: {performance_count['Fail']}\n")
        file.write(f"Mean score: {mean_score:.2f}\n")
        file.write(f"Population standard deviation: {std_dev:.2f}\n")
        file.write(f"Minimum score: {min_score:.2f}\n")
        file.write(f"Maximum score: {max_score:.2f}\n")
        file.write(f"Number of active students who passed: {active_pass['Active Pass']}\n")
        file.write(f"Number of active students: {active_count['Active']}\n")
        file.write(f"Number of inactive students: {active_count['Inactive']}\n")
        file.write("---------------------------------------\n")
        file.write("The active students who have passed and are active are listed below:\n")
        for learner_id, record in valid_records.items():
            if record['Active'] and record['Result'] >= 50:
                file.write(f"Student ID {learner_id} belongs to {record['Name']}, who got a {record['Result']}% passing mark and is an active student.\n")
        file.write("---------------------------------------\n")
    print(f"Report saved to: {output_file}")

if __name__ == "__main__":
#Ensures that the code below is only executed when the script is run directly, not when imported as a module
    file_validation(input_file)
    format_csv_data(input_file)
    calculate_performance()
    calculate_active_pass()
    write_report_to_file()

    print("Your report has been created successfully. You can find it in the same directory as this script.")
    print("Welcome to the Learner Lookup System!")  
    
    learner_id_input = ""

    while learner_id_input.upper() != "DONE":
        try:
            learner_id_input = input("Enter a learner ID to look up (or type 'done' to finish): ").strip().upper()      
            if learner_id_input.upper() != "DONE":
                student_lookup(learner_id_input)

        except KeyboardInterrupt:
                    print("\nOperation cancelled by user.")
                    break
        except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    break   

   


        
