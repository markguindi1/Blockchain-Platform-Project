# Generated by Django 2.1.7 on 2019-04-01 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bcplatform', '0007_auto_20190401_2119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='block',
            old_name='proof',
            new_name='nonce',
        ),
    ]
