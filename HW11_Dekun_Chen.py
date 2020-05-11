from HW08_Dekun_Chen import file_reader
from prettytable import PrettyTable
from collections import defaultdict
import sqlite3
import os
from typing import List, Tuple, Dict, DefaultDict, Iterator, Any, Set

class Major:
    "track the require class and elective class for major "
    pt_header: Tuple[str,str,str] = ("Major","Required Courses","Electives")

    def __init__(self, dept:str)->None:
        self._dept:str =dept
        self.required: Set[str] = set()
        self.electives:Set[str] = set()

    def add_course(self,course:str,type:str) ->None:
        if type == 'R':
            self.required.add(course)
        elif type == 'E':
            self.electives.add(course)
        else:
            raise ValueError(f"Major not found type")

    def pt_rows(self) -> Tuple[str,List[str],List[str]]:
        "return a list of value for prettytable"
        return (self._dept,sorted(self.required),sorted(self.electives) )


class Student:
    "refer to a instance of a student"
    pt_header: Tuple[str,str,str] = ("CWID","Name","Completed Courses")
    _passing_grades = {'A','A-','B+','B','B-','C+','C'}
    _grade_map:Dict[str,float] = {
        'A':4.0,'A-':3.75,'B+':3.25,'B':3.0,'B-':2.75,'C+':2.25,'C':2.0,'C-':0,'D+':0,'D':0,'D-':0,'F':0,
    }

    def __init__(self, cwid:str,name:str,major:str,required:Set[str],electives:Set[str]):
        self._cwid:str = cwid
        self._name:str = name
        self._major:str = major
        self._rem_required: Set[str] = set(required)
        self._rem_electives: Set[str] = set(electives)
        self._courses:Dict[str,str] = dict()

    def add_course(self, course:str,grade:str) ->None:
        "student take a class and add it into its class"
        if grade not in Student._grade_map:
            raise ValueError(f"grade is not in map")

        else:
            self._courses[course] = grade
            if grade in Student._passing_grades:
                if course in self._rem_required:
                    self._rem_required.remove(course)
                if course in self._rem_electives:
                    self._rem_electives = set()

    def _gpa(self) -> float:
        points:[Student._grade_map[grade] for grade in self._courses.values()]
        if len(points)>0:
            return round(mean(points),2)
        else:
            return 0.0

    def pt_rows(self) -> Tuple[str,str,List[str],List[str],List[str],float]:
        "return a list of value for prettytable"
        return self._cwid, self._name, self._major,sorted(self._courses.keys()),\
            sorted(self._rem_required), sorted(self._rem_electives),self._gpa()


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
        self._majors:Dict[str,Major] = dict()
        self._students:Dict[str,Student] = dict()
        self._teachers:Dict[str,Teacher] = dict()

        try:
            self._get_majors(os.path.join(wdir,"majors.txt"))
            self._get_students(os.path.join(wdir,"students.txt"))
            self._get_teachers(os.path.join(wdir,"instructors.txt"))
            self._get_grades(os.path.join(wdir,"grades.txt"))
        
        except ValueError as ve:
            print(ve)
        except FileNotFoundError as fnfe:
            print("file not found")

        if prettytb:
            print("\nMajors Summary")
            self.student_table()
            print("\nStudent Summary")
            self.student_table()

            print("\nTeacher Summary")
            self.teacher_table()

    def _get_majors(self,path: str) ->None:
        for major,flag,course in file_reader(path, 3,sep='\t',header=True):
            if major not in self._majors:
                self._majors[major] = Major(major)
            self._majors[major].add_course(course,flag)

    def _get_students(self,path: str) -> None:
        "read students from the path"
        for cwid, name, major in file_reader(path, 3,sep=';',header=True):
            if major not in self._majors:
                print('not found major')
            else:
                self._students[cwid] = Student(cwid, name,major,self._majors[major].required,self._majors[major].electives)

    def _get_teachers(self,path: str) -> None:
        "read teachers from the path"
        for cwid, name, dept in file_reader(path, 3,sep='\t',header=True):
            self._teachers[cwid] = Teacher(cwid, name, dept)

    def _get_grades(self,path: str) -> None:
        "read grades from the path"
        for student_cwid, course,grade,teacher_cwid, in file_reader(path,4,sep='\t',header=True):
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

    def _students_grades_table_db_data(self,dbpath) -> Iterator[Tuple[str,str,str,str,str]]:
        try:
            db:sqlite3.Connection = sqlite3.connect(dbpath)
        except sqlite3.OperationalError:
            print(f"Error:can not operate db")
        else:
            for row in db.execute("select i.CWID, i.Name, i.Dept, g.Course, count(*) as students from instructors i join grades g on i.CWID=g.InstructorCWID group by i.Name, g.Course"):
                yield row

    def student_grades_table_db(self,dbpath):
        pt = PrettyTable(field_names = ['Name','CWID','Course','Grade','Instructor'])
        for row in self._students_grades_table_db_data(dbpath):
            pt.add_row(row)
        print(pt)

    def majors_table(self):
        pt = Prettytable(field_names = Major.pt_header)
        for major in self._majors.values():
            pt.add_row(major.pt_rows())
        print(pt)

def main():
    wdir = '/Users/homework/HW09_Repository'
    print('gd')
    _ = Repository(wdir)

if __name__ =='main':
    main()



    
    

