from django.db import models

class UserModels(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email_id = models.EmailField()
    birthday = models.DateField()

    class Meta:
        managed = False,
        db_table = 'user'
        app_label='core'
    