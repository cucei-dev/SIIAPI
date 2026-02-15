#!/usr/bin/env python3
"""
Script to seed the database with initial data.
Can be run manually in production or development environments.

Usage:
    python scripts/seed_database.py
    
Or with make:
    make db-seed
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.seed import seed_data


def main():
    """Run database seeding."""
    print("Starting database seeding...")
    try:
        seed_data()
        print("✅ Database seeded successfully!")
        return 0
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())