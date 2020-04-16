from django import forms

class LinkForm(forms.Form):
    link = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Video Link Here'}) , label = False)


class ConvertLink(forms.Form):
    ConvertLink = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter video Link to convert Here'}) , label = False)