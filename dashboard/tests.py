from datetime import timedelta
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone

from academics.models import School, ClassRoom, Subject
from accounts.models import TeacherProfile, StudentProfile
from tasks.models import Task
from dashboard import services


class DashboardServicesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.school = School.objects.create(name='Test High')

        # Admin
        self.admin = User.objects.create_superuser('admin', 'admin@test.local', 'adminpass')

        # Teacher
        self.teacher_user = User.objects.create_user(username='teacher1', password='pass')
        self.teacher = TeacherProfile.objects.create(user=self.teacher_user, school=self.school)

        # Student
        self.student_user = User.objects.create_user(username='student1', password='pass')
        self.student = StudentProfile.objects.create(user=self.student_user, school=self.school, roll_number='R1')

        # Class
        self.classroom = ClassRoom.objects.create(name='Grade 10', school=self.school, class_teacher=self.teacher)
        self.classroom.students.add(self.student)

        # Subject
        self.subject = Subject.objects.create(name='Physics', code='PHY1')
        self.subject.teachers.add(self.teacher)
        self.subject.classes.add(self.classroom)

    def test_role_redirect_teacher(self):
        self.client.login(username='teacher1', password='pass')
        resp = self.client.get('/dashboard/redirect/')
        self.assertRedirects(resp, '/dashboard/teacher/')

    def test_role_redirect_student(self):
        self.client.login(username='student1', password='pass')
        resp = self.client.get('/dashboard/redirect/')
        self.assertRedirects(resp, '/dashboard/student/')

    def test_role_redirect_admin(self):
        self.client.login(username='admin', password='adminpass')
        resp = self.client.get('/dashboard/redirect/')
        self.assertRedirects(resp, '/admin/')

    def test_student_task_buckets_and_workload(self):
        # Create 2 tasks
        t1 = Task.objects.create(
            title='Task 1',
            subject=self.subject,
            teacher=self.teacher,
            class_assigned=self.classroom,
            due_date=timezone.now() + timedelta(hours=5),
            estimated_hours=2.0,
            difficulty='medium',
        )
        t2 = Task.objects.create(
            title='Task 2',
            subject=self.subject,
            teacher=self.teacher,
            class_assigned=self.classroom,
            due_date=timezone.now() + timedelta(hours=10),
            estimated_hours=2.0,
            difficulty='hard',
        )

        buckets = services.student_task_buckets(self.student)
        self.assertEqual(len(buckets['all_tasks']), 2)
        self.assertEqual(len(buckets['pending']), 2)

        conflicts = services.deadline_conflicts(self.student, window_hours=24)
        self.assertTrue(conflicts['conflict'])
        self.assertEqual(conflicts['total_hours'], 4.0)

    def test_teacher_dashboard_stats(self):
        stats = services.teacher_dashboard_stats(self.teacher)
        self.assertEqual(stats['total_classes'], 1)
        self.assertEqual(stats['total_students'], 1)

