
from django.db import models
from django.urls import reverse

class Company(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define primary key
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class registeredUsers(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    company = models.ManyToManyField(Company, blank=True)

    def __str__(self):
        return self.username
    

class Subscriber(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define primary key
    user = models.ForeignKey(registeredUsers, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'company')

    def __str__(self):
        return f"{self.user.username} - {self.company.name}"

class Source(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define primary key
    user = models.ForeignKey(registeredUsers, on_delete=models.CASCADE, default=None)
    source_name = models.CharField(max_length=500, default=None)
    source_url = models.URLField(unique=True, default=None)
    company = models.ManyToManyField(Company, blank=True)  # Optional company association

    class Meta:
        unique_together = ('user', 'source_url')  # Ensures unique URL per user

    def __str__(self):
        return f"{self.user.username} - {self.source_name}"

class Story(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define primary key
    title = models.CharField(max_length=500)
    published_date = models.DateTimeField()
    body_text = models.TextField()
    url = models.URLField(unique=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='stories')
    company = models.ManyToManyField(Company, blank=True, related_name='stories')  # Optional company association
    client = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='client_stories')  # Client association for manual stories
    created_by = models.ForeignKey(registeredUsers, on_delete=models.CASCADE, related_name='created_stories', default=None)

    class Meta:
        unique_together = ('url', 'client')  # Ensures unique URL per client (manual stories)

    def __str__(self):
        return f"{self.title} ({self.source.source_name})"

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'pk': self.pk})
