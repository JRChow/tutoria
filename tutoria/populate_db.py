# -*- coding: utf-8 -*-
"""
populate_db.py.

For populating demo database
data.

Created on Oct. 20, 2017
by Jiayao
"""
import os
import random
from scheduler.models import Session
from datetime import (datetime, timedelta, time, date)
import django.utils.timezone as tz
from uuid import uuid4
from review.models import Review
from account.models import Student, Tutor


def add_review(content, rating, student, tutor, anonymous):
    """Add a review."""
    review, _ = Review.objects.get_or_create(
        content=content, rating=rating, student=student, tutor=tutor,
        anonymous=anonymous)
    review.save()
    return review


def add_coupon(start_date, end_date, coupon_code):
    """Add a new coupon."""
    from django.utils import timezone
    from wallet.models import Coupon
    coupon, _ = Coupon.objects.get_or_create(
        start_date=timezone.make_aware(start_date,
                                       timezone.get_current_timezone()),
        end_date=timezone.make_aware(end_date,
                                     timezone.get_current_timezone()),
        code=coupon_code)
    coupon.save()
    return coupon


OFFICE_HOURS = {'begin': time(9, 00),
                'end': time(19, 00)}
OFFICE_HOUR_STEP = {'CT': timedelta(hours=0.5),
                    'PT': timedelta(hours=1.0)}


def add_student(username, password, email, first_name, last_name, wallet_balance=-1, phone=99999999):
    from account.models import (User, Student)
    if wallet_balance < 0:
        wallet_balance = random.randint(1, 300) * 10

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, email=email,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name,
									    phone=phone)
        user.wallet_balance = wallet_balance

    student, _ = Student.objects.get_or_create(user=user)
    user.save()
    student.save()
    return student


def add_tutor(username, password, email, first_name, last_name,
              tutor_type='CT',
              hourly_rate=0, phone='99999999',
              bio='',
              courses=None,
              tags=None,
              wallet_balance=-1, avatar='default_avatar.png',
              sessions=None, university='HKU'):
    if tags is None:
        tags = ['Software Engineering']
    if courses is None:
        courses = [['COMP3297', 'Software Engineering']]
    from account.models import (User, Tutor)
    if wallet_balance < 0:
        wallet_balance = random.randint(1, 300) * 10
    if tutor_type == 'CT':
        hourly_rate = 0
    elif hourly_rate < 0:
        hourly_rate = random.randint(1, 300) * 10

    # tutor = Tutor.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)

    # user, _ = User.objects.get_or_create(username=username, email=email,
    # 								  password=password,
    #                                      first_name=first_name,
    #                                      last_name=last_name)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, email=email,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name,
									    phone=phone)

    tutor, _ = Tutor.objects.get_or_create(user=user)
    tutor.tutor_type = tutor_type
    tutor.wallet_balance = wallet_balance
    tutor.avatar = avatar
    tutor.university = university
    tutor.hourly_rate = hourly_rate
    tutor.bio = bio
    tutor.save()

    for tag in tags:
        tutor.tags.add(add_tag(tag))

    for course in courses:
        tutor.courses.add(add_course(course[0], course[1]))

    if sessions is not None:
        for session in sessions:
            session.tutor = tutor
            session.save()
    user.save()
    tutor.save()
    return tutor


def add_tag(tag):
    from account.models import SubjectTag
    t, _ = SubjectTag.objects.get_or_create(tag=tag)
    t.save()
    return t


def add_course(code, name):
    from account.models import Course
    c, _ = Course.objects.get_or_create(course_name=name, course_code=code)
    c.save()
    return c


