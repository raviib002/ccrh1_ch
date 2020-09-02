# Generated by Django 2.2.11 on 2020-09-02 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Custom Permission',
                'permissions': (('can_add_case', 'Can Add Case'), ('can_update_case', 'Can Update Case'), ('can_add_follow_up', 'Can Add Follow-up Case'), ('can_delete_follow_up', 'Can Delete Follow-up Case')),
            },
        ),
    ]