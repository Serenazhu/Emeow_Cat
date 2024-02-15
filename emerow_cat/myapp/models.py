from django.db import models

# Create your models here.


class Businesses(models.Model):
    Company = models.CharField(max_length=100, db_column='Company')
    Type = models.CharField(max_length=100, db_column='Type')

    class Meta:
        managed = False
        db_table = 'Businesses'


class Representatives(models.Model):
    Reps = models.CharField(max_length=100, db_column='Reps')
    Email = models.CharField(max_length=100, db_column='Email')
    Company = models.CharField(max_length=100, db_column='Company')

    class Meta:
        managed = False
        db_table = 'Representatives'


class Inbox(models.Model):
    Subject = models.CharField(max_length=1000, db_column='Subject')
    Time = models.CharField(max_length=100, db_column='Time')
    Body = models.CharField(max_length=10000, db_column='Body')
    Email = models.CharField(max_length=100, db_column='Email')
    Reps = models.CharField(max_length=100, db_column="Reps")

    class Meta:
        managed = False
        db_table = 'Inbox'


class Sent(models.Model):
    Email = models.CharField(max_length=1000, db_column='Email')
    Time = models.CharField(max_length=100, db_column='Time')
    Body = models.CharField(max_length=10000, db_column='Body')
    Subject = models.CharField(max_length=100, db_column='Subject')

    class Meta:
        managed = False
        db_table = 'Sent'
