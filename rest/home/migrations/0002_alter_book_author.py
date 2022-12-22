# Generated by Django 3.2.16 on 2022-12-22 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(blank=True, max_length=100, on_delete=django.db.models.deletion.CASCADE, to='home.author', verbose_name='Автор'),
        ),
    ]