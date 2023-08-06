# Generated by Django 4.2.3 on 2023-08-03 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0023_remove_result_test_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionEx',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Test.test')),
            ],
        ),
    ]