def populate_tutor():
    tutors = []
    tutors.append(add_tutor(
        'georgem', 'georgem', 'georgem@cs.hku.hk', 'George', 'Mitcheson', 'PT', 100, '28597068',
        r'Before joining HKU, George accumulated many years of experience in large-scale software engineering and in R&D for real-time systems. He has headed or contributed to development of a wide range of systems spanning fields such as scientific computation, telecommunications, database management systems, control systems and autonomous robotics. This work was carried out principally in Europe and the USA. Between the two he taught for several years at the University of Puerto Rico.',
        [['COMP3297', 'Software Engineering'],
         ['COMP3403', 'Software Implmentation, Testing and Maintainence']],
        ['Software Engineering', 'Evolutionary Computing'],
        avatar='georgem.png'
    ))

    tutors.append(add_tutor(
        'clwang', 'choli', 'clwang@cs.hku.hk', 'Cho-Li', 'Wang', 'CT', 0, '28578458',
        r"Professor Cho-Li Wang received his B.S. degree in Computer Science and Information Engineering from National Taiwan University in 1985. He obtained his M.S. and Ph.D. degrees in Computer Engineering from University of Southern California in 1990 and 1995 respectively. He is currently a professor at the Department of Computer Science. Professor Wang's research interests include parallel architecture, software systems for Cluster and Grid computing, and virtualization techniques for Cloud computing. Recently, he starts working on software transaction memory for multicore/GPU clusters and multi-kernel operating systems for future single-chip manycore processor. Professor Wang has published more than 130 papers in various peer reviewed journals and conference proceedings. He is/was on the editorial boards of several international journals, including IEEE Transactions on Computers (TC), Multiagent and Grid Systems (MGS), Journal of Information Science and Engineering (JISE), International Journal of Pervasive Computing and Communications (JPCC), ICST Transactions on Scalable Information Systems (SIS). He was the program chair for Cluster’03, CCGrid'09, InfoScale’09, and ICPADS’09, ISPA’11, FCST’11, FutureTech’12, and Cluster2012; and the General Chair for IPDPS2012. He has also served as program committee members for numerous international conferences, including IPDPS, CCGrid, Cloud, CloudCom, Grid, HiPC, ICPP, and ICPADS. Professor Wang is the primary investigator of China 863 project 'Hong Kong University Grid Point' (2006-2011). The HKU Grid point consists of 3004 CPU cores (31.45 Teraflops), which offers parallel computing services for the China National Grid (CNGrid) and is used as a testbed for Cloud-related systems development. He has been invited to give keynote and plenary talk related to Distributed JVM design and Cloud Computing at various international conferences.",
        [['COMP3230', 'Operating Systems']],
        ['Cloud Computing'],
        avatar='clwang.png'
    ))

    tutors.append(add_tutor(
        'kitty', 'kitty', 'alpha_zero@deepmind.com', 'Kitty', 'K', 'PT',
        100, '00000000',
        r'I learn by meself so well. No human beats me.',
        [['COMP3314', 'Machine Learning']],
        ['Go', 'Deep Learning']

    ))

    tutors.append(add_tutor(
        'kpwat', 'kpwat', 'watkp@hku.hk', 'Kam Pui', 'Wat', 'PT', 100, '39171989',
        r'Dr. Wat receives a first class honour from BSc(Ac).',
        [['COMP2601', 'Probability & Statistics I']],
        ['Risk Management', 'Statistics'],
        avatar='watkp.png'
    ))

    return tutors


def populate_session(tutors):
    demo_date = date(2017, 11, 25)
    if tutors is not None:
        for tutor in tutors:
            d = datetime.combine(demo_date, OFFICE_HOURS['begin'])
            while d.time() <= OFFICE_HOURS['end']:
                dn = d + OFFICE_HOUR_STEP[tutor.tutor_type]
                s, _ = Session.objects.get_or_create(
                    start_time=tz.make_aware(d),
                    end_time=tz.make_aware(dn),
                    tutor=tutor,
                    status=Session.BOOKABLE)
                d = dn

    geo = tutors[0]
    kitty = tutors[2]
    s, _ = Session.objects.get_or_create(
        start_time=tz.make_aware(datetime.combine(
            date(2017, 11, 27), time(4, 00))),
        end_time=tz.make_aware(datetime.combine(
            date(2017, 11, 27), time(5, 00))),
        tutor=kitty,
        status=Session.BOOKABLE)

    s.save()
    s, _ = Session.objects.get_or_create(
        start_time=tz.make_aware(datetime.combine(
            date(2017, 11, 3), time(5, 00))),
        end_time=tz.make_aware(datetime.combine(
            date(2017, 11, 3), time(6, 00))),
        tutor=kitty,
        status=Session.BOOKABLE)
    s.save()
    s, _ = Session.objects.get_or_create(
        start_time=tz.make_aware(datetime.combine(
            date(2017, 11, 6), time(4, 00))),
        end_time=tz.make_aware(datetime.combine(
            date(2017, 11, 6), time(5, 00))),
        tutor=kitty,
        status=Session.BOOKABLE)

    s.save()
    s, _ = Session.objects.get_or_create(
        start_time=tz.make_aware(datetime.combine(
            date(2017, 11, 6), time(5, 00))),
        end_time=tz.make_aware(datetime.combine(
            date(2017, 11, 6), time(6, 00))),
        tutor=kitty,
        status=Session.BOOKABLE)
    s.save()

    s, _ = Session.objects.get_or_create(
        start_time=tz.make_aware(datetime.combine(
            date(2017, 11, 6), time(9, 00))),
        end_time=tz.make_aware(datetime.combine(
            date(2017, 11, 6), time(10, 00))),
        tutor=geo,
        status=Session.BOOKABLE)

    s.save()
    s, _ = Session.objects.get_or_create(
        start_time=tz.make_aware(datetime.combine(
            date(2017, 12, 6), time(10, 00))),
        end_time=tz.make_aware(datetime.combine(
            date(2017, 12, 6), time(11, 00))),
        tutor=geo,
        status=Session.BOOKABLE)
    s.save()


