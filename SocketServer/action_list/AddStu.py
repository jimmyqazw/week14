from DB.StudentInfoTable import StudentInfoTable
from DB.SubjectInfoTable import SubjectInfoTable
class AddStu:
    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self):
        stu_id = StudentInfoTable().select_a_student(self.parameters['name'])
        if len(stu_id) == 0: #如果學生不存在，進行DB增加
            StudentInfoTable().insert_a_student(self.parameters['name'])
            stu_id = StudentInfoTable().select_a_student(self.parameters['name'])[0]

            SubjectInfoTable().insert_a_student(stu_id, self.parameters['scores'])
            return {"status": "OK"}
        else: #學生存在，不進行增加DB動作，回傳提示告訴使用者已存在
            execution_result = {
                "status": "Fail",
                "reason": "The name is already exists."
            }
            return execution_result
