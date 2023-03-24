# Generated by Django 4.1.1 on 2023-01-30 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Whyus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='slider',
            name='cta',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
