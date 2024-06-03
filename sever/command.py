from sqlite.StudentInfoTable import StudentInfoTable
from sqlite.SubjectInfoTable import SubjectInfoTable


class AddStu:
    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self):
        
        stu_id = StudentInfoTable().select_a_student(self.parameters['name'])
        if len(stu_id) == 0:
            StudentInfoTable().insert_a_student(self.parameters['name'])
            stu_id = StudentInfoTable().select_a_student(self.parameters['name'])[0]

            SubjectInfoTable().insert_a_student(stu_id, self.parameters['scores'])
            return {"status": "OK"}
        

        else: 
            
            SubjectInfoTable().insert_a_student(stu_id[0], self.parameters['scores'])
            
            return {"status": "OK"}



class DelStu:
    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self):
        name = self.parameters['name']
        stu_id = StudentInfoTable().select_a_student(name)[0]
        StudentInfoTable().delete_a_student(stu_id)
        SubjectInfoTable().delete_student_subject(stu_id)
        return {'status': 'OK'}

class ModifyStu:
    def __init__(self, parameters):
        self.name = parameters['name']
        self.subject=parameters['subject']
        self.score=parameters['scores']
    def execute(self):
        return self.modify()

    def modify(self):

        stu_id = StudentInfoTable().select_a_student(self.name)[0]


        SubjectInfoTable().update_student_subject(stu_id,self.subject,self.score)
        return {'status': 'OK'}

class PrintAll:
    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self):
        students = self.get_students()
        return {'status': 'OK', 'parameters': students if students else {}}

    def get_students(self):
        student_records = StudentInfoTable().select_all_students()
        subject_records = SubjectInfoTable().select_all_students()
        students = {}

        for student_record in student_records:
            stu_id = student_record['stu_id']
            name = student_record['name']
            students[name] = {'name': name, 'scores': {}}

            for subject_record in subject_records:
                if subject_record['stu_id'] == stu_id:
                    subject = subject_record['subject']
                    score = subject_record['score']
                    students[name]['scores'][subject] = score

        return students


class Query:
    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self):
        name = self.parameters['name']
        stu_id = StudentInfoTable().select_a_student(name)

        if len(stu_id) == 0:
            execution_result = {
                "status": "Fail",
                "reason": "The name is not found."
            }
        else:
            # print()
            execution_result = {
                "status": "OK",
                "scores": SubjectInfoTable().select_student_subject(stu_id[0])
            }
        return execution_result