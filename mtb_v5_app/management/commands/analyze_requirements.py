"""
Analyze requirements.txt to identify necessary vs unnecessary packages
"""

# Core Django packages
DJANGO_CORE = {
    'Django',
    'asgiref',
    'sqlparse',
    'tzdata',
}

# Django extensions/plugins used in project
DJANGO_EXTENSIONS = {
    'django-ckeditor-5',  # CKEditor integration in admin
    'django-crispy-forms',  # Form styling
    'django-debug-toolbar',  # Development debugging
}

# Database drivers
DATABASE = {
    'psycopg2-binary',  # PostgreSQL (may not be needed if only using SQLite)
}

# Image processing
IMAGE = {
    'pillow',  # Required for ImageField in Media model
}

# CLI/Terminal enhancements
CLI_TOOLS = {
    'about-time',
    'alive-progress',
    'grapheme',
}

# Data processing
DATA_PROCESSING = {
    'narwhals',  # Data manipulation (check if actually used)
}

# HTTP/Network
HTTP = {
    'requests',  # HTTP library
    'urllib3',
    'certifi',
    'charset-normalizer',
    'idna',
}

# Configuration/Environment
CONFIG = {
    'python-dotenv',  # .env file support
    'PyYAML',  # YAML parsing
}

# Date/Time
DATETIME = {
    'python-dateutil',
    'pytz',
}

# Type hints
TYPE_HINTS = {
    'typing_extensions',
}

# Utilities
UTILITIES = {
    'packaging',
    'six',
}

# Template linting
LINTING = {
    'djlint',
}

print("=" * 70)
print("REQUIREMENTS.TXT ANALYSIS")
print("=" * 70)

print("\n✓ NECESSARY PACKAGES:")
print("\nDjango Core:")
for pkg in sorted(DJANGO_CORE):
    print(f"  - {pkg}")

print("\nDjango Extensions (Used in project):")
for pkg in sorted(DJANGO_EXTENSIONS):
    print(f"  - {pkg}")

print("\nImage Processing (Required for Media model):")
for pkg in sorted(IMAGE):
    print(f"  - {pkg}")

print("\nCLI Tools (Used in management commands with progress bars):")
for pkg in sorted(CLI_TOOLS):
    print(f"  - {pkg}")

print("\nConfiguration:")
for pkg in sorted(CONFIG):
    print(f"  - {pkg}")

print("\nDate/Time:")
for pkg in sorted(DATETIME):
    print(f"  - {pkg}")

print("\nTemplate Linting:")
for pkg in sorted(LINTING):
    print(f"  - {pkg}")

print("\n⚠ PACKAGES TO REVIEW:")

print("\nDatabase Drivers:")
print("  - psycopg2-binary: Only needed if using PostgreSQL.")
print("    Currently using SQLite. Can be REMOVED unless planning to use PostgreSQL.")

print("\nHTTP Libraries:")
print("  - requests, urllib3, certifi, charset-normalizer, idna:")
print("    Check if any management commands or views use these.")
print("    If not making external HTTP requests, these can be REMOVED.")

print("\nData Processing:")
print("  - narwhals: Check if actually used in the project.")
print("    If not found in any code, can be REMOVED.")

print("\nUtilities:")
print("  - packaging: Usually a dependency of other packages, auto-installed.")
print("  - six: Python 2/3 compatibility (outdated for Python 3.13).")
print("    Can likely be REMOVED if no package explicitly needs it.")

print("\nType Hints:")
print("  - typing_extensions: Usually needed by other packages.")
print("    Keep unless causing issues.")

print("\n" + "=" * 70)
print("RECOMMENDATION SUMMARY")
print("=" * 70)
print("""
SAFE TO REMOVE (if not used):
  1. psycopg2-binary (unless using PostgreSQL)
  2. requests + urllib3 + certifi + charset-normalizer + idna (if no HTTP calls)
  3. narwhals (if not used in code)
  4. six (outdated for modern Python)

TO VERIFY:
  - Check management commands for HTTP requests usage
  - Search codebase for 'narwhals' imports
  - Check if any dependencies require 'six'
""")
