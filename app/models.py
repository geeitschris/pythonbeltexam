from django.db import models
import re

# Create your models here.


class UserManager(models.Manager):
    def validator(self, data):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(data['first_name']) < 2:
            errors['first_name'] = 'First name should contain at least 2 characters'
        if len(data['last_name']) < 2:
            errors['last_name'] = 'Last name should contain at least 3 characters'
        if len(data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if data['password'] != data['cpassword']:
            errors['password'] = 'Passwords do not match'
        if len(data['email']) == "" or not EMAIL_REGEX.match(data['email']):
            errors['email'] = 'Invalid E-Mail'
        pw = User.objects.filter(email=data['email'])
        if len(pw) > 0:
            errors['email'] = 'Invalid Credentials'
        return errors


class WishManager(models.Manager):
    def validator(self, data):
        errors = {}
        if len(data['name']) < 2:
            errors['name'] = "Name of wish should have at least 3 characters."
        if len(data['description']) < 2:
            errors['description'] = "Name of description should have at least 3 characters."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Wish(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    granted = models.BooleanField(default=False)
    user_wished = models.ForeignKey(
        'User', related_name="wishes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()


class Like(models.Model):
    wish = models.ForeignKey(
        'Wish', related_name='wish_like', on_delete=models.CASCADE)
    user = models.ForeignKey(
        'User', related_name='liked_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
