# Generated by Django 3.1.5 on 2021-01-23 19:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPostRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('rate', models.PositiveSmallIntegerField(choices=[(1, 'Very bad'), (2, 'Bad'), (3, 'Normal'), (4, 'Good'), (5, 'Amazing')])),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
