from DB.StudentInfoTable import StudentInfoTable
from DB.SubjectInfoTable import SubjectInfoTable
class DelStu:
    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self):
        for name in self.parameters:
            stu_id = StudentInfoTable().select_a_student(name)[0]
            StudentInfoTable().delete_a_student(stu_id)
            SubjectInfoTable().delete_student_subject(stu_id)
        return {'status': 'OK'}