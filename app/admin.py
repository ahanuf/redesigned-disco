from django.contrib import admin
from .models import Category, Post, Comment, Profile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "created_at",
        "updated_at",
        "published",
    )

    list_filter = (
        "published",
        "category",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "title",
        "content",
        "author__username",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    autocomplete_fields = (
        "author",
        "category",
    )

    list_select_related = (
        "author",
        "category",
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "author",
        "created_at",
        "approved",
    )

    list_filter = (
        "approved",
        "created_at",
    )

    search_fields = (
        "content",
        "author__username",
        "post__title",
    )

    autocomplete_fields = (
        "post",
        "author",
    )

    list_select_related = (
        "post",
        "author",
    )

    ordering = ("-created_at",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "joined_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    autocomplete_fields = (
        "user",
    )

    ordering = ("-joined_at",)
    