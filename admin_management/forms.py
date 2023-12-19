# forms.py
from django import forms

class AdminActionsForm(forms.Form):
    is_approved = forms.BooleanField(required=False, label='Approve')
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
