from sqlalchemy.orm import relationship
from app import db




class course(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    course_name = db.Column(db.String(20))

    course_one = relationship('personal_info', backref= 'course')
    # course_two = relationship('subject', backref= 'course')


class personal_info(db.Model):
    student_id = db.Column(db.String(20), nullable=False, primary_key=True)
    name = db.Column(db.String(30))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    email = db.Column(db.Text)
    contact_number = db.Column(db.String(20))


    student_two = relationship('attendance', backref= 'personal_info')
    student_four = relationship('loan_info', backref= 'personal_info')


class subject(db.Model):
    sub_id = db.Column(db.Integer, nullable=False, primary_key=True )
    course_id = db.Column(db.Integer, db.ForeignKey('course.id') )
    subject_name = db.Column(db.Text)
    sub_code = db.Column(db.Text)

    subject_one = relationship('classes', backref= 'subject')
    subject_two = relationship('marks', backref= 'subject')
    teach_sub = relationship('teacher_info', secondary='teacher_subject',  viewonly=True)




class classes(db.Model):
    class_id = db.Column(db.String(20), nullable=False, primary_key=True)
    subject_id =  db.Column(db.Integer, db.ForeignKey('subject.sub_id') )
    date_timing =  db.Column(db.DateTime)
    duration = db.Column(db.String(20))

    class_one = relationship('attendance', backref= 'classes')


class attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    student_id = db.Column(db.String(20), db.ForeignKey('personal_info.student_id'))
    class_id = db.Column(db.String(20), db.ForeignKey('classes.class_id'))
    status = db.Column(db.String(20))




class marks(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True )
    student_id = db.Column(db.String(20))
    sub_id = db.Column(db.Integer, db.ForeignKey('subject.sub_id'))
    marks =  db.Column(db.Integer)



class book_info(db.Model):
    book_id = db.Column(db.Integer, nullable=False, primary_key=True )
    title = db.Column(db.Text)
    author = db.Column(db.String(20))
    publisher = db.Column(db.String(20))
    publish_year = db.Column(db.Integer)
    category = db.Column(db.String(20))
    status = db.Column(db.String(20))

    book_info1 = relationship('all_books', backref= 'book_info')


class all_books(db.Model):
    id = db.Column(db.Integer,nullable=False, primary_key=True )
    book_id = db.Column(db.Integer, db.ForeignKey('book_info.book_id'))

    all_books1 = relationship('loan_info', backref= 'all_books')


class loan_info(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True )
    student_id = db.Column(db.String(20),  db.ForeignKey('personal_info.student_id'))
    book_id = db.Column(db.Integer,  db.ForeignKey('all_books.id'))
    loaned_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    return_date = db.Column(db.Date)




class teacher_info(db.Model):
    teacher_id = db.Column(db.String(20), nullable=False, primary_key=True )
    name = db.Column(db.String(30))
    mail_id = db.Column(db.String(30))
    contact_number = db.Column(db.String(30))
    designation = db.Column(db.String(10))
    salary = db.Column(db.Integer)

    teacher_info1 =  relationship('teacher_attendance', backref= 'teacher_info')
    subject_teach1 = relationship("subject", secondary="teacher_subject",  viewonly=True)


class teacher_subject(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    teacher_id = db.Column(db.String(30),  db.ForeignKey('teacher_info.teacher_id'))
    sub_id = db.Column(db.Integer, db.ForeignKey('subject.sub_id'))


class teacher_attendance(db.Model):
    id =  db.Column(db.Integer, nullable=False, primary_key=True )
    teacher_id = db.Column(db.String(20), db.ForeignKey('teacher_info.teacher_id'))
    date = db.Column(db.Date)
    status = db.Column(db.String(10))






