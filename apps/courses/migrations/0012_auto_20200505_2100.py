# Generated by Django 2.2 on 2020-05-05 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_auto_20200505_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='notice',
            field=models.CharField(default='', max_length=20, verbose_name='课程公告'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='课程'),
        ),
        migrations.AlterField(
            model_name='video',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Lesson', verbose_name='章节'),
        ),
    ]
