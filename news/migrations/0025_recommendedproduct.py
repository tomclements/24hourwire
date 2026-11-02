# Generated manually for RecommendedProduct model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0024_story_tweeted_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('search_query', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('world', 'World'), ('us', 'US'), ('politics', 'Politics'), ('business', 'Business'), ('technology', 'Technology'), ('science', 'Science'), ('health', 'Health'), ('sports', 'Sports'), ('entertainment', 'Entertainment')], max_length=20, null=True, blank=True)),
                ('language', models.CharField(default='en', max_length=5)),
                ('description', models.TextField(blank=True)),
                ('image_url', models.URLField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('click_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['category', '-created_at'],
                'indexes': [models.Index(fields=['category', 'language', 'is_active'], name='news_recomm_categor_f14b29_idx')],
            },
        ),
    ]
