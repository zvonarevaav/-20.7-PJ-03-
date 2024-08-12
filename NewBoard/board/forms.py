from django import forms
from .models import Announcement
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AnnouncementForm(forms.ModelForm):
    announcement_text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Announcement
        fields = [
            'announcement_title',
            'announcement_text',
            'author',
            'categories',
        ]

