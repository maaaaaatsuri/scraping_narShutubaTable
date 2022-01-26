# Generated by Django 3.2.9 on 2022-01-05 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('開催日', models.CharField(max_length=12)),
                ('開催場所', models.CharField(max_length=10)),
                ('レース', models.CharField(max_length=4)),
                ('着順', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('枠', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('馬番', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('逆番', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('印', models.CharField(max_length=6)),
                ('馬名', models.CharField(max_length=10)),
                ('騎手', models.CharField(max_length=10)),
                ('厩舎', models.CharField(max_length=10)),
                ('単勝オッズ', models.FloatField(blank=True, null=True)),
                ('人気', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
        ),
    ]
