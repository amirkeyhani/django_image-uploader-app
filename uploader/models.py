from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', validators=[
                              validate_file_extension], upload_to='profile_pics', null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username


class Uploader(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    image = models.ImageField(
        validators=[validate_file_extension], upload_to='images', null=False, blank=False)
    user = models.CharField(max_length=100, null=False, blank=False)
    profile = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    like = models.IntegerField(default=0, blank=True)

    def __str__(self) -> str:
        return f'{self.name} {self.user}'

    def get_absolute_url(self):
        return reverse("image_detail", kwargs={"pk": str(self.pk)})
        # args = [str(self.id)]


class Comment(models.Model):
    image = models.ForeignKey(
        Uploader, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    text = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True, blank=False)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['commented_at']

    def __str__(self) -> str:
        return f'Comment {self.text} by {self.user} with email ID: {self.email}'