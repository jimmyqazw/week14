import json

class AddStu:
    def __init__(self, client):
        self.student_dict = {}
        self.client = client

    def execute(self):
        name = self.get_student_name()
        self.query_student_before_deletion()
        self.collect_student_scores(name)
        self.add_student_to_server()


    def add_student_to_server(self,student_dict_receive):
        self.student_dict = student_dict_receive
        self.client.send_command("add", self.student_dict)
        raw_data = self.client.wait_response()

        raw_data = json.loads(raw_data)
        if raw_data.get('status') == 'OK':
            print("    Add {} success".format(self.student_dict)) 
        else:
            print("    Add {} fail".format(self.student_dict)) 