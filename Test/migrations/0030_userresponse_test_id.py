# Generated by Django 4.2.3 on 2023-08-03 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0029_remove_userresponse_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresponse',
            name='test_id',
            field=models.BigIntegerField(blank=True, default=None, null=True),
        ),
    ]