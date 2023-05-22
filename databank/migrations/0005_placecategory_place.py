# Generated by Django 4.0.4 on 2023-05-22 15:17

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('databank', '0004_remove_rent_end_date_alter_rent_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Categoria de local',
                'verbose_name_plural': 'Categorias de local',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True, verbose_name='Nome')),
                ('description', models.CharField(blank=True, max_length=120, null=True, verbose_name='Descrição')),
                ('lat', models.CharField(blank=True, max_length=120, null=True, verbose_name='Latitude')),
                ('lng', models.CharField(blank=True, max_length=120, null=True, verbose_name='Longitude')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=False, null=True, quality=100, scale=None, size=[500, 300], upload_to='images/places/', verbose_name='Imagem')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='databank.placecategory', verbose_name='Categoria')),
            ],
            options={
                'verbose_name': 'Local',
                'verbose_name_plural': 'Locais',
            },
        ),
    ]
