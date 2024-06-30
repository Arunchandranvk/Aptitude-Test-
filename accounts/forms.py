# accounts/forms.py
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class LogForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email","class":"form-control","style":"border-radius: 0.75rem; "}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password","class":"form-control","style":"border-radius: 0.75rem; "}))


class RegForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone', 'password1', 'password2']

    name = forms.CharField(label='Name',
        widget=forms.TextInput(attrs={
            "placeholder": "Name",
            "class": "form-control",
            "style": "border-radius: 0.5rem; padding:10px 50px;"
        })
    )
    email = forms.EmailField(label='Email',
        widget=forms.EmailInput(attrs={
            "placeholder": "Email",
            "class": "form-control",
            "style": "border-radius: 0.5rem; padding:10px 50px;"
        })
    )
    phone = forms.CharField(label="Phone",
        widget=forms.TextInput(attrs={
            "placeholder": "Phone",
            "class": "form-control",
            "style": "border-radius: 0.5rem; padding:10px 50px;"
        })
    )
    password1 = forms.CharField(label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "class": "form-control",
            "style": "border-radius: 0.5rem; padding:10px 50px;"
        })
    )
    password2 = forms.CharField(label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm Password",
            "class": "form-control",
            "style": "border-radius: 0.5rem; padding:10px 50px;"
        })
    )

    def label_tag(self, contents=None, attrs=None):
        contents = contents or self.label
        attrs = {'class': 'custom-label'}  
        return super().label_tag(contents, attrs)



class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(QuestionsForm, self).__init__(*args, **kwargs)
        self.fields['question'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Question'
        })
        self.fields['ans1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Option 1'
        })
        self.fields['ans2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Option 2'
        })
        self.fields['ans3'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Option 3'
        })
        self.fields['ans4'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Option 4'
        })
        self.fields['correct_ans'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Correct Answer'
        })
        self.fields['solution'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Solution'
        })



class QuestionAnsForm(forms.ModelForm):
    class Meta:
        model=QuestionAnswer
        fields = '__all__'

class StudentForm(forms.ModelForm):
     class Meta:
          model=Students
          fields=['name','email','course','batch','trainer']
          
class BatchForm(forms.ModelForm):
    class Meta:
        model=Batchs
        fields = '__all__'

class CourseForm(forms.ModelForm):
    class Meta:
        model=Courses
        fields = '__all__'

class TrainerForm(forms.ModelForm):
    class Meta:
        model=Trainers
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category_questions
        fields = '__all__'

class MachineTestForm(forms.ModelForm):
    class Meta:
        model=MachineTest
        fields = '__all__'

class AssignExamForm(forms.ModelForm):
    cat = forms.ModelMultipleChoiceField(
        queryset=Category_questions.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = ExamAssign
        fields = ['cat']
      
class AttendedStudentsForm(forms.ModelForm):
    class Meta:
        model=AttendedStudents
        fields='__all__'