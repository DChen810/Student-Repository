import os
from prettytable import Prettytable
from collections import defaultdict
from HW08_Dekun_Chen import file_reader
from typing import List, Tuple, Dict, DefaultDict, Iterator, Any

class Student:
    "refer to a instance of a student"
    pt_header: Tuple[str,str,str] = ("CWID","Name","Completed Courses")

    def __init__(self, cwid:str,name:str,major:str):
        self._cwid:str = cwid
        self._name:str = name
        self._major:str = major
        self._courses:Dict[str,str] = dict()

    def add_course(self, course:str,grade:str) ->None:
        "student take a class and add it into its class"
        self._courses[course] = grade

    def pt_rows(self) -> Tuple[str,str,List[str]]:
        "return a list of value for prettytable"
        return self._cwid, self._name, sorted(self._courses.keys())


class Teacher:
    "refer to a sigle teacher"
    pt_header: List[str] = ["CWID","Name","Dept","Course","Students"]

    def __init__(self,cwid:str,name:str,dept:str) ->None:
        self._cwid:str = cwid
        self._name:str = name  
        self._dept:str = dept
        self._courses:DefaultDict[str,int] =defaultdict(int)      

    def add_student(self,course:str) -> None:
        "add student to a course with tearcher"
        self._courses[course] +=1

    def pt_rows(self) ->Iterator[Tuple[str,str,str,str,int]]:
        for course, count in self._courses.items():
            yield self._cwid, self._name,self._dept,course,count


class Repository:
    "save all the information about the students and teachers"
    def __init__(self,wdir:str,prettytb:bool=True) ->None:
        self._wdir:str = wdir
        self._students:Dict[str,Student] = dict()
        self._teachers:Dict[str,Teacher] = dict()

        try:
            self._get_students(os.path.join(wdir,"students.txt"))
            self._get_teachers(os.path.join(wdir,"instructors.txt"))
            self._get_grades(os.path.join(wdir,"grades.txt"))
        
        except ValueError as ve:
            print(ve)
        except FileNotFoundError as fnfe:
            print("file not found")

        if prettytb:
            print("\nStudent Summary")
            self.student_table()

            print("\nTeacher Summary")
            self.teacher_table()


    def _get_students(self,path: str) -> None:
        "read students from the path"
        for cwid, name, major in file_reader(path, 3,sep='\t',header=False):
            self._students[cwid] = Student(cwid, name,major)

    def _get_teachers(self,path: str) -> None:
        "read teachers from the path"
        for cwid, name, dept in file_reader(path, 3,sep='\t',header=False):
            self._teachers[cwid] = Teacher(cwid, name, dept)

    def _get_grades(self,path: str) -> None:
        "read grades from the path"
        for student_cwid, course,grade,teacher_cwid, in file_reader(path,4,sep='\t',header=False):
            if student_cwid in self._students:
                self._students[student_cwid].add_course(course,grade)
            else:
                print(f"unknow student '{student_cwid}'")

            if teacher_cwid in self._teachers:
                self._teachers[teacher_cwid].add_student(course)
            else:
                print(f"unknow teacher '{teacher_cwid}'")

    def student_table(self) ->None:
        "print a prettytable of all student"
        pt: Prettytable = Prettytable(field_names = Student.pt_header)
        for student in self._students.values():
            pt.add_row(student.pt_rows())

        print(pt)

    def teacher_table(self) ->None:
        "print a prettytable of all teachers"
        pt: Prettytable = Prettytable(field_names = Teacher.pt_header)
        for teacher in self._teachers.values():
            for row in teacher.pt_rows():
                pt.add_row(row)
            

        print(pt)

def main():
    wdir = '/Users/homework/HW09_Repository'
    print('gd')
    _ = Repository(wdir)

if __name__ =='main':
    main()



    
    

