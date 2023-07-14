# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calendarid', models.PositiveIntegerField(db_index=True)),
                ('campus', models.CharField(max_length=3)),
                ('name', models.CharField(default=None, max_length=255)),
                ('last_updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'accountsynchr_gcalendar',
                'unique_together': {('calendarid', 'campus')},
            },
        ),
    ]
