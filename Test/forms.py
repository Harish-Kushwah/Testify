# forms.py
from django import forms
class TestResponseForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(TestResponseForm, self).__init__(*args, **kwargs)
        choices ='abcd'
        self.fields[f'answer_{question.id}'] = forms.ChoiceField(choices=[(i, choice) for i, choice in enumerate(choices)], widget=forms.RadioSelect, required=True)
