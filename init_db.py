# --------------------------
# initialise database
# @author: Shi Junjie
# Sat 8 June 2024
# --------------------------

from host.app import create_app as create_backend_app, db as backend_db
from endusr.app import create_app as create_frontend_app, db as frontend_db

from host.models import Course, Class, Attendance, Lecturer, Student, Device, \
    course_student, course_lecturer
from endusr.models import User

backend_app = create_backend_app()
frontend_app = create_frontend_app()


from datetime import datetime, timedelta
from host.utils import Utils
import torch

import cv2
from facial_fas_recognition.detector import FaceDetector
from facial_fas_recognition.recognizer import Recognizer
from PIL import Image

# init facial recg
face_detector = FaceDetector()
encode = Recognizer().encode

# generate embeddings for testing
def _gen_embedding(file_name) -> torch.Tensor:
    face_dir = 'known_faces/'
    print('{}{}'.format(face_dir, file_name))

    img = cv2.imread('{}{}'.format(face_dir, file_name))
    _, cropped = face_detector.detect_faces(img)
    if cropped is not None:
        cropped = Image.fromarray(cropped[0])
        embedding = encode(cropped)[0, :]
        return embedding


devices = {
    'demo_1': {
        'ip': '192.168.0.105',
        'port': 80,
    },
    'demo_2': {
        'ip': '172.18.32.42',
        'port': 80,
    },
    'FKAB DK1': {
        'ip': '172.18.32.102',
        'port': 80,
    },
    'FKAB DK6': {
        'ip': '172.18.32.44',
        'port': 80,
    },
    'FKAB DK2': {
        'ip': '172.18.32.4',
        'port': 80,
    },
    'FKAB BS5': {
        'ip': '172.18.32.5',
        'port': 80,
    },
    'FKAB BS1': {
        'ip': '172.18.32.6',
        'port': 80,
    },
    'FKAB ASTMK1': {
        'ip': '172.18.32.7',
        'port': 80,
    },
}

mock_courses = {
        'KKEE3153': 'System Design',
        'KKEE3163': 'Digital Signal Processing',
        'KKEC3113': 'Embedded Systems',
        'KKEE3133': 'Power System Analysis',
        'KKKQ3123': 'Statistics and Numerical Method',
        'KKEE3123': 'Control Engineering',
        'KKEE3143': 'Microprocessor and Microcomputer',
        'KKEC3103': 'Object Oriented Programming',
        'KKKF3103': 'Project Management',
        'KKET3103': 'Data Communication and Computer Networks',
        'KKKL3183': 'Digital Signal Processing',
        'KKKF3283': 'Engineering Ethics and Technological Advancement',
        'KKEE3113': 'Measurements and Instrumentation',
        'KKEE4103': 'Electrical Machine, Drives and Application',
        'KKET4113': 'Network and Security',
}

