# Generated by Django 4.2.3 on 2023-08-04 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0031_alter_questionrating_question_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userresponse',
            name='question',
        ),
        migrations.DeleteModel(
            name='QuestionExample',
        ),
        migrations.DeleteModel(
            name='TestExample',
        ),
        migrations.DeleteModel(
            name='UserResponse',
        ),
    ]
