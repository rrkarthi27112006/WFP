from django import forms
from .models import Announcement


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message', 'target_class', 'target_all_students']
        widgets = {'message': forms.Textarea(attrs={'rows': 4})}
