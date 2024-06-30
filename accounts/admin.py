from django.contrib import admin
from .models import *


class AttendedStudentsInline(admin.TabularInline):
    model = AttendedStudents
    extra = 0


@admin.register(SetOfExams)
class SetOfExamsAdmin(admin.ModelAdmin):
    list_display = ('examname', 'student_count')

    inlines = [
        AttendedStudentsInline,
    ]

    def student_count(self, obj):
        return obj.att_set.count()
    student_count.short_description = 'Number of Students'

admin.site.register(AttendedStudents)
# Register your models here.


admin.site.register(Questions)
admin.site.register(CustomUser)
admin.site.register(Category_questions)
admin.site.register(QuestionAnswer)
admin.site.register(Result)
admin.site.register(Students)
admin.site.register(ExamAssign)
admin.site.register(Answers)
admin.site.register(Score)
