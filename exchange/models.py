from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# Create your models here.

class Game(models.Model):
    opponent = models.CharField(max_length=200)
    game_dt = models.DateTimeField()

    def __str__(self):
        return self.opponent

    def is_upcoming(self):
        return self.game_dt >= timezone.now() - datetime.timedelta(days = 7)



class TicketOffering(models.Model):

    HILL = 'Hill'
    UPPER = 'Upper'
    LOWER = 'Lower'

    LOCATION_CHOICES = (
        (HILL, 'Hill'),
        (UPPER, 'Upper Deck'),
        (LOWER, 'Lower Deck'),
    )
    
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    username = models.CharField(max_length=200)
    location = models.CharField(max_length=6, choices=LOCATION_CHOICES)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{} | {} | {}".format(str(self.price), self.game, self.location)

    class Meta:
        ordering = ['price']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
