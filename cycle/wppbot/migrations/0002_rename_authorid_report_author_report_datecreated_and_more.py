# Generated by Django 4.2 on 2023-06-03 00:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wppbot', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='authorId',
            new_name='author',
        ),
        migrations.AddField(
            model_name='report',
            name='dateCreated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='report',
            name='report_state',
            field=models.CharField(choices=[('AWCT', 'Awaiting Category'), ('AWDC', 'Awaiting Description'), ('AWLC', 'Awaiting Localization'), ('DONE', 'Done')], default='AWCT', max_length=4),
        ),
    ]