from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)
admin.site.register(UserProfile)
# Register your models here.
