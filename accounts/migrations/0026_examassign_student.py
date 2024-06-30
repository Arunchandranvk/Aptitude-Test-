# Generated by Django 5.0.6 on 2024-06-08 05:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_remove_examassign_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='examassign',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stu_exam', to='accounts.students'),
        ),
    ]