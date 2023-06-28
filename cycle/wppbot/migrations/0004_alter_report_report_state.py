# Generated by Django 4.2.2 on 2023-06-25 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wppbot', '0003_alter_report_report_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report_state',
            field=models.CharField(choices=[('AWCT', 'Awaiting Category'), ('AWDC', 'Awaiting Description'), ('CFDC', 'Awaiting Description'), ('AWLC', 'Awaiting Localization'), ('ASLN', 'Notifying User'), ('ASLC', 'Awaiting Confirmation'), ('DONE', 'Done')], default='AWCT', max_length=4),
        ),
    ]