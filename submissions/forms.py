import os
from django import forms
from django.conf import settings
from .models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['text_answer', 'file', 'image']
        widgets = {'text_answer': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your answer here...'})}

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if f:
            ext = os.path.splitext(f.name)[1].lower()
            if ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
                raise forms.ValidationError('Unsupported file type. Allowed: PDF, DOC, DOCX, PPT, PPTX, JPG, PNG.')
            if f.size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
                raise forms.ValidationError(f'File too large. Max size is {settings.MAX_UPLOAD_SIZE_MB} MB.')
        return f

    def clean_image(self):
        img = self.cleaned_data.get('image')
        if img:
            ext = os.path.splitext(img.name)[1].lower()
            if ext not in ('.jpg', '.jpeg', '.png'):
                raise forms.ValidationError('Images must be JPG or PNG.')
        return img


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['marks_obtained', 'feedback', 'is_resubmission_allowed']
        widgets = {'feedback': forms.Textarea(attrs={'rows': 4})}
