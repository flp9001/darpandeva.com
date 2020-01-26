# Generated by Django 2.2 on 2020-01-26 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('filer', '0011_auto_20190418_0137'),
        ('darpan', '0009_lazypicture'),
    ]

    operations = [
        migrations.AddField(
            model_name='lazypicture',
            name='placeholder_base64_picture',
            field=models.URLField(blank=True, help_text='If provided, overrides the embedded image. Certain options such as cropping are not applicable to external images.', max_length=32768, null=True, verbose_name='Placeholder Base64 image'),
        ),
        migrations.AddField(
            model_name='lazypicture',
            name='placeholder_picture',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.FILER_IMAGE_MODEL, verbose_name='Placeholder Image'),
        ),
        migrations.AddField(
            model_name='lazypicture',
            name='placeholder_thumbnail_options',
            field=models.ForeignKey(blank=True, help_text='Overrides width, height, and crop; scales up to the provided preset dimensions.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='placeholder_thumbnail_options', to='filer.ThumbnailOption', verbose_name='Placeholder Thumbnail options'),
        ),
        migrations.AlterField(
            model_name='lazypicture',
            name='external_picture',
            field=models.URLField(blank=True, help_text='If provided, overrides the embedded image. Certain options such as cropping are not applicable to external images.', max_length=255, null=True, verbose_name='External image'),
        ),
    ]
