from django import forms
"""
Forms for upload csvs
"""
class UploadLibro1ExampleForm(forms.Form):
    file = forms.FileField()