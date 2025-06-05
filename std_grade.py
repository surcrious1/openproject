import sqlite3

# 데이터베이스 연결 및 테이블 생성
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    number TEXT PRIMARY KEY,
    name TEXT,
    eng INTEGER,
    c INTEGER,
    py INTEGER,
    total INTEGER,
    avg REAL,
    grade TEXT,
    rank INTEGER
)
""")
conn.commit()

# Student 클래스 정의
class Student:
    def __init__(self, number, name, eng, c, py):
        self.number = number
        self.name = name
        self.eng = int(eng)
        self.c = int(c)
        self.py = int(py)
        self.total = 0
        self.avg = 0
        self.grade = ''
        self.rank = 0

    def total_average(self):
        self.total = self.eng + self.c + self.py
        self.avg = self.total / 3

    def cal_grade(self):
        if self.avg >= 90:
            self.grade = 'A'
        elif self.avg >= 80:
            self.grade = 'B'
        elif self.avg >= 70:
            self.grade = 'C'
        elif self.avg >= 60:
            self.grade = 'D'
        else:
            self.grade = 'F'

    def save_to_db(self, cursor):
        cursor.execute("""
        INSERT OR REPLACE INTO students 
        (number, name, eng, c, py, total, avg, grade, rank)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.number, self.name, self.eng, self.c, self.py, self.total, self.avg, self.grade, self.rank))

    def print_info(self):
        return f"{self.number}\t{self.name}\t{self.eng}\t{self.c}\t{self.py}\t{self.grade}\t{self.rank}"

# 성적 관리 기능 클래스
class gradefunction:
    def __init__(self):
        self.students = []

    def input_info(self):
        number = input("학번 : ")
        name = input("이름 : ")
        eng = input("영어 성적 : ")
        c = input("C언어 성적 : ")
        py = input("파이썬 성적 : ")
        student = Student(number, name, eng, c, py)
        student.total_average()
        student.cal_grade()
        return student

    def insert_std(self, student):
        self.students.append(student)
        student.save_to_db(cursor)
        conn.commit()

    def load_students_from_db(self):
        self.students = []
        cursor.execute("SELECT * FROM students")
        for row in cursor.fetchall():
            s = Student(row[0], row[1], row[2], row[3], row[4])
            s.total = row[5]
            s.avg = row[6]
            s.grade = row[7]
            s.rank = row[8]
            self.students.append(s)

    def print_info(self):
        print("학번", "이름", "영어", "C언어", "파이썬", "학점", "등수", sep='\t')
        for s in self.students:
            print(s.print_info())

    def cal_rank(self):
        for now in self.students:
            now.rank = 1
            for other in self.students:
                if now.total < other.total:
                    now.rank += 1

    def delete_std(self, number):
        for s in self.students:
            if s.number == number:
                self.students.remove(s)
                cursor.execute("DELETE FROM students WHERE number = ?", (number,))
                conn.commit()
                print("해당 학생의 정보가 삭제되었습니다.")
                return
        print("해당 학번의 학생은 존재하지 않습니다.")

    def find_std(self, avg):
        for s in self.students:
            if s.avg == avg:
                return s.number
        return None

    def sort_std(self):
        self.students.sort(key=lambda s: s.total, reverse=True)

    def over_80(self):
        cnt = 0
        for s in self.students[:]:
            if s.avg >= 80:
                cnt += 1
            else:
                temp = self.find_std(s.avg)
                self.delete_std(temp)

        if cnt == 0:
            print("80점이 넘은 학생은 없습니다.")
        else:
            print("80점이 넘은 학생은", cnt, "명입니다.")
            self.print_info()

# main 실행부
f = gradefunction()

# 학생 입력 및 추가
for _ in range(5):
    std = f.input_info()
    f.insert_std(std)

# DB에서 불러오기 및 등수, 정렬 등 처리
f.load_students_from_db()
f.cal_rank()

print("-학생 정보-(입력순)")
f.print_info()

f.sort_std()
print("-학생 정보-(정렬순)")
f.print_info()

f.over_80()

# DB 연결 종료
conn.close()
