from .DBConnection import DBConnection

class SubjectInfoTable:
    def insert_a_student(self, stu_id, subjects_scores):
        """Insert a student and their subjects with scores."""
        with DBConnection() as connection:
            cursor = connection.cursor()
            connection.commit()

            for subject, score in subjects_scores.items():
                cursor.execute("INSERT INTO subject_info (stu_id, subject, score) VALUES (?, ?, ?);",
                               (stu_id, subject, score))
            connection.commit()

    def delete_student_subject(self, stu_id):
        command = "DELETE FROM subject_info WHERE stu_id='{}';".format(stu_id)
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def select_student_subject(self, stu_id):
        command = "SELECT * FROM subject_info WHERE stu_id='{}';".format(stu_id)
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            records = cursor.fetchall()

        students_dict = {}
        for entry in records:
            DB_subject = entry['subject']
            DB_score = entry['score']
            students_dict[DB_subject] = DB_score

        return students_dict

    def select_all_students(self):
        command = "SELECT * FROM student_info"
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            records = cursor.fetchall()

        result = dict()
        for row in records:
            result[row['stu_id']] = row['name']
        return records