# Generated by Django 4.2 on 2023-05-25 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_userprofile_pincode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='pincode',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
