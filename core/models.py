from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
	titulo = models.CharField(max_length=30)
	file = models.FileField(upload_to='photos')
	user = models.ForeignKey(User)

	def delete(self, *args, **kwargs):
		storage, path = self.file.storage, self.file.path
		super(File, self).delete(*args, **kwargs)
		storage.delete(path)

	def __unicode__(self):
		return self.titulo

