from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager
import uuid
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"
        

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("app:posts_by_category", args=[self.slug])

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts"
    )
    content = CKEditor5Field('Text', config_name='extends')
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    attachment = models.FileField(upload_to="media/", blank=True, null=True)
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    
    indexes = [
        models.Index(fields=["-created_at"]),
        models.Index(fields=["published", "-created_at"]),
    ]
    
    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            # ensure unique
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("app:post_detail", args=[self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
    class Meta:
        indexes = [
            models.Index(fields=["post", "-created_at"]),
            models.Index(fields=["approved", "-created_at"]),
        ]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # email = models.EmailField(unique=False, blank=True, null=True)
    website = models.URLField(blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    twitter = models.URLField(blank=True )

    def __str__(self):
        return self.user.username
