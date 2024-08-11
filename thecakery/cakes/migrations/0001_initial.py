# Generated by Django 5.0.6 on 2024-07-28 18:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CakeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Flavour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='flavour_images/')),
            ],
        ),
        migrations.CreateModel(
            name='TrendingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CakeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='cake_images/')),
                ('alt_text', models.CharField(blank=True, max_length=255, null=True)),
                ('cake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='cakes.cake')),
            ],
        ),
        migrations.CreateModel(
            name='CakeSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=50)),
                ('additional_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='cakes.cake')),
            ],
        ),
        migrations.AddField(
            model_name='cake',
            name='cake_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cakes', to='cakes.caketype'),
        ),
        migrations.AddField(
            model_name='cake',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cakes', to='cakes.category'),
        ),
        migrations.AddField(
            model_name='cake',
            name='flavours',
            field=models.ManyToManyField(blank=True, related_name='cakes', to='cakes.flavour'),
        ),
        migrations.CreateModel(
            name='TrendingCake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trend_score', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trending_entries', to='cakes.cake')),
                ('trend_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trending_cakes', to='cakes.trendingtype')),
            ],
            options={
                'ordering': ['-trend_score', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('cakes', models.ManyToManyField(blank=True, related_name='discounts', to='cakes.cake')),
            ],
        ),
    ]
