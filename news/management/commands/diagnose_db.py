"""
Management command to diagnose database connectivity issues.
Run: python manage.py diagnose_db
"""

import os
import time
from django.core.management.base import BaseCommand
from django.db import connection, OperationalError
from django.conf import settings


class Command(BaseCommand):
    help = 'Diagnose database connectivity issues'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("DATABASE DIAGNOSTIC")
        self.stdout.write("=" * 60)
        self.stdout.write("")
        
        # Check environment variables
        self.stdout.write("1. Environment Variables:")
        db_url = os.environ.get('DATABASE_URL', 'NOT SET')
        # Mask password for security
        if '://' in db_url and '@' in db_url:
            masked = db_url.split('@')[0].split('://')[0] + '://' + '****:****@' + db_url.split('@')[1]
            self.stdout.write(f"   DATABASE_URL: {masked}")
        else:
            self.stdout.write(f"   DATABASE_URL: {'SET' if db_url != 'NOT SET' else 'NOT SET'}")
        
        self.stdout.write("")
        
        # Check Django settings
        self.stdout.write("2. Django Database Settings:")
        db_config = settings.DATABASES.get('default', {})
        self.stdout.write(f"   ENGINE: {db_config.get('ENGINE')}")
        self.stdout.write(f"   HOST: {db_config.get('HOST')}")
        self.stdout.write(f"   PORT: {db_config.get('PORT')}")
        self.stdout.write(f"   NAME: {db_config.get('NAME')}")
        self.stdout.write(f"   USER: {db_config.get('USER')}")
        self.stdout.write(f"   CONN_MAX_AGE: {db_config.get('CONN_MAX_AGE', 'Not set')}")
        self.stdout.write(f"   OPTIONS: {db_config.get('OPTIONS', {})}")
        
        self.stdout.write("")
        
        # Test connection with retries
        self.stdout.write("3. Testing Database Connection:")
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.stdout.write(f"   Attempt {attempt + 1}/{max_retries}...", ending=" ")
                connection.ensure_connection()
                with connection.cursor() as cursor:
                    # Use database-agnostic test
                    cursor.execute("SELECT 1")
                    cursor.fetchone()
                    self.stdout.write(self.style.SUCCESS("SUCCESS"))
                    
                    # Try to get story count
                    try:
                        from news.models import Story
                        count = Story.objects.count()
                        self.stdout.write(f"   Total stories in database: {count}")
                    except Exception as e:
                        self.stdout.write(f"   Could not count stories: {e}")
                    break
            except OperationalError as e:
                self.stdout.write(self.style.ERROR(f"FAILED: {e}"))
                if attempt < max_retries - 1:
                    wait_time = 2 * (attempt + 1)
                    self.stdout.write(f"   Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    try:
                        connection.close()
                    except:
                        pass
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"ERROR: {type(e).__name__}: {e}"))
                break
        else:
            self.stdout.write("")
            self.stdout.write(self.style.ERROR("All connection attempts failed"))
            self.stdout.write("")
            self.stdout.write("Possible causes:")
            self.stdout.write("   - Database is not running or reachable")
            self.stdout.write("   - DATABASE_URL is incorrect")
            self.stdout.write("   - Network/firewall blocking connection")
            self.stdout.write("   - SSL/TLS configuration mismatch")
            self.stdout.write("")
            self.stdout.write("Recommended actions:")
            self.stdout.write("   1. Check Render dashboard for database status")
            self.stdout.write("   2. Verify DATABASE_URL environment variable")
            self.stdout.write("   3. Check database logs in Render dashboard")
            self.stdout.write("   4. Ensure web service and database are in same region")
            return
        
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Database connection is working!"))
