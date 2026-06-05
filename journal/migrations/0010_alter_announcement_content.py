from django.db import migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0009_user_orcid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