# Mock data for classes
mock_classes = {
    "demo_1": [
        {"course_code": "KKEE3153", "course_name": "System Design", "start_time": datetime(2024, 6, 15, 15, 0, 0), "end_time": (datetime(2024, 6, 15, 15, 0, 0) + timedelta(hours=1))},
        {"course_code": "KKEE3163", "course_name": "Digital Signal Processing", "start_time": datetime(2024, 6, 15, 17, 0, 0), "end_time": (datetime(2024, 6, 15, 17, 0, 0) + timedelta(hours=3))},
        {"course_code": "KKEC3113", "course_name": "Embedded Systems", "start_time": datetime(2024, 6, 16, 11, 0, 0), "end_time": (datetime(2024, 6, 16, 11, 0, 0) + timedelta(hours=2))}
    ],
    "FKAB DK1": [
        {"course_code": "KKEE3153", "course_name": "System Design", "start_time": datetime(2024, 6, 15, 15, 0, 0), "end_time": (datetime(2024, 6, 15, 15, 0, 0) + timedelta(hours=1))},
        {"course_code": "KKEE3163", "course_name": "Digital Signal Processing", "start_time": datetime(2024, 6, 15, 17, 0, 0), "end_time": (datetime(2024, 6, 15, 17, 0, 0) + timedelta(hours=3))},
        {"course_code": "KKEC3113", "course_name": "Embedded Systems", "start_time": datetime(2024, 6, 16, 11, 0, 0), "end_time": (datetime(2024, 6, 16, 11, 0, 0) + timedelta(hours=2))}
    ],
    "FKAB DK6": [
        {"course_code": "KKEE3133", "course_name": "Power System Analysis", "start_time": datetime(2024, 6, 15, 9, 0, 0), "end_time": (datetime(2024, 6, 15, 9, 0, 0) + timedelta(hours=1))},
        {"course_code": "KKKQ3123", "course_name": "Statistics and Numerical Method", "start_time": datetime(2024, 6, 15, 10, 0, 0), "end_time": (datetime(2024, 6, 15, 10, 0, 0) + timedelta(hours=2))},
        {"course_code": "KKEE3123", "course_name": "Control Engineering", "start_time": datetime(2024, 6, 16, 14, 0, 0), "end_time": (datetime(2024, 6, 16, 14, 0, 0) + timedelta(hours=2))}
    ],
    "FKAB DK2": [
        {"course_code": "KKEE3143", "course_name": "Microprocessor and Microcomputer", "start_time": datetime(2024, 6, 10, 10, 0, 0), "end_time": (datetime(2024, 6, 10, 10, 0, 0) + timedelta(hours=3))},
        {"course_code": "KKEC3103", "course_name": "Object Oriented Programming", "start_time": datetime(2024, 6, 15, 13, 0, 0), "end_time": (datetime(2024, 6, 15, 13, 0, 0) + timedelta(hours=1))},
        {"course_code": "KKKF3103", "course_name": "Project Management", "start_time": datetime(2024, 6, 17, 9, 0, 0), "end_time": (datetime(2024, 6, 17, 9, 0, 0) + timedelta(hours=2))}
    ],
    "FKAB BS5": [
        {"course_code": "KKET3103", "course_name": "Data Communication and Computer Networks", "start_time": datetime(2024, 6, 12, 10, 0, 0), "end_time": (datetime(2024, 6, 12, 10, 0, 0) + timedelta(hours=3))},
        {"course_code": "KKKL3183", "course_name": "Digital Signal Processing", "start_time": datetime(2024, 6, 13, 11, 0, 0), "end_time": (datetime(2024, 6, 13, 11, 0, 0) + timedelta(hours=2))}
    ],
    "FKAB BS1": [
        {"course_code": "KKKF3283", "course_name": "Engineering Ethics and Technological Advancement", "start_time": datetime(2024, 6, 14, 14, 0, 0), "end_time": (datetime(2024, 6, 14, 14, 0, 0) + timedelta(hours=3))},
        {"course_code": "KKEE3113", "course_name": "Measurements and Instrumentation", "start_time": datetime(2024, 6, 18, 8, 0, 0), "end_time": (datetime(2024, 6, 18, 8, 0, 0) + timedelta(hours=2))}
    ],
    "FKAB ASTMK1": [
        {"course_code": "KKEE4103", "course_name": "Electrical Machine, Drives and Application", "start_time": datetime(2024, 6, 20, 12, 0, 0), "end_time": (datetime(2024, 6, 20, 12, 0, 0) + timedelta(hours=2))},
        {"course_code": "KKET4113", "course_name": "Network and Security", "start_time": datetime(2024, 6, 21, 14, 0, 0), "end_time": (datetime(2024, 6, 21, 14, 0, 0) + timedelta(hours=2))}
    ]
}

# Mock data for lecturers
mock_lecturers = {
    'L000001': {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': list(mock_courses.keys()),
    },
    'L000002': {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKKQ3123', 'KKEE3133', 'KKEC3113']
    },
    'L000003': {
        'first_name': 'Alice',
        'last_name': 'Johnson',
        'email': 'alice.johnson@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKKQ3123', 'KKEE3123', 'KKEC3113', 'KKEE4103']
    },
    'L000004': {
        'first_name': 'Bob',
        'last_name': 'Williams',
        'email': 'bob.williams@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKEE3143', 'KKEC3103', 'KKKF3103']
    },
    'L000005': {
        'first_name': 'Charlie',
        'last_name': 'Brown',
        'email': 'charlie.brown@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKET3103', 'KKEC3103', 'KKEC3113', 'KKET4113']
    },
    'L000006': {
        'first_name': 'Emily',
        'last_name': 'Davis',
        'email': 'emily.davis@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKKL3183', 'KKKF3283', 'KKEE3113']
    },
}

