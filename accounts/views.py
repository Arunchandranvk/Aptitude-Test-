from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,CreateView,FormView,View
from .models import *
from .forms import *
from django.urls import reverse_lazy
import random
from django.http import HttpResponse
from django.contrib.auth import login,authenticate
from .backends import CustomUserBackend
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import logout
from django.forms import modelformset_factory
import random
# Create your views here.

@receiver(post_save, sender=Students)
def create_user_from_student(sender, instance, created, **kwargs):
    if created:
        # User = get_user_model()
        CustomUser= get_user_model()
        student=instance
        email = instance.email
        password = 'luminar@123'  # Set your desired default password here
        name=instance.name        
        CustomUser.objects.create_user(email=email, password=password,name=name,student=student)
        



class AddStudent(TemplateView):
    template_name='addstudent.html'
    # model=Students
    # form_class=StudentForm 
    # success_url=reverse_lazy('addstu')  

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     messages.success(self.request, 'Student added successfully!')
    #     return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batch']=Batchs.objects.all()
        context['course']=Courses.objects.all()
        context['stu']=AttendedStudents.objects.all()
        context['cat']=Category_questions.objects.all()
        return context
    

class BatchsView(CreateView):
    template_name='batch.html'
    model=Batchs
    form_class=BatchForm 
    success_url=reverse_lazy('batch')  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batch']=Batchs.objects.all()
        return context

class CourseView(CreateView):
    template_name='course.html'
    model=Courses
    form_class=CourseForm 
    success_url=reverse_lazy('cou')  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course']=Courses.objects.all()
        return context

class TrainerView(CreateView):
    template_name='trainer.html'
    model=Trainers
    form_class=TrainerForm 
    success_url=reverse_lazy('trainer') 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trainer']=Trainers.objects.all()
        context['course']=Courses.objects.all()
        return context 
    

class CategoryView(CreateView):
    template_name='category.html'
    model=Category_questions
    form_class=CategoryForm 
    success_url=reverse_lazy('catall')  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat']=Category_questions.objects.all()
        return context
    

class MachineTestView(CreateView):
    template_name='machinetest.html'
    model=MachineTest
    form_class=MachineTestForm 
    success_url=reverse_lazy('machinetest')  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test']=MachineTest.objects.all()
        return context

class LoginView(FormView):
    template_name="login.html"
    form_class=LogForm
    def post(self,request,*args,**kwargs):
        log_form=LogForm(data=request.POST)
        if log_form.is_valid():  
            email=log_form.cleaned_data.get('email')
            print(email)
            password=log_form.cleaned_data.get('password')
            print(password)
            user=authenticate(request,email=email,password=password)
            print(user)
            if user: 
                
                login(request,user)
                if request.user.is_superuser:
                    return redirect('ah')
                else:
                    return redirect('h')
            else:
                return render(request,'login.html',{"form":log_form})
        else:
            return render(request,'login.html',{"form":log_form}) 
        

class RegView(CreateView):
     form_class=RegForm
     template_name="reg.html"
     model=CustomUser
     success_url=reverse_lazy("log")  

     def form_valid(self, form):
        response = super().form_valid(form)
        return response

     def form_invalid(self, form):
        print(form.errors)  # Print form errors to the console for debugging
        return super().form_invalid(form)

class Home(TemplateView):
    template_name="index.html"

class AdminHome(TemplateView):
    template_name="adminhome.html"



class CategoryExam(TemplateView):
    template_name="set_of_exams.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=CustomUser.objects.get(id=self.request.user.id)
        print(user)
        student=Students.objects.get(id=user.student_id)
        print(student)
        context['data']=ExamAssign.objects.filter(student=student)
        return context

class CategoryResults(TemplateView):
    template_name="set_of_results.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=CustomUser.objects.get(id=self.request.user.id)
        print(user)
        student=Students.objects.get(id=user.student_id)
        print(student)
        context['data']=ExamAssign.objects.filter(student=student)
        return context


class ExamView(TemplateView):
    template_name="exam.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id=kwargs.get('pk')
        stu=kwargs.get('stu')
        print('set',stu)
        print(id)
        # print(id)
        cat=Questions.objects.filter(category=id)
        print(cat)
        stu=AttendedStudents.objects.get(id=stu)
        print("=====",stu)
        print(stu.set.id)
        set=SetOfExams.objects.get(id=stu.set.id)
        print(set.cat.all())
        for i in set.cat.all():
            print(i)
            context['questions']= Questions.objects.filter(category=i)
            print('kkkk',Questions.objects.filter(category=i))
        context['set']=SetOfExams.objects.get(id=stu.set.id)
        context['stu']=AttendedStudents.objects.get(id=stu.id)
        
        context['category']=Category_questions.objects.get(id=id)
        return context    
    


