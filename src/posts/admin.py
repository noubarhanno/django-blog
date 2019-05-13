from django.contrib import admin

# Register your models here.
from .models import Posts

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "updated", "created", "validate"]
	list_display_links = ["updated"]
	list_editable = ["title"]
	list_filter = ["updated", "created"]

	search_fields = ["title", "content"]
	class Meta:
		model = Posts


admin.site.register(Posts, PostModelAdmin)