from flask import Flask, render_template
import sqlite3

app: Flask = Flask(__name__)

@app.route('/')
def demo() -> str:
    header = ['Student', 'CWID', 'Course', 'Grade', 'Instructor']
    db_path: str = '/Users/yaoyuchen/Documents/SSW810/HWK&ASMT/HW12_Yuchen_Yao/HW12.db'

    try:
        db: sqlite3.Connection = sqlite3.connect(db_path)
    except sqlite3.OperationalError as err:
        print(err)
    else:
        dbscripts: str = 'select s.Name, s.CWID, g.Course, g.Grade, i.Name from students s join grades g ' \
                         'on s.CWID=g.StudentCWID join instructors i on g.InstructorCWID = i.CWID order by s.Name'
        rows = list(db.execute(dbscripts))

    return render_template('hello.html', header=header, rows = rows)


app.run(debug=False)