from DB.StudentInfoTable import StudentInfoTable
from DB.SubjectInfoTable import SubjectInfoTable
class ModifyStu:
    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self):
        stu_id = StudentInfoTable().select_a_student(self.parameters['name'])[0]
        StudentInfoTable().delete_a_student(stu_id)
        SubjectInfoTable().delete_student_subject(stu_id)

        stu_id = StudentInfoTable().select_a_student(self.parameters['name'])
        if len(stu_id) == 0: #如果學生不存在，進行DB增加
            StudentInfoTable().insert_a_student(self.parameters['name'])
            stu_id = StudentInfoTable().select_a_student(self.parameters['name'])[0]

            SubjectInfoTable().insert_a_student(stu_id, self.parameters['scores'])
            return {"status": "OK"}
