# Generated by Django 5.2.4 on 2025-07-11 16:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('due_date', models.DateField()),
                ('prio', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=15)),
                ('status', models.CharField(choices=[('todo', 'To-do'), ('in_progress', 'In progress'), ('review', 'Review'), ('done', 'Done')], max_length=15)),
                ('assignees', models.ManyToManyField(related_name='tickets', to=settings.AUTH_USER_MODEL)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='dashboard_app.board')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard_app.ticket')),
            ],
        ),
    ]