def populate_student():
    students = [add_student('kpwat', 'kpwat', 'watkp@hku.hk', 'Kam Pui', 'Wat'),
                add_student('ckchui', 'ckchui', 'ckchui@cs.hku.hk', 'Chun-Kit', 'Chui', wallet_balance=500),
                add_student('atam', 'atam', 'atam@cs.hku.hk', 'Anthony', 'Tam', wallet_balance=1000),
                add_student('jrchow', 'jrchow', 'jrchow@hku.hk', 'Jingran', 'Zhou', wallet_balance=3000)]

    return students


def populate_booking_record():
    return
    # from scheduler.models import (Session, BookingRecord)
    # from account.models import (User, Student, Tutor)
    # from wallet.models import Transaction
    # # let it err rather than create improper users
    # user = User.objects.get(username='ckchui')
    # s = Student.objects.get(user=user)
    # user = User.objects.get(username='georgem')
    #
    # DEMO_DATE = date(2017, 11, 1)
    # DEMO_TIME = time(9, 30)
    # d = datetime.combine(DEMO_DATE, DEMO_TIME)
    # dn = d + OFFICE_HOUR_STEP['CT']
    # tran, _ = Transaction.objects.get_or_create(
    #     issuer=s, receiver=t, amount=100, created_at=tz.make_aware(d), commission=5.0)
    # sess = t.session_set.all()[0]
    # sess.status = Session.BOOKED
    # sess.save()
    # # use populated session
    # # sess, _ = Session.objects.get_or_create(start_time=tz.make_aware(d), end_time=tz.make_aware(dn),tutor=t,status=Session.BOOKABLE)
    # b, _ = BookingRecord.objects.get_or_create(
    #     student=s, tutor=t, session=sess, entry_date=tz.make_aware(d), transaction=tran, status=BookingRecord.INCOMING)


def populate_review():
    """Populate some reviews into our database."""
    review_list = []
    student_list = Student.objects.all()
    tutor_list = Tutor.objects.all()
    review_list.append(add_review(content="Best tutor XD",
                                  rating=5, student=student_list[0],
                                  tutor=tutor_list[0], anonymous=False))
    review_list.append(add_review(content="Nice tutor!",
                                  rating=4, student=student_list[1],
                                  tutor=tutor_list[1], anonymous=False))

    review_list.append(add_review(content="Just a tutor...",
                                  rating=2, student=student_list[2],
                                  tutor=tutor_list[2], anonymous=False))
    review_list.append(add_review(content="Bad tutor >_<",
                                  rating=0, student=student_list[3],
                                  tutor=tutor_list[3], anonymous=True))
    return review_list


def populate_coupon():
    """Populate coupons into the database."""
    coupon_list = [add_coupon(datetime(1997, 6, 15), datetime(2097, 6, 15),
                              uuid4()),
                   add_coupon(datetime(2025, 6, 15), datetime(2035, 6, 15),
                              uuid4()),
                   add_coupon(datetime(1960, 6, 15), datetime(1997, 6, 15),
                              uuid4())]
    return coupon_list


def populate_staff():
    # create superuser
    from django.contrib.auth.models import User as Admin
    from account.models import User
    from django.contrib.auth.models import Permission
    Admin.objects.create_user(username='admin',
                              password='admin',
                              first_name='Admin',
                              is_staff=True,
                              is_superuser=True)
    User.objects.create_user(username='mytutors',
                           password='mytutors',
                           first_name='MyTutors',
                            is_staff=True)
    ca = User.objects.create_user(username='course_admin',
							password='course_admin',
							first_name='Course Admin',
							is_staff=True)
    ca.user_permissions.add(Permission.objects.get(name='Can add course'))
    ca.user_permissions.add(Permission.objects.get(name='Can change course'))
    ca.user_permissions.add(Permission.objects.get(name='Can delete course'))
    ca.user_permissions.add(Permission.objects.get(name='Can add subject tag'))
    ca.user_permissions.add(Permission.objects.get(name='Can change subject tag'))
    ca.user_permissions.add(Permission.objects.get(name='Can delete subject tag'))
    ca.user_permissions.add(Permission.objects.get(name='Can add coupon'))
    ca.user_permissions.add(Permission.objects.get(name='Can change coupon'))
    ca.user_permissions.add(Permission.objects.get(name='Can delete coupon'))

def populate():
    populate_staff()
    tutors = populate_tutor()
    students = populate_student()
    populate_session(tutors)
    populate_booking_record()
    coupons = populate_coupon()
    populate_review()
    return [tutors, students]


if __name__ == '__main__':
    populate()