@login_required
@require_POST
def submit_quiz(request, *args, **kwargs):
    total_questions = len([key for key in request.POST.keys() if key.startswith('answer')])
    score = 0
    try:
        id = kwargs.get('pk')
        print(id)
        stu = AttendedStudents.objects.get(id=id)
        cat_id = SetOfExams.objects.get(id=stu.set.id)
        
        for key in request.POST.keys():
            if key.startswith('answer'):
                question_id = key[len('answer'):]
                selected_answer = request.POST.get(key)
                question = Questions.objects.get(id=question_id)
                
                is_correct = (question.correct_ans == selected_answer)
                Answers.objects.create(
                    user=stu,
                    question=question,
                    ans=selected_answer if selected_answer else "None",
                    cat=question.category,
                    set=cat_id,
                    is_correct=is_correct
                )
                
                if is_correct:
                    score += 1
        
        Score.objects.create(user=stu, set=cat_id, score=score)
        messages.success(request, f"Quiz submitted successfully! Your score: {score}")
        return redirect('stresult')
        
    except Questions.DoesNotExist:
        messages.error(request, "Invalid question. Please try again.")
        return redirect('createexam')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('createexam')

class ResultsView(TemplateView):
    template_name='results.html'
    def get_context_data(self, **kwargs):
        id=kwargs.get('pk')
        stu=AttendedStudents.objects.get(id=id)
        context = super().get_context_data(**kwargs)
        try:
            context['score']=Score.objects.get(set=stu.set,user=stu)
        except:
            context['score']="Exam Not Attended"
        set=SetOfExams.objects.get(id=stu.set.id)
        context['ans']=Answers.objects.filter(set=set,user=stu)
        print(Answers.objects.filter(set=set,user=stu))
        return context


class Tryagain(View):
    def post(self,request,**kwargs):
        id=kwargs.get('pk')
        Result.objects.get(cat=id,user=request.user).delete()
        QuestionAnswer.objects.filter(cat=id,user=request.user).delete()
        return redirect('cat')
    
def add_category_to_student(request, student_id):
    student = get_object_or_404(Students, pk=student_id)
    
    if request.method == 'POST':
        selected_categories = request.POST.getlist('categories')
        exam_assign = ExamAssign.objects.create(student=student)
        exam_assign.cat.clear()
        for category_id in selected_categories:
            category = get_object_or_404(Category_questions, pk=category_id)
            exam_assign.cat.add(category)
        
        exam_assign.save()
        
    return redirect('addstu')



class LogOut(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("log")
    

class AdminResultView(TemplateView):
    template_name='adminresultview.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stu = AttendedStudents.objects.all()
        # student_list = []  # Initialize an empty list to store students
        # for i in stu:
            # students = CustomUser.objects.filter(student_id=i.id)
            # student_list.extend(students)  # Append students to the list
        context['students'] = stu # Assign the list to the context
        return context
    
class AdminScoreView(TemplateView):
    template_name='scorestudent.html'
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        id=kwargs.get('pk')
        print(id)
        context['result']=Result.objects.filter(user=id)
        return context
    

class Aptitude_Questions(TemplateView):
    template_name='aptitudequestions.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id=kwargs.get('pk')
        cat=Category_questions.objects.get(id=id)
        print(cat.id)
        context['cat']=cat
        context['ques']=Questions.objects.filter(category=cat)
        return context
    

# class QuestionView(View):

def QuestionView(request, pk):
    category = Category_questions.objects.get(id=pk)
    print(category)
    num_forms = int(request.GET.get('num_forms', 3))
    QuestionsFormSet = modelformset_factory(Questions, form=QuestionsForm, extra=num_forms)
    
    if request.method == 'POST':
        formset = QuestionsFormSet(request.POST, request.FILES, queryset=Questions.objects.none())
        # print(formset)
        if formset.is_valid():
            print('valid')
            instances = formset.save(commit=False)
            for instance in instances:
                # instance.category = category.id
                instance.save()
            return redirect('aptitude',pk=category.id)  # Replace 'aptitude' with the appropriate URL name
    else:
        formset = QuestionsFormSet(queryset=Questions.objects.none())

    return render(request, 'Addquestions.html', {'formset': formset, 'category': category})


# class QuestionView(CreateView):
#     template_name = 'Addquestions.html'
#     model = Questions
#     form_class = QuestionsForm
#     success_url = reverse_lazy('aptitude')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         pk = self.kwargs.get('pk')
#         if pk:
#             cat = Category_questions.objects.get(id=pk)
#             context['cat'] = cat

#         num_forms = int(self.request.GET.get('num_forms', 2))
#         QuestionsFormSet = modelformset_factory(Questions, form=QuestionsForm, extra=num_forms)
        
#         if self.request.POST:
#             context['formset'] = QuestionsFormSet(self.request.POST, self.request.FILES, queryset=Questions.objects.none())
#         else:
#             context['formset'] = QuestionsFormSet(queryset=Questions.objects.none())
#         return context

#     def form_valid(self, form):
#         print('hii')
#         context = self.get_context_data()
#         formset = context['formset']
#         if formset.is_valid():
#             instances = formset.save(commit=False)
#             for instance in instances:
#                 instance.category = Category_questions.objects.get(id=self.kwargs.get('pk'))
#                 instance.save()
#             return super().form_valid(form)
#         else:
#             return self.render_to_response(self.get_context_data(form=form, formset=formset))



class DeleteExamView(View):
    def get(self,req,*args,**kwargs):
       id=kwargs.get('pk')
       dl=Category_questions.objects.get(id=id)
       dl.delete()
       return redirect('catall')

class DeleteQuestionsView(View):
    def get(self,req,*args,**kwargs):
       id=kwargs.get('pk')
       dl=Questions.objects.get(id=id)
       dl.delete()
       print(dl.category.id)
       return redirect('aptitude',pk=dl.category.id)
    

def exam_view(request):
    if request.method == 'POST':
        exam=request.POST.get('examname')
        # duration=request.POST.get('duration')
        selected_categories = request.POST.getlist('categories')
        exam_assign = SetOfExams.objects.create(examname=exam)
        exam_assign.exam_link = request.build_absolute_uri(f'/accounts/detailsofstudents/{exam_assign.uuid}/')
        exam_assign.cat.clear()
        for category_id in selected_categories:
            category = get_object_or_404(Category_questions, pk=category_id)
            exam_assign.cat.add(category)
        exam_assign.save()
        
    return redirect('exam')

class CreateExamView(TemplateView):
    template_name='createexam.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat']=Category_questions.objects.all()
        context['exam']=SetOfExams.objects.all()
        exam=SetOfExams.objects.all()
        exam_counts = {}
        for exam in exam:
            set_of_exam = get_object_or_404(SetOfExams, id=exam.id)
            student_count = set_of_exam.att_set.count()
            exam_counts[exam.id] = student_count
        context['exam_counts'] = exam_counts
        return context
    

