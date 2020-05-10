from datetime import datetime, timedelta
import unittest
from collections import defaultdict
from collections import Counter
from typing import List, Tuple, Dict, Set , Any,IO,DefaultDict,Iterator
import os
from prettytable import prettytable

def date_arithmetic() -> Tuple[datetime, datetime, int]:
    """ 
    return the data 3days after feb 27,2020 and 2019
    return the days passed between feb 1 ,2019 and sep 30,2019
    """
    
    data_2020227: datetime = datetime(2020,2,27)
    dela : timedelta = timedelta(days = 3)
    date1:datetime = data_2020227 + dela

    data_2019227:datetime = datetime(2019,2,27)
    dela2 : timedelta = timedelta(days=3)
    date2 : datetime = data_2019227 + dela2

    data_2019930:datetime = datetime(2019,9,30)
    data_2019201:datetime = datetime(2019,2,1)
    dela3 : timedelta = data_2019930 - data_2019201
    
    return date1, date2,dela3.days
    

    

def file_reader(path:str, numfields: int, sep: str =',', header:bool=False) -> Iterator[Tuple[str]]:
    """
    Write a generator function file_reader() to read field-separated text files and yield a tuple with all of the values from a single line in the file on each call to next().
    The generator definition should include following parameters:
    path: str 
    fields: int 
    sep: str 
    header: bool
    raise a FileNotFound exception if the specified file can’t be opened for reading along with a meaningful message to help the reader to understand the problem
    raise a ValueError exception if a line in the file doesn’t have exactly the expected number of fields, e.g. “ValueError: ‘foo.txt’ has 3 fields on line 26 but expected 4”.  
    """

    try:
        fp :IO = open(path,"r",encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"can not open '{path}' file")
    else:
        with fp:
            for n, line in enumerate(fp,1):
                field: List[str] = line.strip('\n').split(sep)
                if len(field) !=numfields:
                    raise ValueError(f"'{path}' line:{n}: read {len(field)} field but is expected {numfields}")
                elif n==1 and header:
                    continue
                else:
                    yield tuple(field)


class FileAnalyzer:
    """ Write a Python class, FileAnalyzer that given a directory name, searches that directory for Python files (i.e. files ending with .py). For each .py file in the directory, open each file and calculate a summary of the file including:
    the file name
    the total number of lines in the file
    the total number of characters in the file
    the number of Python functions (lines that begin with ‘def ’, including methods inside class definitions) 
    the number of Python classes (lines that begin with ‘class ’)"""
    def __init__(self, directory: str) -> None:
        """ summerize the directory of the class function and chars"""
        self.directory: str = directory # NOT mandatory!
        self.files_summary: Dict[str, Dict[str, int]] = dict() 
        self.analyze_files() # summerize the python files data

    def analyze_files(self) -> None:
        """ summerize the directory and return a dict with a number of the calss function and str
            raise the FileNotFound if directory can not be open or file in directory can not be open
        """
        result:Dict[str,int] = dict()
        try:
            file: List[str] = os.listdir(self.directory)
        except FileNotFoundError:
            raise FileNotFoundError(f"{self.directory} is not found")
        else:
            for file1 in file:
                if file1.lower().endswith('.py'):
                    path: str = os.path.join(self.directory,file1)
                    try:
                        self.files_summary[path] = self.processfile(path)
                    except FileNotFoundError as Enfound:
                        raise Enfound

    
    def processfile(self,path:str) -> Dict[str,int]:
        """summerize the content of the file and return the class function line and str raise exceptions  """
        try:
            fp:IO = open(path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f"Unablt to open '{path}'")
        else:
            with fp:
                counts: DefaultDict[str,int] = defaultdict(int)
                for line in fp:
                    counts['char'] += len(line)
                    counts['line'] +=1
                    line = line.strip()
                    if line.startswith('class '):
                        counts['class'] +=1
                    elif line.startswith('def '):
                        counts['function']+=1
                return counts

                        

    def pretty_print(self) -> None:
        """ print the prettytable with the result"""
        prettytb: PrettyTable = PrettyTable(field_name = ['File Name','Classes','Functions','Lines','Characters'])
        for file in self.files_summary:
            counts:Dict[str,int] = self.files_summary[file]
            prettytb.add_row([file,counts['class'], counts['function'], counts['line'],counts['char'] ])

        return prettytb
