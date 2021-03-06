# Generated by Django 3.0.3 on 2020-02-25 03:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("elections", "0004_auto_20200220_0524")]

    operations = [
        migrations.AddField(
            model_name="candidate",
            name="election",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="candidates",
                to="elections.Election",
            ),
            preserve_default=False,
        )
    ]
