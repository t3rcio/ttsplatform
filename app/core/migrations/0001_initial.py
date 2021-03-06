# Generated by Django 4.0.3 on 2022-04-06 21:19

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequestTTS',
            fields=[
                ('ide', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=256)),
                ('text', models.TextField(blank=True, default='', null=True)),
                ('mp3', models.CharField(default='', max_length=1024)),
                ('language', models.CharField(default='pt-br', max_length=256)),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Requisição',
                'verbose_name_plural': 'Requisições',
            },
        ),
    ]
