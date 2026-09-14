# Generated manually for topic matching redesign

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0022_alter_story_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='match_rules',
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text=(
                    "Tiered matching: {anchors, medium, weak, negatives, "
                    "deny_categories, min_score}. Empty => legacy keywords as medium-only."
                ),
            ),
        ),
    ]
