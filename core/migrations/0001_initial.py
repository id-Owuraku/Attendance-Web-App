# Generated by Django 5.0.6 on 2024-06-10 00:03

import django.db.models.deletion
import django_google_maps.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=100)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('event_url', models.URLField(null=True)),
                ('event_name', models.CharField(blank=True, max_length=100)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('location_address', models.CharField(blank=True, max_length=200, null=True)),
                ('geolocation', django_google_maps.fields.GeoLocationField(blank=True, max_length=100, null=True)),
                ('radius', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Radius')),
                ('is_student_id_required', models.BooleanField(default=False)),
                ('is_index_number_required', models.BooleanField(default=False)),
                ('is_student_name_required', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('checkpoint_lat', models.DecimalField(decimal_places=7, max_digits=15, null=True)),
                ('checkpoint_lng', models.DecimalField(decimal_places=7, max_digits=15, null=True)),
                ('related_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.class')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='lecturer_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profile'),
        ),
    ]
