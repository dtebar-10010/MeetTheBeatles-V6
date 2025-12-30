from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache, caches
from django.conf import settings

## Basic usage with confirmation prompt
#python manage.py clearcache

## Skip confirmation
#python manage.py clearcache --no-confirm

## Clear a specific cache alias
#python manage.py clearcache --alias sessions

## Preview without clearing
#python manage.py clearcache --dry-run

## Clear specific pattern (Redis only)
#python manage.py clearcache --pattern "user:*"

## Show statistics
#python manage.py clearcache --show-stats --no-confirm

## Combine options
#python manage.py clearcache --alias default --dry-run --show-stats

class Command(BaseCommand):
    help = 'Clears the Django cache with options for selective clearing and confirmation'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-confirm',
            action='store_true',
            help='Skip confirmation prompt'
        )
        parser.add_argument(
            '--alias',
            type=str,
            default='default',
            help='Cache alias to clear (default: "default")'
        )
        parser.add_argument(
            '--pattern',
            type=str,
            help='Clear only keys matching this pattern (Redis/Memcached only)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be cleared without actually clearing'
        )
        parser.add_argument(
            '--show-stats',
            action='store_true',
            help='Show cache statistics before and after clearing'
        )

    def handle(self, *args, **options):
        try:
            # Get the cache backend
            cache_alias = options['alias']
            target_cache = caches[cache_alias]
            
            # Check if cache alias exists
            if cache_alias not in settings.CACHES:
                raise CommandError(
                    f'Cache alias "{cache_alias}" not found in settings. '
                    f'Available: {", ".join(settings.CACHES.keys())}'
                )

            # Show cache backend info
            backend = settings.CACHES[cache_alias].get('BACKEND', 'Unknown')
            self.stdout.write(f'Cache backend: {self.style.WARNING(backend)}')
            self.stdout.write(f'Cache alias: {self.style.WARNING(cache_alias)}')
            
            # Handle dry-run mode
            if options['dry_run']:
                self.stdout.write(
                    self.style.WARNING('\n🔍 DRY RUN MODE - No changes will be made\n')
                )

            # Show stats if requested
            if options['show_stats']:
                self._show_cache_stats(target_cache, 'BEFORE')

            # Handle pattern-based clearing
            if options['pattern']:
                self._clear_by_pattern(target_cache, options['pattern'], options['dry_run'])
                return

            # Confirmation prompt (unless skipped)
            if not options['no_confirm'] and not options['dry_run']:
                confirm = input(
                    f'\n⚠️  This will clear ALL data in the "{cache_alias}" cache. '
                    'Are you sure? (yes/no): '
                )
                if confirm.lower() != 'yes':
                    self.stdout.write(self.style.WARNING('Cache clear cancelled.'))
                    return

            # Clear the cache
            if not options['dry_run']:
                target_cache.clear()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✅ Cache "{cache_alias}" cleared successfully!'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✅ Would clear cache "{cache_alias}" (dry-run)'
                    )
                )

            # Show stats after clearing
            if options['show_stats'] and not options['dry_run']:
                self._show_cache_stats(target_cache, 'AFTER')

        except Exception as e:
            raise CommandError(f'Error clearing cache: {str(e)}')

    def _show_cache_stats(self, cache_instance, label):
        """Show cache statistics if the backend supports it"""
        import sys
        
        self.stdout.write(f'\n📊 Cache Stats ({label}):')
        
        try:
            backend_class = cache_instance.__class__.__name__
            stats = {}
            
            # LocMemCache (Local Memory Cache)
            if hasattr(cache_instance, '_cache') and hasattr(cache_instance, '_expire_info'):
                cache_dict = cache_instance._cache
                expire_info = cache_instance._expire_info
                
                stats['Keys'] = len(cache_dict)
                stats['Expired Keys'] = len(expire_info)
                
                # Calculate approximate memory usage
                try:
                    total_size = 0
                    for key, value in cache_dict.items():
                        total_size += sys.getsizeof(key) + sys.getsizeof(value)
                    stats['Approx. Size'] = self._format_bytes(total_size)
                except:
                    pass
                
                # Show max entries if available
                if hasattr(cache_instance, '_max_entries'):
                    max_entries = cache_instance._max_entries
                    stats['Max Entries'] = max_entries
                    if max_entries > 0:
                        usage_pct = (len(cache_dict) / max_entries) * 100
                        stats['Usage'] = f'{usage_pct:.1f}%'
            
            # Redis Cache
            elif hasattr(cache_instance, '_cache') and hasattr(cache_instance._cache, 'info'):
                try:
                    info = cache_instance._cache.info()
                    stats['Keys'] = info.get('db0', {}).get('keys', 0)
                    stats['Memory'] = self._format_bytes(info.get('used_memory', 0))
                    stats['Clients'] = info.get('connected_clients', 0)
                except:
                    stats['Info'] = 'Available (use redis-cli INFO for details)'
            
            # Memcached
            elif hasattr(cache_instance, '_cache') and hasattr(cache_instance._cache, 'get_stats'):
                try:
                    stat_list = cache_instance._cache.get_stats()
                    if stat_list:
                        stats['Info'] = 'Available (use telnet for stats)'
                except:
                    pass
            
            # Display stats
            if stats:
                for key, value in stats.items():
                    self.stdout.write(f'  • {key}: {self.style.SUCCESS(str(value))}')
            else:
                self.stdout.write(f'  • Backend: {backend_class}')
                self.stdout.write('  • No detailed stats available for this backend')
                
        except Exception as e:
            self.stdout.write(f'  • Error retrieving stats: {str(e)}')
    
    def _format_bytes(self, bytes_size):
        """Format bytes to human-readable size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f'{bytes_size:.2f} {unit}'
            bytes_size /= 1024.0
        return f'{bytes_size:.2f} TB'

    def _clear_by_pattern(self, cache_instance, pattern, dry_run):
        """Clear cache keys matching a pattern (backend-dependent)"""
        self.stdout.write(
            self.style.WARNING(
                f'\n🔎 Pattern-based clearing: "{pattern}"'
            )
        )
        
        # Check if backend supports pattern deletion
        if hasattr(cache_instance, 'delete_pattern'):
            if not dry_run:
                cache_instance.delete_pattern(pattern)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Cleared keys matching pattern: {pattern}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Would clear keys matching pattern: {pattern} (dry-run)'
                    )
                )
        else:
            self.stdout.write(
                self.style.ERROR(
                    '❌ Pattern-based clearing not supported by this cache backend.\n'
                    '   This feature requires Redis or a compatible backend.'
                )
            )
