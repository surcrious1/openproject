#sturct 이용 성적계산프로그램 코드 작성 ~4/16
class Student:
    #변수 초기화
    #학번, 이름, 영어 성적, C언어 성적, 파이썬 성적, 총합, 평균 성적, 등수, 학점
    def __init__(self, number, name, eng, c, py):
        self.number=number
        self.name=name
        self.eng=int(eng)
        self.c=int(c)
        self.py=int(py)
        self.total=0
        self.avg=0
        self.grade=''
        self.rank=0

    #총합 및 평균을 구하는 함수
    def total_average(self):
        self.total=self.eng+self.c+self.py
        self.avg=self.total/3

    def cal_grade(self):
        if(self.avg>=90):
            self.grade='A'
        elif(self.avg>=80):
            self.grade='B'
        elif(self.avg>=70):
            self.grade='C'
        elif(self.avg>=60):
            self.grade='D'
        else:
            self.grade='F'

    def print_info(self):
        return f"{self.number}\t{self.name}\t{self.eng}\t{self.c}\t{self.py}\t{self.grade}"
    
class gradefunction:
    def __init__(self):
        self.students=[]

    #학생들의 정보를 받고 저장한다.
    #정보를 받고 받은 정보를 바로 총합,평균을 구하는 함수를 호출한다.
    def input_info(self):
        for i in range(5):
            number=input("학번 : ")
            name=input("이름 : ")
            eng=input("영어 성적 : ")
            c=input("C언어 성적 : ")
            py=input("파이썬 성적 : ")
            student=Student(number, name, eng, c, py)
            student.total_average()
            student.cal_grade()
            return student
            
    #학생들의 정보를 출력하는 함수 
    #등수 순서대로 학생들의 정보를 출력한다.   
    def print_info(self):
        print("학번", "이름", "영어", "C언어", "파이썬","학점", "등수",sep='\t')
        for s in self.students:
            print(s.number, s.name, s.eng, s.c, s.py, s.grade, s.rank,sep='\t')
    
    #학생들의 등수를 결정하는 함수
    #기본 등수를 1로 지정하고 총점을 비교하여 더 적은 학생에게 1을 더한다.
    #해당 방법으로 총점이 높은 학생은 적은 수를 반대는 높은 수를 가지게 되며
    #만일 등수가 같다면 같은 경우에는 서로 수를 더하지 않으므로 같은 등수를 같게 된다.
    def cal_rank(self):
        for now in self.students:
            now.rank=1
            for notnow in self.students:
                if now.total < notnow.total:
                    now.rank+=1
    
    #학생을 삽입하는 함수
    #입력함수에서 학생의 정보를 받고 해당 정보의 학생을 삽입한다.
    def insert_std(self, student):
        self.students.append(student)
    
    #탐색 함수로 찾은 학번으로 학생 삭제하는 함수
    #학번을 매개변수로 받아 해당 학생을 삭제한다.
    def delete_std(self, number):
        for s in self.students:
            #해당 학생이 존재한다면 삭제한다.
            if s.number == number:
                self.students.remove(s)
                print("해당 학생의 정보가 삭제되었습니다.")
                return
        #학번으로 찾을 수 없다면 해당 문구를 출력한다.
        print("해당 학번의 학생은 존재하지 않습니다.")
    
    #학생의 평균값을 통해 학번을 알아내는 함수
    #알아낸 학번을 삭제함수의 매개변수로 넘겨주어 학생의 정보를 삭제한다.
    def find_std(self, avg):
        for s in self.students:
            if s.avg==avg:
                return s.number
        return None

    #total, 즉 총점을 통해 학생을 정렬하는 함수
    #파이썬의 정렬 기능을 사용하여 정렬한다.
    def sort_std(self):
        self.students.sort(key=lambda s:s.total, reverse=True)
        #정렬 방식을 잘 모르겠음, 알아볼것
    
    #80점이 넘은 학생의 수 출력하는 함수
    #cnt에 학생의 수를 저장하고 리턴한다.
    def over_80(self):
        cnt=0
        for s in self.students[:]:
            if s.avg>=80:
                cnt+=1
            else:
                temp=self.find_std(s.avg)
                self.delete_std(temp)

        #80이 넘는 학생이 없다면 학생들의 수와 정보를 출력하지 않는다.
        if cnt==0:
            print("80점이 넘은 학생은 없습니다.")
        #만약 80이 넘는 학생이 존재한다면 학생의 수와 정보를 출력한다.
        else: 
            print("80점이 넘은 학생은 ", cnt, "명입니다. ")
            self.print_info()
    
#main 함수
f=gradefunction()
#5명의 학생의 정보를 받고 해당 정보들을 추가한다.
for i in range(5):
    new_std=f.input_info()
    f.insert_std(new_std)

#5명의 정보를 바탕으로 등수를 정렬한다.
f.cal_rank()

#입력된 순서대로 정보를 출력한다.
print("-학생 정보-(입력순)")
f.print_info()

#총점(등수) 순서대로 정렬 후 학생들의 정보를 다시 출력한다.
f.sort_std()
print("-학생 정보-(정렬순)")
f.print_info()

#80이상 학생의 수, 학생의 정보를 출력한다. 
f.over_80()

#input
"""
학번 : 1
이름 : 김ㅇㅇ
영어 성적 : 70
C언어 성적 : 70
파이썬 성적 : 70
학번 : 2
이름 : 이ㅁㅁ
영어 성적 : 80
C언어 성적 : 80
파이썬 성적 : 80
학번 : 3
이름 : 박ㅅㅅ
영어 성적 : 60
C언어 성적 : 60
파이썬 성적 : 60
학번 : 4
이름 : 황ㄱㄱ
영어 성적 : 100
C언어 성적 : 100
파이썬 성적 : 100
학번 : 5
이름 : 최ㄹㄹ
영어 성적 : 90
C언어 성적 : 90
파이썬 성적 : 90
"""

#output
"""
-학생 정보-(입력순)
학번    이름    영어    C언어   파이썬  학점    등수
1       김ㅇㅇ  70      70      70      C       4
2       이ㅁㅁ  80      80      80      B       3
3       박ㅅㅅ  60      60      60      D       5
4       황ㄱㄱ  100     100     100     A       1
5       최ㄹㄹ  90      90      90      A       2
-학생 정보-(정렬순)
학번    이름    영어    C언어   파이썬  학점    등수
4       황ㄱㄱ  100     100     100     A       1
5       최ㄹㄹ  90      90      90      A       2
2       이ㅁㅁ  80      80      80      B       3
1       김ㅇㅇ  70      70      70      C       4
3       박ㅅㅅ  60      60      60      D       5
해당 학생의 정보가 삭제되었습니다.
해당 학생의 정보가 삭제되었습니다.
80점이 넘은 학생은  3 명입니다.
학번    이름    영어    C언어   파이썬  학점    등수
4       황ㄱㄱ  100     100     100     A       1
5       최ㄹㄹ  90      90      90      A       2
2       이ㅁㅁ  80      80      80      B       3
"""