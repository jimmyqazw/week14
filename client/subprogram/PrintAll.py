import json

class PrintAll:
    def __init__(self, client):
        self.client = client

    def execute(self):
        return self.retrieve_all_students()

    def retrieve_all_students(self):
        self.client.send_command("show", student_dict={})
        reply_msg = self.client.wait_response()
        reply_msg_dict = json.loads(reply_msg)

        return reply_msg_dict
