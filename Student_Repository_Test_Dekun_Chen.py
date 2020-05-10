import unittest
import os
from HW09_Dekun_Chen import Student,Teacher,Repository
from HW08_Dekun_Chen import file_reader

class TestRepo(unittest.TestCase):
    def setUp(self):
        self.test_path = '/Users/homework/HW09_Repository'
        self.repo = Repository(self.test_path,False)

    def test_student_atrr(self):
        expect ={
            '001':('001','aaaaa','A',['k1','k02','k03','k04']),
            '0012':('0012','aaabaa','B',['k011','k012','k013','k014']),
            '0013':('0013','aaacaa','C',['k021','k022','k023','k024'])

        }

        calculate = {cwid:student.pt_rows() for cwid, student in self.repo._students.items()}

        self.assertEqual(expect,calculate)

    
    def test_teacher_atrr(self):
        expect ={
            ('001','aaaaa','A','k','k02',3),
            ('0012','aaabaa','B','k','k012',1),
            ('0013','aaacaa','C','k','k022',1)

        }

        calculate = {tuple(detail) for teacher in self.repo._teachers.values() for detail in teacher.pt_rows() }

        self.assertEqual(expect,calculate)

if __name__ == '_main_':
    unittest.main(exit=False,verbosity=2)