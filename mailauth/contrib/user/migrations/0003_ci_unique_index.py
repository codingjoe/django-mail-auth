from django.db import migrations

try:
    from citext import CIEmailField, CITextExtension
except ImportError:
    CITextExtension = None
    CIEmailField = None


def _operations():
    if CITextExtension:
        yield CITextExtension()
        yield migrations.AlterField(
            model_name="emailuser",
            name="email",
            field=CIEmailField(
                db_index=True, max_length=254, unique=True, verbose_name="email address"
            ),
        )
    else:
        yield migrations.RunSQL(
            sql=(
                "CREATE UNIQUE INDEX mailauth_user_emailuser_email_upper_idx"
                ' ON mailauth_user_emailuser (UPPER("email"));',
            ),
            reverse_sql=("DROP INDEX mailauth_user_emailuser_email_upper_idx;",),
        )


class Migration(migrations.Migration):
    dependencies = [
        ("mailauth_user", "0002_emailuser_session_salt"),
    ]

    operations = list(_operations())
