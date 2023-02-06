from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mailauth_user", "0003_ci_unique_index"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emailuser",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
    ]
