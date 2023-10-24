from django.db import migrations, models

try:
    from citext import CIEmailField
except ImportError:
    CIEmailField = models.EmailField


class Migration(migrations.Migration):
    dependencies = [
        ("mailauth_user", "0004_auto_20200812_0722"),
    ]

    operations = [
        # add new permissions
        migrations.AlterModelOptions(
            name="emailuser",
            options={
                "permissions": [("anonymize", "Can anonymize user")],
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
        ),
        # email is now nullable
        migrations.AlterField(
            model_name="emailuser",
            name="email",
            field=CIEmailField(
                blank=True,
                db_index=True,
                max_length=254,
                null=True,
                unique=True,
                verbose_name="email address",
            ),
        ),
    ]
