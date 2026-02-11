#!/usr/bin/env python3
"""
Migration script to add Phase V columns to tasks table
"""

import os
from sqlalchemy import create_engine, text

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_KXME4ua0Cnvo@ep-snowy-hill-ai5atl3i-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

print("Connecting to database...")
engine = create_engine(DATABASE_URL)

# SQL statements to add missing columns
migrations = [
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'medium'",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS tags JSON",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS due_date TIMESTAMP",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS reminder_date TIMESTAMP",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurrence_pattern JSON",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS parent_task_id INTEGER",
]

print("\nRunning migrations...")

with engine.connect() as conn:
    for i, migration in enumerate(migrations, 1):
        try:
            print(f"{i}. {migration[:60]}...")
            conn.execute(text(migration))
            conn.commit()
            print("   [OK]")
        except Exception as e:
            print(f"   [SKIP] {e}")

print("\n[SUCCESS] Migration complete!")
print("Tasks table now has Phase V advanced fields.")
