from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
import uuid
from datetime import timedelta
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, name, password, **extra_fields)

    
class Batchs(models.Model):
    batch=models.CharField(max_length=200)

    def __str__(self):
        return self.batch
    
class Courses(models.Model):
    course=models.CharField(max_length=200)

    def __str__(self):
        return self.course
    
class Trainers(models.Model):
    trainer=models.CharField(max_length=200)
    course=models.ForeignKey(Courses,on_delete=models.CASCADE,related_name='trainer_cou')

    def __str__(self):
        return self.trainer

    
class Students(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(null=True,unique=True)
    batch=models.ForeignKey(Batchs,on_delete=models.CASCADE,related_name="batch_stu")
    trainer=models.ForeignKey(Trainers,on_delete=models.CASCADE,related_name="trainer_stu")
    course=models.ForeignKey(Courses,on_delete=models.CASCADE,related_name="cou_stu")

    def __str__(self):
        return self.name
    


class CustomUser(AbstractBaseUser,PermissionsMixin):
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(unique=True)
    phone=models.IntegerField(null=True,blank=True)
    student=models.OneToOneField(Students,on_delete=models.CASCADE,related_name='stu_user',unique=True,null=True,blank=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    # def save(self, *args, **kwargs):
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    

    def __str__(self):
        return self.email

class Category_questions(models.Model):
    cat=models.CharField(max_length=200)

    def __str__(self):
        return self.cat

class Questions(models.Model):
    question=models.TextField()
    # img=models.FileField(upload_to='question',null=True,blank=True)
    ans1=models.CharField(max_length=100,null=True)
    ans2=models.CharField(max_length=100,null=True)
    ans3=models.CharField(max_length=100,null=True)
    ans4=models.CharField(max_length=100,null=True)
    correct_ans=models.CharField(max_length=100,null=True)
    solution=models.FileField(upload_to="solution",null=True,blank=True)
    category=models.ForeignKey(Category_questions,on_delete=models.CASCADE,related_name='cat_q',null=True)

    def save(self, *args, **kwargs):
        # Ensure correct_ans is one of ans1, ans2, ans3, ans4
        answer_choices = [self.ans1, self.ans2, self.ans3, self.ans4]
        if self.correct_ans not in answer_choices:
            raise ValueError("Correct answer must be one of the provided answer choices.")
        
        super(Questions, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.question
    
class MachineTest(models.Model):
    question=models.TextField()
    # cat=models.ForeignKey(Category_questions,on_delete=models.CASCADE)

    def __str__(self):
        return self.question

class MachineTestAnswer(models.Model):
    question=models.ForeignKey(MachineTest,on_delete=models.CASCADE,related_name='mt_quest')
    ans=models.TextField()
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='test_ans')

    def __str__(self):
        return self.question.question


class QuestionAnswer(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='u_ans')
    question=models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='q_ans')
    ans=models.CharField(max_length=100)
    cat=models.ForeignKey(Category_questions,on_delete=models.CASCADE,related_name='cat_ques',null=True)
    is_correct=models.BooleanField(null=True)

    def __str__(self) -> str:
        return self.question.question
    


class Result(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_result')
    cat=models.ForeignKey(Category_questions,on_delete=models.CASCADE,related_name='cat_quest')
    score=models.IntegerField()

    def __str__(self):
        return self.user.name
    

class ExamAssign(models.Model):
    student=models.ForeignKey(Students,on_delete=models.CASCADE,related_name='stu_exam',null=True)
    cat=models.ManyToManyField(Category_questions,related_name='cat_exam')

class SetOfExams(models.Model):
    cat=models.ManyToManyField(Category_questions)
    examname=models.CharField(max_length=100)
    duration = models.DurationField(default=timedelta(hours=2))
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,null=True)
    exam_link = models.URLField(blank=True, null=True)
    # attendedstudentscount=models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.examname

class AttendedStudents(models.Model):
    set=models.ForeignKey(SetOfExams,on_delete=models.CASCADE,related_name='att_set',null=True)
    name=models.CharField(max_length=200)
    email=models.EmailField(unique=True)
    batch=models.ForeignKey(Batchs,on_delete=models.CASCADE,related_name='att_b')
    course=models.ForeignKey(Courses,on_delete=models.CASCADE,related_name='att_cou',null=True)
    datetime=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
       return  self.name
    

class Answers(models.Model):
    user=models.ForeignKey(AttendedStudents,on_delete=models.CASCADE,related_name='user_ans')
    question=models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='ques_ans')
    ans=models.CharField(max_length=100)
    cat=models.ForeignKey(Category_questions,on_delete=models.CASCADE,related_name='cat_quess',null=True)
    set=models.ForeignKey(SetOfExams,on_delete=models.CASCADE,related_name='set',null=True)
    is_correct=models.BooleanField(null=True)

    def __str__(self) -> str:
        return self.question.question
    

class Score(models.Model):
    set=models.ForeignKey(SetOfExams,on_delete=models.CASCADE,related_name='score')
    user=models.ForeignKey(AttendedStudents,on_delete=models.CASCADE,related_name='set_score')
    score=models.PositiveIntegerField()

    def __str__(self):
       return  self.user