# Generated by Django 5.0.6 on 2024-05-19 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_groups_customuser_user_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questions',
            name='answer',
        ),
        migrations.AddField(
            model_name='questions',
            name='ans1',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='ans2',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='ans3',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='ans4',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='correct_ans',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Answers',
        ),
    ]