class DetailsStudentsView(CreateView):
    template_name='filldetailsof_students.html'
    model=AttendedStudents
    form_class=AttendedStudentsForm
    print(form_class)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id=self.kwargs.get('pk')
        print(id)
        set=SetOfExams.objects.get(uuid=id)
        context['set']=set
        context['course']=Courses.objects.all()
        context['batch']=Batchs.objects.all()
        return context
    
    def form_valid(self, form):
        self.object = form.save()  # Save the form and get the instance
        return super().form_valid(form)
    
    
    def get_success_url(self):
        return reverse_lazy('startexam' ,kwargs={'pk':self.object.pk} )
   


class StartExamPage(TemplateView):
    template_name='startexam.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id=kwargs.get('pk')
        context['student']=AttendedStudents.objects.get(id=id)
        stu=AttendedStudents.objects.get(id=id)
        print(stu.set.id)
        context['set']=SetOfExams.objects.get(id=stu.set.id)
        return context
    

class DeleteExamSetView(View):
    def get(self,req,*args,**kwargs):
       id=kwargs.get('pk')
       dl=SetOfExams.objects.get(id=id)
       dl.delete()
       return redirect('exam')
    

class ExamSetDetailsView(TemplateView):
    template_name='examset_details.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id=kwargs.get('pk')
        set_of_exam = get_object_or_404(SetOfExams, id=id)
        student_count = set_of_exam.att_set.count()
        context['count']=student_count
        context['examset']=SetOfExams.objects.get(id=id)
        context['students']=AttendedStudents.objects.filter(set=set_of_exam)
        return context
    

class QuestionsView(TemplateView):
    template_name='questions.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id=self.kwargs.get('pk')
        cat=Category_questions.objects.get(id=id)
        print(cat.id)
        context['cat']=cat
        context['question']=Questions.objects.filter(category=cat)
        return context


class AttendExamPage(TemplateView):
    template_name = 'examattendingpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = kwargs.get('pk')
        student = get_object_or_404(AttendedStudents, id=id)
        set_of_exams = student.set
        all_questions = []
        for category in set_of_exams.cat.all():
            questions_in_category = Questions.objects.filter(category=category)
            all_questions.extend(questions_in_category)

        questions = random.sample(all_questions,min(len(all_questions),50))

        context['student'] = student
        context['set'] = set_of_exams
        context['questions'] = questions

        return context
    

class StudentResultsView(TemplateView):
    template_name='studentresultview.html'
    def get_context_data(self, **kwargs):
        id=kwargs.get('pk')
        stu=AttendedStudents.objects.get(id=id)
        context = super().get_context_data(**kwargs)
        try:
            context['score']=Score.objects.get(set=stu.set,user=stu)
        except:
            context['score']="Exam Not Attended"
        set=SetOfExams.objects.get(id=stu.set.id)
        context['ans']=Answers.objects.filter(set=set,user=stu)
        print(Answers.objects.filter(set=set,user=stu))
        return context