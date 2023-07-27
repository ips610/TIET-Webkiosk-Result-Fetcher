import firebase_admin
from firebase_admin import credentials, firestore, auth



cred = credentials.Certificate("./ru.json")
default_app = firebase_admin.initialize_app(
    cred,
    {
        "apiKey": "AIzaSyB3EDMY_ANLh6vqC_LwhLmLhbw_okePfjo",
        "authDomain": "result-update-626.firebaseapp.com",
        "projectId": "result-update-626",
        "storageBucket": "result-update-626.appspot.com",
        "messagingSenderId": "217810071418",
        "appId": "1:217810071418:web:7f34572f6a076855fc30c3",
        "measurementId": "G-7LKBG4GB93",
    },
)
db = firestore.client(default_app)



def read_txt_file(filename):
    with open(filename, "r") as file:
        content = file.read()
    return content


def save_exam_marks_to_firestore(exam_data, rollno, exam_codes):
    try:
        # Reference the "exams" collection in Firestore
        exams_ref = db.collection("exams")

        # Create a document with the roll number as the document ID
        rollno_doc_ref = exams_ref.document(rollno)

        # Update exam_codes dictionary with the corresponding exam code and count
        exam_code = exam_data["Exam Code"]
        if exam_code in exam_codes:
            exam_codes[exam_code] += 1
        else:
            exam_codes[exam_code] = 1

        # Reference the subcollection for the specific exam code
        exam_code_subcollection_ref = rollno_doc_ref.collection(exam_code)

        # Use the "Sr No" as the document ID for each exam record
        sr_no = exam_data["Sr No"]

        # Create a document with the Sr No as the document ID and store the exam data as fields
        exam_doc_ref = exam_code_subcollection_ref.document(sr_no)
        exam_data["Roll No"] = rollno
        exam_doc_ref.set(exam_data)

        print(f"Exam marks data for Sr No {sr_no} saved to Firestore under roll number {rollno}.")
        return True
    except Exception as e:
        print(f"Error saving exam marks data for Sr No {sr_no} to Firestore:", e)
        return False

def convert_to_list_of_dictionaries(text_content):
    marks_list = []
    lines = text_content.strip().split("\n")

    exam_data = {}
    for line in lines:
        line = line.strip()
        if line:  # Check if the line is not empty
            key_value = line.split(": ")
            if len(key_value) == 2:  # Ensure that line has both key and value
                key, value = key_value
                exam_data[key] = value
            else:
                # Assuming each exam record is separated by an empty line
                if exam_data:
                    marks_list.append(exam_data.copy())  # Create a shallow copy of the dictionary
                    exam_data = {}  # Create a new dictionary for the next exam record

    # Append the last exam_data to the marks_list
    if exam_data:
        marks_list.append(exam_data.copy())  # Create a shallow copy of the dictionary

    return marks_list

if __name__ == "__main__":
    filename = "marks.txt"  # Replace with the name of your text file
    text_content = read_txt_file(filename)

    rollno = "102203100"  # Replace with the actual roll number

    marks_list = convert_to_list_of_dictionaries(text_content)
    exam_codes = {}  # Dictionary to track the exam codes and count

    for exam_data in marks_list:
        save_exam_marks_to_firestore(exam_data, rollno, exam_codes)
        print(exam_data)

    # # Automatically create the "exam code" subcollections based on the exam_codes dictionary
    # exams_ref = db.collection("exams").document(rollno)
    # for exam_code, count in exam_codes.items():
    #     for i in range(1, count + 1):
    #         exams_ref.collection(exam_code).document(str(i)).set({})  # Empty document with Sr No as the ID