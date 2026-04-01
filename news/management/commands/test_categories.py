"""
Test command for categorization system.

Usage:
    python manage.py test_categories
    python manage.py test_categories --verbose
"""
import sys
from django.core.management.base import BaseCommand
from news.tests_category import TEST_CASES
from news.views import get_story_categories


class Command(BaseCommand):
    help = 'Test story categorization accuracy'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output for each test case',
        )

    def handle(self, *args, **options):
        verbose = options['verbose']
        
        self.stdout.write(self.style.HTTP_INFO("Testing categorization system...\n"))
        
        passed = 0
        failed = 0
        
        for title, expected_categories, notes in TEST_CASES:
            predicted = get_story_categories(title)
            
            # Check if all expected categories are in predicted
            missing = set(expected_categories) - set(predicted)
            extra = set(predicted) - set(expected_categories)
            
            is_correct = len(missing) == 0
            
            if is_correct:
                passed += 1
                status = self.style.SUCCESS("✓ PASS")
            else:
                failed += 1
                status = self.style.ERROR("✗ FAIL")
            
            if verbose or not is_correct:
                self.stdout.write(f"\n{status} {title}")
                self.stdout.write(f"   Expected: {expected_categories}")
                self.stdout.write(f"   Predicted: {predicted}")
                if missing:
                    self.stdout.write(self.style.WARNING(f"   Missing: {list(missing)}"))
                if extra:
                    self.stdout.write(self.style.WARNING(f"   Extra: {list(extra)}"))
                if notes:
                    self.stdout.write(f"   Notes: {notes}")
        
        # Summary
        total = passed + failed
        accuracy = (passed / total * 100) if total > 0 else 0
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.HTTP_INFO(f"\nTest Results:"))
        self.stdout.write(f"  Total: {total}")
        self.stdout.write(self.style.SUCCESS(f"  Passed: {passed}"))
        self.stdout.write(self.style.ERROR(f"  Failed: {failed}"))
        self.stdout.write(f"  Accuracy: {accuracy:.1f}%")
        
        if failed > 0:
            self.stdout.write(self.style.WARNING("\n⚠ Some tests failed. Review failures above."))
            sys.exit(1)
        else:
            self.stdout.write(self.style.SUCCESS("\n✓ All tests passed! Ready to deploy."))
