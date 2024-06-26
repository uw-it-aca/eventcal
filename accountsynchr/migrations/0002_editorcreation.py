# Generated by Django 4.2.13 on 2024-06-03 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountsynchr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditorCreation',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('uwnetid', models.CharField(
                    db_index=True, max_length=128, unique=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'accountsynchr_editor_creation',
            },
        ),
    ]
