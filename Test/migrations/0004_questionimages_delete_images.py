# Generated by Django 4.2.3 on 2023-07-21 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0003_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionImages',
            fields=[
                ('question_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('question_title', models.CharField(max_length=100)),
                ('question_image', models.FileField(default=None, max_length=250, null=True, upload_to='question/')),
                ('ans', models.CharField(max_length=2)),
            ],
        ),
        migrations.DeleteModel(
            name='Images',
        ),
    ]
