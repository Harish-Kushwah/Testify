# Generated by Django 4.2.3 on 2023-08-15 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0036_testpaperset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionset',
            name='test_paper_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Test.testpaperset'),
        ),
    ]
