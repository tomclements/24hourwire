# Deduplicate PollVote (poll, vote_hash) keeping the oldest row, then
# replace the non-unique composite index with a UniqueConstraint.

from django.db import migrations, models
from django.db.models import Count, Min


def dedupe_pollvotes(apps, schema_editor):
    """Keep the oldest PollVote per (poll, vote_hash); delete extras."""
    PollVote = apps.get_model('news', 'PollVote')
    groups = (
        PollVote.objects.values('poll_id', 'vote_hash')
        .annotate(n=Count('id'), keep_id=Min('id'))
        .filter(n__gt=1)
    )
    for group in groups:
        PollVote.objects.filter(
            poll_id=group['poll_id'],
            vote_hash=group['vote_hash'],
        ).exclude(id=group['keep_id']).delete()


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0020_story_categories'),
    ]

    operations = [
        migrations.RunPython(dedupe_pollvotes, noop_reverse),
        migrations.RemoveIndex(
            model_name='pollvote',
            name='news_pollvo_poll_id_99743a_idx',
        ),
        migrations.AddConstraint(
            model_name='pollvote',
            constraint=models.UniqueConstraint(
                fields=('poll', 'vote_hash'),
                name='news_pollvote_poll_vote_hash_uniq',
            ),
        ),
    ]
