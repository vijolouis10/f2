# Generated by Django 4.2 on 2023-05-09 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_variation_value_variation_size_and_more'),
        ('cart', '0003_cart_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='variations',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.variation'),
        ),
    ]
