from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
# Create your models here.

PAYMENT_METHOD = (
    ('HBL', 'Habib Bank Limited'),
    ('UBL', 'United Bank Limited'),
    ('MCB', 'Muslim Commerial Bank')
)


class Tournament(models.Model):
    slug = models.SlugField(max_length=50)
    organizer = models.CharField(max_length=50, default="Ground ESports")
    image = models.ImageField(blank=True, null=True, upload_to='Pics')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    slots = models.IntegerField(default=100)
    entry_fee = models.FloatField()
    prize_pool = models.FloatField()
    last_date = models.DateField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('core:Detail', kwargs={
            'slug' : self.slug
        })
    
    def get_registeration_url(self):
        return reverse('core:Register', kwargs={
            'slug' : self.slug
        })

    def get_entry_fee(self):
        return self.entry_fee
    

class Teams(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=50)
    team_tag = models.CharField(max_length=50)
    team_number = models.CharField(max_length=15)
    
    player1_ign = models.CharField(max_length=50)
    player1_id = models.CharField(max_length=11)
    
    player2_ign = models.CharField(max_length=50)
    player2_id = models.CharField(max_length=11)
    
    player3_ign = models.CharField(max_length=50)
    player3_id = models.CharField(max_length=11)
    player4_ign = models.CharField(max_length=50)
    player4_id = models.CharField(max_length=11)

    player5_ign = models.CharField(max_length=50, null=True, blank=True)
    player5_id = models.CharField(max_length=11, null=True, blank=True)

    payment_method = models.CharField(max_length=3, choices=PAYMENT_METHOD)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, null=True, blank=True)
    registered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team_name} in {self.tournament.title}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    card_number = models.CharField(max_length=16)
    tournament_fee = models.FloatField()
    amount = models.FloatField()
    paid_date = models.DateField()
    


    def __str__(self):
        return f"{self.user.username} paid ${self.amount}"




class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    message = models.TextField(max_length=500)

    def __str__(self):
        return self.name