from django.db import models


class School(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    """Represents a school class/section, e.g. '10-A'."""
    name = models.CharField(max_length=50)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    class_teacher = models.ForeignKey(
        'accounts.TeacherProfile', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='classes_managed'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return self.name

    @property
    def student_count(self):
        return self.students.count()


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    classes = models.ManyToManyField(ClassRoom, related_name='subjects', blank=True)
    teacher = models.ForeignKey(
        'accounts.TeacherProfile', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='subjects_taught'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
