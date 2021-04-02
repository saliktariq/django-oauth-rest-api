# Generated by Django 3.0.2 on 2021-04-02 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0003_remove_messages_is_live'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='dislikes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='messages',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='messages',
            name='total_interactions',
            field=models.PositiveIntegerField(default=0),
        ),
    ]