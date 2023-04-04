# Generated by Django 4.1.7 on 2023-04-11 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grocery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('grain', '곡물'), ('nut', '견과류'), ('fruit', '과일'), ('vegetable', '채소'), ('meat', '육류'), ('dairy', '유제품'), ('marine', '수산물'), ('seasoning', '조미료'), ('spice', '향신료'), ('processed', '가공식품')], default='grain', max_length=50)),
                ('qty', models.IntegerField()),
                ('in_date', models.DateField()),
                ('exp_date', models.DateField()),
            ],
        ),
    ]