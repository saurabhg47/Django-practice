from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Candidate(models.Model):

    """
    Model for candidate
    """
    email = models.EmailField(max_length=75, unique=True)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Rating(models.Model):
    """
    Model for save given Rating to Candidates
    """
    interviewer = models.ForeignKey(User, db_index=True)
    candidate = models.ForeignKey(Candidate, db_index=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
