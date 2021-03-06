from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Post, UserPostRelation


class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = ('email', 'is_staff', 'is_active',)
	list_filter = ('email', 'is_staff', 'is_active',)
	fieldsets = (
		(None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
		('Permissions', {'fields': ('is_staff', 'is_active')})
		)
	add_fieldsets = (
		(None, {
			'classes': ('wide'),
			'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)


@admin.register(Post)
class BlogAdmin(admin.ModelAdmin):
	pass

@admin.register(UserPostRelation)
class UserPostRelationAdmin(admin.ModelAdmin):
	pass


admin.site.register(CustomUser, CustomUserAdmin)