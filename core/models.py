from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
	titulo = models.CharField(max_length=30)
	file = models.FileField(upload_to='photos')
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.titulo

