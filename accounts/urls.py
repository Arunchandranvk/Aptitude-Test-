from django.urls import path,register_converter
from .views import *
import uuid

class UUIDConverter:
    regex = '[0-9a-f-]{36}'

    def to_python(self, value):
        return uuid.UUID(value)

    def to_url(self, value):
        return str(value)

register_converter(UUIDConverter, 'uuid')

urlpatterns = [ 
    path('home/',Home.as_view(),name='h'),
    path('adminhome/',AdminHome.as_view(),name='ah'),
    path('reg/',RegView.as_view(),name='reg'),
    path('Aptitudeexam/<int:pk>/<int:stu>/',ExamView.as_view(),name='exams'),
    path('category/',CategoryExam.as_view(),name='cat'),
    path('resultcategory/',CategoryResults.as_view(),name='catresult'),
    path('quiz_submit/<int:pk>/',submit_quiz,name="submit_quiz"),
    path('result/<int:pk>/',ResultsView.as_view(),name="result"),
    path('tryagain/<int:pk>/',Tryagain.as_view(),name='try'),
    path('addstudent/',AddStudent.as_view(),name='addstu'),
    path('batch/',BatchsView.as_view(),name='batch'),
    path('course/',CourseView.as_view(),name='cou'),
    path('trainer/',TrainerView.as_view(),name='trainer'),
    path('examassign/<int:student_id>/',add_category_to_student,name='assignexam'),
    path('logout/',LogOut.as_view(),name='logout'),
    path('resultview/',AdminResultView.as_view(),name='adminresult'),
    path('scoreview/<int:pk>/',AdminScoreView.as_view(),name='scoreadmin'),
    path('categoryall/',CategoryView.as_view(),name='catall'),
    path('aptitude/<int:pk>/',Aptitude_Questions.as_view(),name='aptitude'),
    path('machinetest/',MachineTestView.as_view(),name='machinetest'),
    path('questionadd/<int:pk>/',QuestionView,name='addquestion'),
    path('deleteexam/<int:pk>/',DeleteExamView.as_view(),name='delexam'),
    path('deletequestion/<int:pk>/',DeleteQuestionsView.as_view(),name='delque'),
    path('exam/',CreateExamView.as_view(),name='exam'),
    path('createexam/',exam_view,name='createexam'),
    path('detailsofstudents/<uuid:pk>/',DetailsStudentsView.as_view(),name='detstu'),
    path('startexam/<int:pk>/',StartExamPage.as_view(),name='startexam'),
    path('delexamset/<int:pk>/',DeleteExamSetView.as_view(),name='delexamset'),
    path('examsetdetail/<int:pk>/',ExamSetDetailsView.as_view(),name='detexamset'),
    path('questions/<int:pk>/',QuestionsView.as_view(),name='question'),
    path('examattend/<int:pk>/',AttendExamPage.as_view(),name='attexam'),
    path('studentresult/<int:pk>/',StudentResultsView.as_view(),name='stresult'),
]
