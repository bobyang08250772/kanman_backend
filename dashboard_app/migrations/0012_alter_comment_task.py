# Generated by Django 5.2.4 on 2025-07-12 10:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0011_task_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='dashboard_app.task'),
        ),
    ]
