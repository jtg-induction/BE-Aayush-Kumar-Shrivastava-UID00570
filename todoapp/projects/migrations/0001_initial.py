# Generated by Django 4.2.5 on 2025-02-04 19:08

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
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Project Name')),
                ('max_members', models.PositiveIntegerField(verbose_name='Max Members')),
                ('status', models.IntegerField(choices=[(0, 'To be started'), (1, 'In progress'), (2, 'Completed')], default=0, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Member')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='Project')),
            ],
            options={
                'unique_together': {('project', 'member')},
            },
        ),
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(related_name='projects', through='projects.ProjectMember', to=settings.AUTH_USER_MODEL, verbose_name='Members'),
        ),
    ]
