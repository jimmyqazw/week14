from DB.StudentInfoTable import StudentInfoTable
from DB.SubjectInfoTable import SubjectInfoTable
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