# Generated migration for adding multilingual fields to Scheme model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheme',
            name='eligibility_hi',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='scheme',
            name='eligibility_ta',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='scheme',
            name='benefits_hi',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='scheme',
            name='benefits_ta',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='scheme',
            name='how_to_apply_hi',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='scheme',
            name='how_to_apply_ta',
            field=models.TextField(blank=True, default=''),
        ),
    ]
