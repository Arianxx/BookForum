# Generated by Django 2.0.5 on 2018-09-07 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Discussion', '0006_auto_20180906_2335'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('-create_time',), 'verbose_name': '通知', 'verbose_name_plural': '通知'},
        ),
        migrations.AddField(
            model_name='notification',
            name='is_reply',
            field=models.BooleanField(default=False, verbose_name='是否是回复'),
        ),
    ]