# Generated by Django 4.2.3 on 2023-07-30 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0017_candidate_profileimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='about',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='contact_no',
            field=models.TextField(blank=True, default=None, max_length=10, null=True),
        ),
    ]