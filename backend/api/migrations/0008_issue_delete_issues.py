# Generated by Django 4.2 on 2024-08-22 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_rename_submited_by_article_submitted_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_title', models.CharField(max_length=255)),
                ('vol_no', models.IntegerField()),
                ('issue_no', models.IntegerField()),
                ('year', models.BigIntegerField()),
                ('month', models.CharField(max_length=20)),
                ('issued_date', models.DateField()),
                ('newIssuePdf', models.FileField(blank=True, null=True, upload_to='issues_pdf/')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='api.article')),
            ],
        ),
        migrations.DeleteModel(
            name='Issues',
        ),
    ]
