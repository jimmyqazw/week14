import json

class ModifyStu:
    def __init__(self, client):
        self.student_dict = {}
        self.client = client

    def execute(self):
        return self.modify_student_from_server()


    def modify_student_from_server(self,student_name,subject,score):
        self.student_dict = {'name':student_name,'subject':subject,'scores':score}
        self.client.send_command("modify", self.student_dict)
        raw_data = self.client.wait_response()

        raw_data = json.loads(raw_data)
        return raw_data
        