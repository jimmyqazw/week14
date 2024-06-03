import json

class Query:
    def __init__(self, client):
        self.student_dict = {}
        self.client = client

    def execute(self):
        name = self.get_student_name()
        self.query_student_before_deletion()
        self.collect_student_scores(name)
        self.add_student_to_server()


    def query_student_from_server(self,student_name):
        self.student_dict = {'name': student_name}
        self.client.send_command("query", self.student_dict)
        raw_data = self.client.wait_response()

        raw_data = json.loads(raw_data)
        return raw_data
        