import app.database.models as mod
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, case, desc, cast
from flask import Blueprint
from app import db
database = Blueprint('dbutils', __name__, url_prefix='/dbutils')



class Database:
    '''This class provides query for the database '''

    def get_personal_info(self, student_id):
        '''This function retreives student personal information'''
        students = db.session.execute(db.select(
            mod.personal_info.student_id,
            mod.personal_info.name,
            mod.course.id,
            mod.course.course_name,
            mod.personal_info.email,
            mod.personal_info.contact_number
        ).filter(
            mod.personal_info.student_id == student_id,
            mod.personal_info.course_id == mod.course.id

        ))
        person_info = []
        for row in students:
            person_info.append(list(row))

        return person_info

    def get_attendance_info(self, student_id):
        '''This function retreives student attendance information'''

        attendance = db.session.execute(db.select(
            mod.attendance.student_id,
            mod.classes.class_id,
            mod.attendance.status).filter(
            mod.attendance.student_id == student_id,
            mod.attendance.class_id  == mod.classes.class_id
            )
        )
        attendance_info = []
        for row in attendance:
            attendance_info.append(list(row))

        return attendance_info

    def get_individual_subject_attendance(self, student_id):
        '''This function retreives individual subject attendance information'''

        attended_classes = func.sum(case([(mod.attendance.status=='T' ,1)], else_=0 )).label("attended")
        percentage = func.avg(case([(mod.attendance.status=='T' ,1)], else_=0 )) .label("percentage")
        subject_attendance = db.session.execute(db.select(
            mod.attendance.student_id,
            mod.subject.subject_name,
            func.count(mod.attendance.student_id),
            attended_classes,
            percentage * 100).filter(
            mod.attendance.student_id == student_id,
            mod.attendance.class_id == mod.classes.class_id,
            mod.classes.subject_id == mod.subject.sub_id).group_by(
            mod.attendance.student_id, mod.subject.sub_id
            ))

        subject_attend = []
        for row in subject_attendance:
            subject_attend.append(list(row))

        return subject_attend


    def get_marks(self, student_id):
        '''This function retreives student marks '''

        student_marks = db.session.execute(db.select(
            mod.marks.student_id,
            mod.subject.sub_code,
            mod.subject.subject_name,
            mod.marks.marks
            ).filter(
            mod.marks.student_id == student_id,
            mod.marks.sub_id == mod.subject.sub_id
        ))

        marks_info = []
        for row in student_marks:
            marks_info.append(list(row))

        return marks_info


    def get_total_score(self, student_id):
        '''This function returns tolscore of student'''

        totalscore = db.session.execute(db.select(
            mod.marks.student_id,
            func.sum(mod.marks.marks).label("totalmarks"),
            func.avg(mod.marks.marks).label("average")).filter(
            mod.marks.student_id == student_id
            ))

        total = []
        for row in totalscore:
            total.append(list(row))

        return total


    def get_info(self):
        '''This function retreives student personal information'''

        students = db.session.execute(db.select(
            mod.personal_info.student_id,
            mod.personal_info.name,
            mod.course.id,
            mod.course.course_name,
            mod.personal_info.email,
            mod.personal_info.contact_number
        ).filter(
            mod.personal_info.course_id == mod.course.id))

        person_info = []
        for row in students:
            person_info.append(list(row))

        return person_info


    def student_attendance(self):
        '''This function retreives all student's attendance '''

        attendance = db.session.execute(db.select(
            mod.attendance.student_id,
            mod.classes.class_id,
            mod.attendance.status).filter(
            mod.attendance.class_id  == mod.classes.class_id
            )
        )
        attendance_info = []
        for row in attendance:
            attendance_info.append(list(row))

        return attendance_info

    def individual_subject_attendance(self, sub_id):
        '''This function retreives individual subject attendance'''

        percentage = func.avg(case([(mod.attendance.status=='T' ,1)], else_=0 )).label("percentage")
        subject_attendance = db.session.execute(db.select(
            mod.attendance.student_id,
            mod.subject.subject_name,
            # func.count(mod.attendance.student_id),
            percentage * 100).filter(
            mod.subject.sub_id == sub_id,
            mod.attendance.class_id == mod.classes.class_id,
            mod.classes.subject_id == mod.subject.sub_id).group_by(
            mod.attendance.student_id
            ))

        subject_attend = []
        for row in subject_attendance:
            subject_attend.append(list(row))

        return subject_attend


    def student_marks(self):
        '''This function retreives student marks in all subjects'''

        student_marks = db.session.execute(db.select(
            mod.marks.student_id,
            mod.subject.sub_code,
            mod.subject.subject_name,
            mod.marks.marks
            ).filter(
            mod.marks.sub_id == mod.subject.sub_id
        ))

        marks = []
        for row in student_marks:
            marks.append(list(row))

        return marks


    def student_total_marks(self):
        '''This function retreives student's total score '''

        totalscore = db.session.execute(db.select(
            mod.marks.student_id,
            func.sum(mod.marks.marks).label("totalmarks"),
            func.avg(mod.marks.marks).label("average")).group_by(
            mod.marks.student_id
            ))

        total = []
        for row in totalscore:
            total.append(list(row))

        return total


    def students_grtr_avg(self):
        '''This function retreives student's  with  average > 35 '''

        grt_avg = db.session.execute(db.select(
            mod.marks.student_id,
            func.sum(mod.marks.marks),
            func.avg(mod.marks.marks)).having(
            func.avg(mod.marks.marks) > 35
            ).group_by(mod.marks.student_id)
        )

        avg_grt = []
        for row in  grt_avg:
            avg_grt.append(list(row))

        return avg_grt


    def students_lwr_avg(self):
        '''This function retreives student's  with  average < 35 '''

        grt_avg = db.session.execute(db.select(
            mod.marks.student_id,
            func.sum(mod.marks.marks),
            func.avg(mod.marks.marks)).having(
            func.avg(mod.marks.marks) < 35
            ).group_by(mod.marks.student_id)
        )

        avg_lwr = []
        for row in  grt_avg:
            avg_lwr.append(list(row))

        return avg_lwr


    def get_marks_status(self):
        '''This function retreives overall student's  pass or fail status'''

        marks_case = case([(func.min(mod.marks.marks) >= 35, 'Pass')], else_='Fail')
        status =  db.session.execute(db.select(
            mod.marks.student_id,
            mod.personal_info.name,
            func.sum(mod.marks.marks).label("total_marks"),
            func.avg(mod.marks.marks).label("percentage"),
            marks_case).filter(
            mod.marks.student_id == mod.personal_info.student_id).group_by(
                mod.personal_info.student_id))

        mark_status = []

        for row in status:
           mark_status.append(list(row))

        return mark_status


    def get_individual_subject_status(self):
        '''This function retreives  student's  pass or fail status in all subjects'''


        subject_status = db.session.execute(db.select(
            mod.marks.student_id ,
            mod.personal_info.name,
            mod.subject.subject_name,
            mod.marks.marks,
            func.IF(mod.marks.marks>=35, 'Pass', 'Fail').label('result')).filter(
                mod.subject.sub_id == mod.marks.sub_id,
                mod.personal_info.student_id == mod.marks.student_id)
        )

        subject = []
        for row in subject_status:
            subject.append(list(row))

        return subject


    def get_passed_status(self):
        '''This function retreives only student's  pass status in all subjects'''

        pass_status = db.session.execute(db.select(
            mod.marks.student_id,
            mod.subject.subject_name,
            mod.marks.marks,
            func.IF(mod.marks.marks >=35, 'Pass','Fail').label("result")).filter(
                mod.marks.marks >= 35,
                mod.marks.sub_id == mod.subject.sub_id
            ))

        passed_status = []
        for row in pass_status:
            passed_status.append(list(row))

        return passed_status


    def get_fail_status(self):
        '''This function retreives only student's  fail status in all subjects'''

        fail_status = db.session.execute(db.select(
            mod.marks.student_id,
            mod.subject.subject_name,
            mod.marks.marks,
            func.IF(mod.marks.marks >= 35, 'Pass','Fail').label("result")).filter(
                mod.marks.marks < 35,
                mod.marks.sub_id == mod.subject.sub_id
            ))

        failed_status = []
        for row in fail_status:
            failed_status.append(list(row))

        return failed_status


    def get_lowest_percentage(self):
        '''This function retreives student with lowest percentage'''

        low_percentage =  db.session.execute(db.select(
            mod.marks.student_id,
            func.sum(mod.marks.marks).label("totalscore"),
            func.avg(mod.marks.marks).label("percentage")).order_by(
            func.sum(mod.marks.marks).label("totalscore"),
            func.avg(mod.marks.marks).label("percentage")).group_by(
            mod.marks.student_id
            ).limit(1))

        low_percent = []
        for row in low_percentage:
            low_percent.append(list(row))

        return low_percent


    def get_highest_percentage(self):
        '''This function retreives student with highest percentage'''

        highest_percentage =  db.session.execute(db.select(
            mod.marks.student_id,
            func.sum(mod.marks.marks).label("totalscore"),
            func.avg(mod.marks.marks).label("percentage")).order_by(
            desc(func.sum(mod.marks.marks).label("totalscore")),
            desc(func.avg(mod.marks.marks).label("percentage"))).group_by(
            mod.marks.student_id
            ).limit(1))

        high_percent = []
        for row in highest_percentage:
            high_percent.append(list(row))

        return high_percent

    def get_bsc_highscore(self):
        '''This function retreives student with highest marks in BSc course'''

        search = "BSC%"
        bsc_highscore = db.session.execute(db.select(
            mod.marks.student_id,
            func.sum(mod.marks.marks).label("totalscore"),
            func.avg(mod.marks.marks).label("percentage")).filter(
            mod.marks.student_id.like(search)).group_by(
            mod.marks.student_id).order_by(
            desc(func.sum(mod.marks.marks).label("totalscore"))).limit(1)
            )

        bsc = []
        for row in  bsc_highscore:
            bsc.append(list(row))

        return bsc


    def get_bcm_highscore(self):
        '''This function retreives student with highest marks in BSc course'''

        search = "BCM%"
        bcm_highscore = db.session.execute(db.select(
            mod.marks.student_id,
            func.sum(mod.marks.marks).label("totalscore"),
            func.avg(mod.marks.marks).label("percentage")).filter(
            mod.marks.student_id.like(search)).group_by(
            mod.marks.student_id).order_by(
            desc(func.sum(mod.marks.marks).label("totalscore"))).limit(1)
            )

        bcm = []
        for row in  bcm_highscore:
            bcm.append(list(row))

        return bcm


    def get_book_info(self):
        '''This function retreives book information'''

        book_info = db.session.execute(db.select(
            mod.book_info.book_id,
            mod.book_info.title,
            mod.book_info.author,
            mod.book_info.publisher,
            mod.book_info.publish_year,
            mod.book_info.category,
            mod.book_info.status))

        books = []
        for row in book_info:
            books.append(list(row))

        return books


    def get_individual_bookinfo(self, title):
        '''This function retreives individual book information'''

        individual_book =  db.session.execute(db.select(
            mod.book_info.book_id,
            mod.book_info.title,
            mod.book_info.author,
            mod.book_info.publisher,
            mod.book_info.publish_year,
            mod.book_info.category,
            mod.book_info.status).filter(
            mod.book_info.title == title
            ))

        book_info = []
        for row in individual_book :
            book_info.append(list(row))

        return book_info


    def get_borrow_info(self):
        '''This function retreives borrow information on books'''

        loan_info = db.session.execute(db.select(
            mod.loan_info.id,
            mod.loan_info.student_id,
            mod.book_info.title,
            mod.loan_info.loaned_date,
            mod.loan_info.due_date,
            mod.loan_info.return_date).filter(
            mod.all_books.id == mod.loan_info.book_id,
            mod.book_info.book_id == mod.all_books.book_id
            ))

        borrow = []
        for row in loan_info:
            borrow .append(list(row))

        return borrow


    def get_individual_borrow_info(self, student_id):
        '''This function retreives individual borrow information on books'''

        borrow_info = db.session.execute(db.select(
            mod.loan_info.id,
            mod.loan_info.student_id,
            mod.all_books.book_id,
            mod.book_info.title,
            mod.loan_info.loaned_date,
            mod.loan_info.return_date).filter(
            mod.loan_info.student_id == student_id,
            mod.all_books.id == mod.loan_info.book_id,
            mod.all_books.book_id == mod.book_info.book_id
            ))

        indvidual_borrow = []
        for row in borrow_info:
            indvidual_borrow.append(list(row))

        return indvidual_borrow



    def get_book_count(self):
        '''This function retreives the count of books in library'''

        book_count = db.session.execute(db.select(
            mod.loan_info.student_id,
            mod.personal_info.name,
            func.count(mod.loan_info.id).label("bookcount")).filter(
                mod.all_books.id == mod.loan_info.book_id ,
                mod.loan_info.student_id == mod.personal_info.student_id).group_by(
                mod.loan_info.student_id
                ))

        book_num = []
        for row in book_count:
            book_num.append(list(row))

        return book_num


    def get_overdue_fine(self):
        '''This function retreives student's overdue fine'''

        fine = cast(mod.loan_info.return_date, db.Date) - cast(mod.loan_info.due_date, db.Date)
        overdue_fine = db.session.execute(db.select(
            mod.loan_info.id,
            mod.loan_info.student_id,
            mod.personal_info.name,
            fine*6).filter(
            mod.loan_info.return_date >  mod.loan_info.due_date,
            mod.personal_info.student_id == mod.loan_info.student_id
            ))

        student_fine = []

        for row in overdue_fine:
            student_fine.append(list(row))

        return student_fine


    def get_book_status(self):
        '''This function gives books availability information'''

        book_status = db.session.execute(db.select(
            mod.book_info.book_id,
            mod.book_info.title,
            func.sum(case([(mod.book_info.status =='available', 1)], else_=0 )).label("available"),
            func.count(mod.all_books.id).label('total')).filter(
            mod.book_info.book_id == mod.all_books.book_id).group_by(
            mod.book_info.title).order_by(mod.book_info.book_id))

        status = []
        for row in book_status:
            status.append(list(row))

        return status


    def get_teacher_info(self):
        '''This function gives teacher personal information'''

        teacher_info = db.session.execute('select * from teacher_info')

        teacher = []
        for row in teacher_info:
            teacher.append(list(row))

        return teacher


    def get_teacher_attendance(self):
        '''This function gives teacher attendance information'''

        attendance = db.session.execute(db.select(
            mod.teacher_attendance.teacher_id,
            mod.teacher_info.name,
            mod.teacher_attendance.date,
            mod.teacher_attendance.status).filter(
            mod.teacher_attendance.teacher_id ==  mod.teacher_info.teacher_id
            ))

        teacher_attendance = []
        for row in attendance:
            teacher_attendance.append(list(row))

        return teacher_attendance


    def get_teacher_salary(self):
        '''This function gives teacher salary information'''

        total_attended = func.sum(case([(mod.teacher_attendance.status == 'T', 1)], else_=0)).label('total_attended')
        salary_case = func.sum(case([(mod.teacher_attendance.status == 'F', 1)], else_=0)).label('total_salary')
        teacher_salary = db.session.execute(db.select(
            mod.teacher_attendance.id,
            mod.teacher_info.name,
            total_attended,
            mod.teacher_info.salary - (salary_case * 100 - func.count(mod.teacher_attendance.id))).filter(
            mod.teacher_attendance.teacher_id ==  mod.teacher_info.teacher_id).group_by(
            mod.teacher_info.teacher_id))

        salary = []
        for row in teacher_salary:
            salary.append(list(row))

        return salary


    def get_teacher_subject(self):
        '''This function gives subject taken by teachers'''
        teacher_subject = db.session.execute(db.select(
            mod.teacher_info.name,
            mod.subject.subject_name).filter(
            mod.teacher_info.teacher_id == mod.teacher_subject.teacher_id,
            mod.subject.sub_id == mod.teacher_subject.sub_id
            ))

        subject_teachers = []
        for row in teacher_subject:
            subject_teachers.append(list(row))

        return subject_teachers




































