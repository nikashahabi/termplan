# Create your tests here.
import json

from rest_framework.test import APITestCase

from src.models import Department, ChartTable, Course, SemesterCourse, Professor, User, UserSchedule, UserPassed


class TestHomepage(APITestCase):
    def test_anonymous_cannot_see_page(self):
        response = self.client.get('')
        self.assertRedirects(response, "/login/?next=/")

    def test_authenticated_user_can_see_page(self):
        department = Department.objects.create(name="test_dep")
        user = User.objects.create(username='test', password='1234', department=department)
        self.client.force_login(user=user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')


class TestCoursesList(APITestCase):

    def test_semester_courses_list(self):
        department = Department.objects.create(name="dep1")
        prof1 = Professor.objects.create(name="prof1", department=department)
        prof2 = Professor.objects.create(name="prof2", department=department)
        table = ChartTable.objects.create(dep=department, code=1)
        course1 = Course.objects.create(name="course1", code=1, department=department, unit=3, table=table)
        course2 = Course.objects.create(name="course2", code=2, department=department, unit=3, table=table)
        sc1 = SemesterCourse.objects.create(course=course1, professor=prof1, start_time=10.0, end_time=12.0, day1='1',
                                            day2='3',
                                            capacity=40, group=1)
        sc2 = SemesterCourse.objects.create(course=course2, professor=prof2, start_time=8.0, end_time=10.0, day1='2',
                                            day2='4',
                                            capacity=30, group=1)
        data = {'dep_id': 1}
        response = self.client.post('/courses_list/', data=data, format='json')
        expected_response = [{
            "course_id": f"{sc1.course.code}-{sc1.group}",
            "name": sc1.course.name,
            "class_times": [{
                "day": sc1.day1,
                "start": sc1.start_time,
                "end": sc1.end_time
            }, {"day": sc1.day2,
                "start": sc1.start_time,
                "end": sc1.end_time}],
            "ta_time": sc1.ta_time,
            "ta_day": sc1.ta_day,
            "exam_time": sc1.exam,
            "department": sc1.course.department.name,
            "units": sc1.course.unit,
            "instructor": sc1.professor.name,
            "course_number": sc1.course.code,
            "info": sc1.info,
            "capacity": sc1.capacity

        }, {
            "course_id": f"{sc2.course.code}-{sc2.group}",
            "name": sc2.course.name,
            "class_times": [{
                "day": sc2.day1,
                "start": sc2.start_time,
                "end": sc2.end_time
            }, {"day": sc2.day2,
                "start": sc2.start_time,
                "end": sc2.end_time}],
            "ta_time": sc2.ta_time,
            "ta_day": sc2.ta_day,
            "exam_time": sc2.exam,
            "department": sc2.course.department.name,
            "units": sc2.course.unit,
            "instructor": sc2.professor.name,
            "course_number": sc2.course.code,
            "info": sc2.info,
            "capacity": sc2.capacity

        }]
        print(response)
        self.assertEqual(json.loads(response.content)['data'], expected_response)


class TestSchedule(APITestCase):

    def test_anonymous_cannot_see_page(self):
        response = self.client.get('/schedule/')
        self.assertRedirects(response, "/login/?next=/schedule/")

    def test_authenticated_user_can_see_page(self):
        department = Department.objects.create(name="test_dep")
        user = User.objects.create(username='test', password='1234', department=department)
        self.client.force_login(user=user)
        response = self.client.get('/schedule/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grid.html')

    def test_add_delete_course(self):
        department = Department.objects.create(name="test_dep")
        user = User.objects.create(username='test', password='1234', department=department)
        prof1 = Professor.objects.create(name="prof1", department=department)
        table = ChartTable.objects.create(dep=department, code=1)
        course1 = Course.objects.create(name="course1", code=1, department=department, unit=3, table=table)
        sc1 = SemesterCourse.objects.create(course=course1, professor=prof1, start_time=10.0, end_time=12.0, day1='1',
                                            day2='3',
                                            capacity=40, group=1)
        self.client.force_login(user=user)

        # add course
        response = self.client.post("/add_course/", data={'course_id': "1-1"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserSchedule.objects.filter(user=user).count(), 1)
        self.assertEqual(UserSchedule.objects.filter(user=user).first().courses.count(), 1)

        # delete course
        response = self.client.post("/delete_course/", data={'course_id': "1-1"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserSchedule.objects.filter(user=user).count(), 1)
        self.assertEqual(UserSchedule.objects.filter(user=user).first().courses.count(), 0)


class TestGraduation(APITestCase):
    def test_anonymous_cannot_see_page(self):
        response = self.client.get('/graduation/')
        self.assertRedirects(response, "/login/?next=/graduation/")

    def test_authenticated_user(self):
        department = Department.objects.create(name="test_dep")
        user = User.objects.create(username='test', password='1234', department=department)
        self.client.force_login(user=user)

        # test user  can see page
        response = self.client.get('/graduation/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'graduation.html')

        # test chart tables count
        table = ChartTable.objects.create(dep=department, code=1)
        response = self.client.post('/graduation/', {"group": 0}, format='json')
        self.assertEqual(json.loads(response.content)['group_count'], 1)

        # test chart table course list with no passed courses

        course = Course.objects.create(name="course1", code=1, department=department, unit=3, table=table,
                                       is_starred=True)
        response = self.client.post('/graduation/', {"group": 1}, format='json')
        expected_response = [{
            "id": course.code,
            "name": course.name,
            "is_starred": course.is_starred,
            "is_passed": False
        }]
        self.assertEqual(json.loads(response.content)['user_courses'], expected_response)

        # test chart table course list with no passed courses

        UserPassed.objects.create(user=user).courses.add(course)
        response = self.client.post('/graduation/', {"group": 1}, format='json')
        expected_response = [{
            "id": course.code,
            "name": course.name,
            "is_starred": course.is_starred,
            "is_passed": True
        }]
        self.assertEqual(json.loads(response.content)['user_courses'], expected_response)

    def test_add_passed_course(self):
        department = Department.objects.create(name="test_dep")
        user = User.objects.create(username='test', password='1234', department=department)
        self.client.force_login(user=user)
        table = ChartTable.objects.create(dep=department, code=1)
        course = Course.objects.create(name="course1", code=1, department=department, unit=3, table=table,
                                       is_starred=True)
        data = {"passed_courses": [course.code]}
        response = self.client.post('/add_passed_course/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserPassed.objects.filter(user=user).count(), 1)
        self.assertEqual(UserPassed.objects.filter(user=user).first().courses.count(), 1)

    def test_remove_passed_course(self):
        department = Department.objects.create(name="test_dep")
        user = User.objects.create(username='test', password='1234', department=department)
        self.client.force_login(user=user)
        table = ChartTable.objects.create(dep=department, code=1)
        course1 = Course.objects.create(name="course1", code=1, department=department, unit=3, table=table,
                                        is_starred=True)
        course2 = Course.objects.create(name="course2", code=2, department=department, unit=3, table=table,
                                        is_starred=True)
        user_passed = UserPassed.objects.create(user=user)
        user_passed.courses.add(course1)
        user_passed.courses.add(course2)
        data = {"passed_courses": [course1.code]}
        response = self.client.post('/add_passed_course/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserPassed.objects.filter(user=user).count(), 1)
        self.assertEqual(UserPassed.objects.filter(user=user).first().courses.count(), 1)

        # test remove all passed users
        data = {"passed_courses": []}
        response = self.client.post('/add_passed_course/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserPassed.objects.filter(user=user).count(), 1)
