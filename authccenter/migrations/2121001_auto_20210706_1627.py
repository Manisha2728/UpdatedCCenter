# Generated by Django 3.2.4 on 2021-07-06 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authccenter', '2121000_Peacock_CU1_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adgroup',
            name='ccneter_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authccenter.ccentergroup'),
        ),
        migrations.AlterField(
            model_name='ccenteruser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='ccenter_user_set', related_query_name='ccenter_user', to='authccenter.ADGroup', verbose_name='groups'),
        ),
    ]
