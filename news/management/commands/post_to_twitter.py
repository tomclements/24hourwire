import os
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import tweepy
from news.models import Story

logger = logging.getLogger('news.twitter')
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = 'Post top stories to Twitter/X - Optimized for free tier (1,500 tweets/month)'

    def handle(self, *args, **options):
        # FREE TIER LIMIT: 1,500 tweets/month
        # Strategy: Post every 2 hours = 12/day = 360/month (safe buffer)
        
        # Get Twitter credentials from environment
        bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
        api_key = os.environ.get('TWITTER_API_KEY')
        api_secret = os.environ.get('TWITTER_API_SECRET')
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        
        if not all([api_key, api_secret, access_token, access_token_secret]):
            logger.error('Twitter credentials not configured')
            self.stdout.write(self.style.ERROR('Twitter credentials not configured'))
            return
        
        try:
            # Authenticate with Twitter v2 API
            client = tweepy.Client(
                bearer_token=bearer_token,
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )
            
            # Test authentication
            me = client.get_me()
            if not me or not me.data:
                logger.error('Failed to authenticate with Twitter')
                self.stdout.write(self.style.ERROR('Twitter authentication failed'))
                return
                
            logger.info(f'Authenticated as @{me.data.username}')
            self.stdout.write(f'Authenticated as @{me.data.username}')
            
        except Exception as e:
            logger.error(f'Twitter authentication error: {e}')
            self.stdout.write(self.style.ERROR(f'Authentication error: {e}'))
            return
        
        # FREE TIER OPTIMIZATION:
        # - Get stories from last 4 hours (wider window for quality content)
        # - Only post the SINGLE best story per run
        # - Require high quality: covered by 3+ sources, recent
        cutoff = timezone.now() - timedelta(hours=4)
        
        # Get the single best story (prioritize high coverage, then recency)
        story = Story.objects.filter(
            published__gte=cutoff,
            tweeted=False,
            covered_by_count__gte=3  # Higher bar: 3+ sources
        ).order_by('-covered_by_count', '-published').first()
        
        if not story:
            # Fallback: try with 2+ sources if nothing with 3+
            story = Story.objects.filter(
                published__gte=cutoff,
                tweeted=False,
                covered_by_count__gte=2
            ).order_by('-covered_by_count', '-published').first()
        
        if not story:
            logger.info('No quality stories to tweet')
            self.stdout.write(self.style.WARNING('No quality stories to tweet'))
            return
        
        try:
            # Create tweet text (optimized for engagement)
            title = story.title[:180] if len(story.title) > 180 else story.title
            source = story.source
            bias = story.bias_label
            coverage = story.covered_by_count
            
            # Format: Engaging headline + Coverage info + Link
            if coverage >= 3:
                coverage_text = f"Covered by {coverage} sources"
            else:
                coverage_text = f"Via {source}"
            
            tweet_text = f"📰 {title}\n\n{coverage_text}\n\nRead more 👇\n{story.url}\n\n#24HourWire #News #{bias.replace(' ', '').replace('-', '')}"
            
            # Post tweet
            tweet = client.create_tweet(text=tweet_text)
            
            if tweet and tweet.data:
                # Mark as tweeted
                story.tweeted = True
                story.save(update_fields=['tweeted'])
                
                logger.info(f'Posted: {story.title[:50]}...')
                self.stdout.write(self.style.SUCCESS(f'Posted: {story.title[:60]}...'))
                
                # Log monthly count for monitoring
                month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                monthly_count = Story.objects.filter(tweeted=True, tweeted_at__gte=month_start).count()
                logger.info(f'Monthly tweets: {monthly_count}/1500')
                self.stdout.write(f'Monthly usage: {monthly_count}/1500 tweets')
            
        except Exception as e:
            logger.error(f'Error tweeting: {e}')
            self.stdout.write(self.style.ERROR(f'Failed to tweet: {e}'))