# Generated by Django 2.2 on 2019-12-22 00:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('darpan', '0002_customlink'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='linkaccess',
            name='link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='darpan.ExternalLink'),
        ),
    ]