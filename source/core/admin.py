from planner.core.models import Institution, Course, Subject, Group, Field, Prerequisite, UserProfile
from django.contrib import admin

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'available_in_first_semester', 'available_in_second_semester', 'available_in_summer_semester')
    list_editable = ('available_in_first_semester', 'available_in_second_semester', 'available_in_summer_semester')
    search_fields = ['code', 'name', 'thai_name', 'description', 'thai_description']

admin.site.register(Institution)
admin.site.register(Course)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Group)
admin.site.register(Field)
admin.site.register(Prerequisite)
admin.site.register(UserProfile)
