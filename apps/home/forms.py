#[ ]: upload file to server

from django import forms

from .models import FirmwareFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = FirmwareFile
        fields = ('file',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'id': 'upload_input', 'hidden': True})
        self.fields['file'].label = ''


    # file = forms.FileField(widget=forms.FileInput(attrs={'multiple': True, 'id': 'upload_input','hidden': True}), label='')

# define delete file form
class Deletefileform(forms.Form):
    pass
