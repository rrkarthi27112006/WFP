from .models import Notification


def create_notification(user, notification_type, message, link=''):
    return Notification.objects.create(
        user=user, notification_type=notification_type, message=message, link=link
    )


def notify_task_assigned(task):
    for student in task.target_students():
        create_notification(
            student.user, 'task_assigned',
            f'New task assigned: "{task.title}" ({task.subject.name})',
            link=f'/tasks/student/{task.id}/',
        )


def notify_new_submission(submission):
    teacher_user = submission.task.teacher.user
    create_notification(
        teacher_user, 'new_submission',
        f'{submission.student.user.get_full_name() or submission.student.user.username} submitted "{submission.task.title}"',
        link=f'/tasks/teacher/{submission.task.id}/',
    )


def notify_reviewed(submission):
    create_notification(
        submission.student.user, 'reviewed',
        f'Your submission for "{submission.task.title}" has been reviewed.',
        link=f'/tasks/student/{submission.task.id}/',
    )
    if submission.feedback:
        create_notification(
            submission.student.user, 'feedback',
            f'New feedback on "{submission.task.title}".',
            link=f'/tasks/student/{submission.task.id}/',
        )


def notify_announcement(announcement):
    from accounts.models import StudentProfile
    if announcement.target_all_students:
        students = StudentProfile.objects.all()
    elif announcement.target_class:
        students = announcement.target_class.students.all()
    else:
        students = StudentProfile.objects.none()

    for student in students:
        create_notification(
            student.user, 'announcement',
            f'New announcement: {announcement.title}',
            link='/notifications/announcements/',
        )



def notify_missing_work(student, teacher_user, count):
    create_notification(
        teacher_user, 'missing_work',
        f'{student.user.get_full_name() or student.user.username} has {count} task(s) with missing work.',
        link='/academics/students/',
    )
