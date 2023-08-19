from django import forms

class PlayerSearchForm(forms.Form):
    player_name = forms.CharField(label='Player Name', max_length=100)
    player_rating = forms.IntegerField(label='Player Rating')
