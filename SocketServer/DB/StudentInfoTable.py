from .DBConnection import DBConnection

class StudentInfoTable:
    def insert_a_student(self, name):
        command = "INSERT INTO student_info (name) VALUES ('{}');".format(name)
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def delete_a_student(self, stu_id):
        command = "DELETE FROM student_info WHERE stu_id='{}';".format(stu_id)
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def select_a_student(self, name):
        command = "SELECT * FROM student_info WHERE name='{}';".format(name)
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            records = cursor.fetchall()

        return [row['stu_id'] for row in records]
        # [(1, 'John Doe'), (3, 'John Doe')]

    def select_all_students(self):
        command = "SELECT * FROM student_info"
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            records = cursor.fetchall()

        result = dict()
        for row in records:
            result[row['stu_id']] = row['name']
        return result
