# Generated by Django 4.2.3 on 2023-07-30 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0016_alter_candidate_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='profileImage',
            field=models.ImageField(blank=True, default=None, max_length=250, null=True, upload_to='profile_images/'),
        ),
    ]
