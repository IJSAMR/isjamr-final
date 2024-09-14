# Generated by Django 4.2 on 2024-08-15 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article_copyright',
            field=models.FileField(blank=True, null=True, upload_to='copyright_form/'),
        ),
        migrations.AddField(
            model_name='article',
            name='article_doc',
            field=models.FileField(blank=True, null=True, upload_to='article_doc/'),
        ),
    ]
