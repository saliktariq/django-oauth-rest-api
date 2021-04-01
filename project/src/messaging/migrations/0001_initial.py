# Generated by Django 3.0.2 on 2021-04-01 04:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(choices=[('P', 'Politics'), ('H', 'Health'), ('S', 'Sports'), ('T', 'Tech')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('post_identifier', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('creation_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('expiration_timestamp', models.DateTimeField()),
                ('is_live', models.BooleanField(default=True)),
                ('username', models.CharField(max_length=100)),
                ('topic', models.ManyToManyField(to='messaging.Topics')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_liked', models.BooleanField(default=False)),
                ('is_disliked', models.BooleanField(default=False)),
                ('comment', models.TextField(blank=True)),
                ('username', models.CharField(max_length=100)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messaging.Messages')),
            ],
        ),
    ]
