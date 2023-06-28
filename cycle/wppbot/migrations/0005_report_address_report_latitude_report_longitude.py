# Generated by Django 4.2.2 on 2023-06-25 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wppbot', '0004_alter_report_report_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='address',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='report',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='longitude',
            field=models.FloatField(default=0),
        ),
    ]