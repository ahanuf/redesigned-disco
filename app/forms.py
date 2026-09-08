from django import forms
from .models import Post, Comment, Profile
from taggit.forms import TagWidget
from django_ckeditor_5.widgets import CKEditor5Widget

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget())

    class Meta:
        model = Post
        fields = ["title", "category", "tags", "content", "image",'attachment', "published"]
        widgets = {
            "tags": TagWidget(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput()
    )

    class Meta:
        model = Profile
        fields = [
            "bio",
            "avatar",
            "website",
            "twitter",
        ]

        widgets = {
            "bio": forms.Textarea(attrs={"rows": 5}),
            "website": forms.URLInput(),
            "twitter": forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.user:
            self.fields["email"].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=commit)

        email = self.cleaned_data.get("email")

        if profile.user:
            profile.user.email = email
            profile.user.save(update_fields=["email"])

        return profile

