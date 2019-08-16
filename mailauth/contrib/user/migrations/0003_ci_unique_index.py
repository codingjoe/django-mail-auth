from django.db import migrations

try:
    from django.contrib.postgres.fields import CIEmailField
except ImportError:
    CIEmailField = None
else:
    from django.contrib.postgres.operations import CITextExtension


def _operations():
    if CIEmailField:
        yield CITextExtension()
        yield migrations.AlterField(
            model_name='emailuser',
            name='email',
            field=CIEmailField(
                db_index=True, max_length=254, unique=True, verbose_name='email address'
            ),
        )
    else:
        yield migrations.RunSQL(
            sql=(
                'CREATE UNIQUE INDEX mailauth_user_emailuser_email_upper_idx'
                ' ON mailauth_user_emailuser (UPPER("email"));',
            )
            ,
            reverse_sql=(
                'DROP INDEX mailauth_user_emailuser_email_upper_idx;',
            )
        )


class Migration(migrations.Migration):
    dependencies = [
        ('mailauth_user', '0002_emailuser_session_salt'),
    ]

    operations = list(_operations())
