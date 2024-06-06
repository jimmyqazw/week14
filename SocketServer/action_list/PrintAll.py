from DB.StudentInfoTable import StudentInfoTable
from DB.SubjectInfoTable import SubjectInfoTable
class PrintAll:
    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self):
        result = dict()

        all_stu_dict = StudentInfoTable().select_all_students()
        for stu_id, name in all_stu_dict.items():
            stu_dict = {
                'name': name,
                'scores': SubjectInfoTable().select_student_subject(stu_id)
            }
            result[name] = stu_dict

        execution_result = {
            "status": "OK",
            "parameters": result
        }
        return execution_result