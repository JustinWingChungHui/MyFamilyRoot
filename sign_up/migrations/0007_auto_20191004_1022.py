# Generated by Django 2.2.6 on 2019-10-04 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign_up', '0006_signup_ip_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='gender',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('N', 'Non-Binary'), ('O', 'Other'), ('P', 'Prefer Not To Say')], max_length=1),
        ),
    ]
