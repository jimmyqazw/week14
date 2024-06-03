import json

class DelStu:
    def __init__(self, client):
        self.student_dict = {}
        self.client = client

    def execute(self):
        return self.del_student_from_server()


    def del_student_from_server(self,student_name):
        self.student_dict = {'name': student_name}
        self.client.send_command("del", self.student_dict)
        raw_data = self.client.wait_response()

        raw_data = json.loads(raw_data)
        return raw_data
        