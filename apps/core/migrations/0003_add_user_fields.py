# Generated by Django 5.1.4 on 2024-12-23 23:25

from django.db import migrations, models
import django.utils.timezone
import uuid


def generate_uuid(apps, schema_editor):
    CustomUser = apps.get_model('core', 'CustomUser')
    for user in CustomUser.objects.all():
        user.uuid = uuid.uuid4()
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_customuser_options_customuser_created_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier for this user', null=True, verbose_name='UUID'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time when this user was created', verbose_name='Created Date'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, help_text='Date and time when this user was last updated', verbose_name='Updated Date'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='notes',
            field=models.TextField(blank=True, help_text='Optional notes about this user', verbose_name='Notes'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='metadata',
            field=models.JSONField(blank=True, default=dict, help_text='Additional data stored as JSON', verbose_name='Metadata'),
        ),
        migrations.RunPython(generate_uuid, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='customuser',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier for this user', unique=True, verbose_name='UUID'),
        ),
    ]