# Mock data for students
mock_students = {
    'A178915': {
        'first_name': 'Junjie',
        'last_name': 'Shi',
        'email': 'a178915@siswa.ukm.edu.my',
        'embedding': Utils.convert_tensor_to_binary(_gen_embedding('A178915.jpg')),
        'courses': ['KKEE3153', 'KKEE3163', 'KKEC3113']
    },
    'A187006': {
        'first_name': 'Fauzi',
        'last_name': 'Fadzil',
        'email': 'a187006@siswa.ukm.edu.my',
        'embedding': Utils.convert_tensor_to_binary(_gen_embedding('A187006.jpeg')),
        'courses': ['KKEE3153', 'KKEE3163', 'KKEC3113', 'KKET3103', 'KKEE3143']
    },
    'A187898': {
        'first_name': 'Aiman',
        'last_name': 'Radzi',
        'email': 'a187898@siswa.ukm.edu.my',
        'embedding': Utils.convert_tensor_to_binary(_gen_embedding('A187898.jpeg')),
        'courses': ['KKKQ3123', 'KKEE3133', 'KKEC3113', 'KKEE3143']
    },
    'A181981': {
        'first_name': 'Ridhwan',
        'last_name': 'Hakim',
        'email': 'A181981@siswa.ukm.edu.my',
        'embedding': Utils.convert_tensor_to_binary(_gen_embedding('A181981.jpeg')),
        'courses': ['KKKQ3123', 'KKEE3123', 'KKEC3113', 'KKEE4103', 'KKEE3133'],
    },
    'A189125': {
        'first_name': 'Shafiq',
        'last_name': 'Aiman',
        'email': 'a189125@siswa.ukm.edu.my',
        'embedding': Utils.convert_tensor_to_binary(_gen_embedding('A189125.jpeg')),
        'courses': ['KKEE3143', 'KKEC3103', 'KKKF3103']
    },
    'A000005': {
        'first_name': 'Daniel',
        'last_name': 'Thomas',
        'email': 'daniel.thomas@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKET3103', 'KKEC3103', 'KKEC3113', 'KKET4113', 'KKEE4103']
    },
    'A000006': {
        'first_name': 'Mia',
        'last_name': 'Moore',
        'email': 'mia.moore@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKKL3183', 'KKKF3283', 'KKEE3113', 'KKEE4103']
    },
}

def add_mock_data():
    # Add courses
    for code, name in mock_courses.items():
        course = Course(code=code, name=name)
        backend_db.session.add(course)
        
    # Add lecturers and link to courses
    for lecturer_id, lecturer_data in mock_lecturers.items():
        lecturer = Lecturer(
            lecturer_id=lecturer_id,
            first_name=lecturer_data['first_name'],
            last_name=lecturer_data['last_name'],
            email=lecturer_data['email'],
            embedding=lecturer_data['embedding']
        )
        backend_db.session.add(lecturer)
        for course_code in lecturer_data['courses']:
            course = Course.query.filter_by(code=course_code).first()
            lecturer.courses.append(course)

    # Add students and link to courses
    for student_id, student_data in mock_students.items():
        student = Student(
            student_id=student_id,
            first_name=student_data['first_name'],
            last_name=student_data['last_name'],
            email=student_data['email'],
            embedding=student_data['embedding']
        )
        backend_db.session.add(student)
        for course_code in student_data['courses']:
            course = Course.query.filter_by(code=course_code).first()
            student.courses.append(course)

    # Add classes and attendance
    for location, classes in mock_classes.items():
        for class_data in classes:
            class_session = Class(
                course_code=class_data['course_code'],
                start_time=class_data['start_time'],
                end_time=class_data['end_time'],
                location=location,
                lecturer_id='L000001'  # Assuming the lecturer is L000001 for simplicity
            )
            backend_db.session.add(class_session)
            backend_db.session.flush()

            # Add attendance for each student in the course
            students_in_course = Student.query.join(course_student).filter(course_student.c.course_code == class_data['course_code']).all()
            for student in students_in_course:
                attendance = Attendance(
                    course_code=class_data['course_code'],
                    class_id=class_session.class_id,
                    student_id=student.student_id,
                    record_time=class_data['start_time'],
                    status='present'
                )
                backend_db.session.add(attendance)

    # Add attendance device
    for location, network in devices.items():
        device = Device(
            ip=network['ip'],
            port=network['port'],
            location=location,
        )
        backend_db.session.add(device)

    backend_db.session.commit()

def insert_frontend_data():
    for lecturer_id, lecturer_data in mock_lecturers.items():
        user = User(
            id=lecturer_id,
            email=lecturer_data['email'],
            password='123456789',
            is_lecturer=True
        )
        frontend_db.session.add(user)
    
    for student_id, student_data in mock_students.items():
        user = User(
            id=student_id,
            email=student_data['email'],
            password='123456789',
            is_lecturer=False
        )
        frontend_db.session.add(user)
    
    frontend_db.session.commit()
        

if __name__ == '__main__':
    with backend_app.app_context():
        backend_db.create_all()
        add_mock_data()
        
    with frontend_app.app_context():
        frontend_db.create_all()
        insert_frontend_data()
