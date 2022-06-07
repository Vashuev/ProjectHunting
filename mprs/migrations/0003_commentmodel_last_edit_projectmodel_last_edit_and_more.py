# Generated by Django 4.0.5 on 2022-06-07 12:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mprs', '0002_projectmodel_url_projectmodel_votecount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentmodel',
            name='last_edit',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='projectmodel',
            name='last_edit',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='replymodel',
            name='last_edit',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
