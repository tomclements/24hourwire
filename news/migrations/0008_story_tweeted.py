# Generated manual migration for adding tweeted field
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('news', '0007_alter_story_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='tweeted',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]