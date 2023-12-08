# Generated by Django 4.2.3 on 2023-08-20 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0038_testpaperset_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscussRoom',
            fields=[
                ('discuss_room_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('message', models.TextField(blank=True)),
                ('post_date', models.DateField(auto_now=True)),
                ('post_time', models.TimeField(auto_now=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Test.candidate')),
            ],
        ),
    ]