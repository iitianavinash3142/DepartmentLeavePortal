# Generated by Django 2.0.5 on 2018-07-13 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0003_auto_20180712_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='applyleave',
            name='TypeOfLeave',
            field=models.CharField(choices=[('Odinary', 'Odinary'), ('Medical', 'Medical'), ('Acedemic', 'Acedemic'), ('Maternity', 'Maternity'), ('paternity', 'paternity')], default='', max_length=255),
        ),
        migrations.AddField(
            model_name='student',
            name='Acedemic',
            field=models.IntegerField(default=30, max_length=3),
        ),
        migrations.AddField(
            model_name='student',
            name='Maternity',
            field=models.IntegerField(default=135, max_length=3),
        ),
        migrations.AddField(
            model_name='student',
            name='Medical',
            field=models.IntegerField(default=15, max_length=3),
        ),
        migrations.AddField(
            model_name='student',
            name='Odinary',
            field=models.IntegerField(default=15, max_length=3),
        ),
        migrations.AddField(
            model_name='student',
            name='Paternity',
            field=models.IntegerField(default=15, max_length=3),
        ),
    ]