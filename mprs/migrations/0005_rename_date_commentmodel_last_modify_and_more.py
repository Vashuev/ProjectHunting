# Generated by Django 4.0.5 on 2022-06-07 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mprs', '0004_remove_commentmodel_last_edit_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commentmodel',
            old_name='date',
            new_name='last_modify',
        ),
        migrations.RenameField(
            model_name='projectmodel',
            old_name='last_edit',
            new_name='last_modify',
        ),
        migrations.RenameField(
            model_name='replymodel',
            old_name='date',
            new_name='last_modify',
        ),
    ]
