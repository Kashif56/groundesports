from django import forms
from .models import Teams

class RForm(forms.ModelForm):
    team_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Team Name'
        }
    ))
    team_tag= forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Team Tag'
        }
    ))

    team_number= forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Team Leader Whastapp Number'
        }
    ))
    
    player1_ign= forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'First Player IGN'
        }
    ))
    player1_id= forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'First Player ID'
        }
    ))
    player2_ign= forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Second Player IGN'
        }
    ))
    player2_id= forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Second Player ID'
        }
    ))
    

    player3_ign= forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Third Player IGN'
        }
    ))
    player3_id= forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Third Player ID'
        }
    ))
    

    player4_ign= forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Foruth Player IGN'
        }
    ))
    player4_id= forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Fourth Player ID'
        }
    ))
    

    player5_ign= forms.CharField(label='', required=False,widget=forms.TextInput(
        attrs={
            'placeholder': 'Fifth Player IGN(optional)'
        }
    ))
    player5_id= forms.CharField(label='', required=False , widget=forms.TextInput(
        attrs={
            'placeholder': 'Fifth Player ID(optional)'
        }
    ))
    
    
    
    
    
    
    
    
    
    
    
    class Meta:
        model = Teams
        fields = [
            'team_name',
            'team_tag',
            'team_number',
            'player1_ign',
            'player1_id',
            'player2_ign',
            'player2_id',
            'player3_ign',
            'player3_id',
            'player4_ign',
            'player4_id', 
            'player5_ign',
            'player5_id',
            'payment_method'
        ]