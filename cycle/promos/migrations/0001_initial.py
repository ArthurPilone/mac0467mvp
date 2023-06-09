# Generated by Django 4.2 on 2023-06-04 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wppbot', '0003_alter_report_report_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerAdvert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advert_text', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='PartnerPromotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_text', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='SingleUsePromotionalCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('used', models.BooleanField(default=False)),
                ('related_promotion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='promos.partnerpromotion')),
                ('usedBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wppbot.chatbotuser')),
            ],
        ),
    ]
