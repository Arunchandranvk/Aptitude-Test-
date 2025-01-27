# Generated by Django 5.0.6 on 2024-05-18 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans', models.CharField(max_length=100)),
                ('ans_img', models.FileField(blank=True, null=True, upload_to='Answers')),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('img', models.FileField(blank=True, null=True, upload_to='question')),
                ('answer', models.ManyToManyField(related_name='q_answer', to='accounts.answers')),
            ],
        ),
    ]
