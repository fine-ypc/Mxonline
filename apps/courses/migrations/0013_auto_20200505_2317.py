# Generated by Django 2.2 on 2020-05-05 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20200505_2100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseresource',
            old_name='download',
            new_name='file',
        ),
    ]
