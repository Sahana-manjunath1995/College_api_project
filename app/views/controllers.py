from flask import Flask, Blueprint, jsonify,request
from app.database.controllers import Database
from markupsafe import escape


views = Blueprint('dashboard', __name__)
db = Database()

@views.route("/personal-info/")
@views.route("/personal-info/<student_id>")
def personal_info(student_id=None):
    student_info = db.get_personal_info(student_id)
    information = db.get_info()

    if student_id:
        return jsonify(data=student_info)

    return jsonify(data_info=information)



@views.route("/attendance-info/")
@views.route("/attendance-info/<student_id>")
def subject_attendance_info(student_id=None):
    sub_individual = db.get_individual_subject_attendance(student_id)
    attendance = db.get_attendance_info(student_id)
    attendance_info = db.student_attendance()

    if student_id:
        return jsonify(data_info=sub_individual, data_info1=attendance)

    return jsonify(data_info2=attendance_info)


@views.route("/individual-sub-info/<sub_id>/")
def attendance_info(sub_id=None):

    sub_attendance = db.individual_subject_attendance(sub_id)
    return jsonify(data=sub_attendance)


@views.route("/marks/")
@views.route("/marks/<student_id>/")
def marks_info(student_id=None):
    student_marks = db.student_marks()

    marks = db.get_marks(student_id)
    totalscore = db.get_total_score(student_id)

    if student_id:
        return jsonify(data1=marks, data2=totalscore)


    return jsonify(data4=student_marks)


@views.route("/student-totalscore")
def student_total_score():
    student_score = db.student_total_marks()
    return jsonify(data=student_score)


@views.route("/student-greater-avg")
def student_greater_avg():
    student_grt_avg = db.students_grtr_avg()
    return jsonify(data=student_grt_avg)


@views.route("/student-lower-avg")
def student_lower_avg():
    student_lwr_avg = db.students_lwr_avg()
    return jsonify(data=student_lwr_avg)


@views.route("/student-marks-status")
def student_marks_status():
    student_status = db.get_marks_status()
    return jsonify(data=student_status)

@views.route("/student-subject-status")
def get_subject_status():
    subject_status = db. get_individual_subject_status()
    return jsonify(data=subject_status)


@views.route("/student-pass-status")
def student_pass_status():
    pass_status = db. get_passed_status()
    return jsonify(data=pass_status )


@views.route("/student-fail-status")
def student_fail_status():
    fail_status = db. get_fail_status()
    return jsonify(data=fail_status )


@views.route("/student-low-percent")
def student_low_percent():
    low_percent = db.get_lowest_percentage()
    return jsonify(data=low_percent )


@views.route("/student-high-percent")
def student_high_percent():
    high_percent = db. get_highest_percentage()
    return jsonify(data=high_percent )


@views.route("/student-bsc-highscore")
def bsc_highscore():
    bsc_highscore = db.get_bsc_highscore()
    return jsonify(data=bsc_highscore)


@views.route("/student-bcm-highscore")
def bcm_highscore():
    bcm_highscore = db.get_bcm_highscore()
    return jsonify(data= bcm_highscore)


@views.route("/book-info/")
@views.route("/book-info/<title>")
def book_info(title=None):
    book_information = db.get_book_info()
    book_info_title = db.get_individual_bookinfo(title)

    if title:
        return jsonify(data=book_info_title)

    return jsonify(data=book_information)


@views.route("/borrow-info")
@views.route("/borrow-info/<student_id>")
def borrow_book_info(student_id=None):
    borrow_information = db.get_borrow_info()
    borrow_info_individual = db.get_individual_borrow_info(student_id)

    if student_id:
        return jsonify(data= borrow_info_individual)

    return jsonify(data= borrow_information)


@views.route("/book-count")
def book_count():
    book_count = db.get_book_count()
    return jsonify(data=book_count)


@views.route("/over-due-fine")
def over_due_fine():
    book_fine = db. get_overdue_fine()
    return jsonify(data=book_fine)


@views.route("/book-status")
def book_status():
    book_status = db.get_book_status()
    return jsonify(data=book_status)


@views.route("/teacher-info")
def teacher_info():
    teacher_info = db.get_teacher_info()
    return jsonify(data=teacher_info)


@views.route("/teacher-attendance-info")
def teacher_attendance_info():
    teacher_info = db.get_teacher_attendance()
    return jsonify(data=teacher_info)


@views.route("/teacher-salary-info")
def teacher_salary():
    teacher_salary = db.get_teacher_salary()
    return jsonify(data=teacher_salary)



@views.route("/teacher-subjects-info")
def teacher_subject_info():
    teacher_subject = db.get_teacher_subject()
    return jsonify(data=teacher_subject)