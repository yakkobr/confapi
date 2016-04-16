from django.db import models



class Confapi(models.Model):
	question = models.CharField(max_length=200)
	