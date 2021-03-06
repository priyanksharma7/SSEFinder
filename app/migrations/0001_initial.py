# Generated by Django 3.1.7 on 2021-05-08 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_num', models.PositiveIntegerField(unique=True)),
                ('patient_name', models.CharField(max_length=200)),
                ('id_num', models.CharField(max_length=20, unique=True)),
                ('date_of_birth', models.DateField()),
                ('date_of_onset', models.DateField()),
                ('date_of_confirmation', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue_name', models.CharField(max_length=200)),
                ('venue_location', models.CharField(max_length=200)),
                ('x_coordinate', models.FloatField()),
                ('y_coordinate', models.FloatField()),
                ('address', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('infector', models.BooleanField(default=False, editable=False)),
                ('infected', models.BooleanField(default=False, editable=False)),
                ('description', models.TextField()),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.case')),
            ],
        ),
        migrations.CreateModel(
            name='CHPuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_number', models.CharField(max_length=6)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'CHP User',
                'verbose_name_plural': 'CHP Users',
            },
        ),
    ]
