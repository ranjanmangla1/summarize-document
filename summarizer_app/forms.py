# summarizer_app/forms.py
from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     # Override the widget for the 'file' field
        #     self.fields['file'].widget = forms.FileInput()
        #     self.fields['file'].widget.attrs = {'class': 'custom-file-input', 'id': 'custom-file-input'}
        
        def __init__(self, *args, **kwargs):
            self.fields['file'].widget = forms.FileInput()

            self.fields['file'].widget.attrs={'class':'custome-file-input', 'id':'custom-file-input'}


