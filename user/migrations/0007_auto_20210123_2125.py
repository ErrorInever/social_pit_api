# Generated by Django 3.1.5 on 2021-01-23 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210123_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpostrelation',
            name='rate',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Very bad'), (2, 'Bad'), (3, 'Normal'), (4, 'Good'), (5, 'Amazing')], null=True),
        ),
    ]