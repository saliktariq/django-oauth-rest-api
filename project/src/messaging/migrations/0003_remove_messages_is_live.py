# Generated by Django 3.0.2 on 2021-04-01 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_auto_20210401_0558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='is_live',
        ),
    ]