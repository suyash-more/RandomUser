# Generated by Django 3.2 on 2021-08-11 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='frst_name',
            new_name='first_name',
        ),
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=models.DateField(null=True),
        ),
    ]
