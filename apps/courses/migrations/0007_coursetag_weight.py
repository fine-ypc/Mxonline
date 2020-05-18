# Generated by Django 2.2 on 2020-05-05 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_coursetag'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursetag',
            name='weight',
            field=models.CharField(choices=[('d', '低'), ('z', '中'), ('g', '高')], default='d', max_length=1, verbose_name='权重'),
        ),
    ]
