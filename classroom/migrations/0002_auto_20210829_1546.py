# Generated by Django 3.2.6 on 2021-08-29 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stream',
            options={'ordering': ('-id',)},
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='text',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='testsubmission',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]