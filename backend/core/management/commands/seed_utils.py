import json
from datetime import date, datetime, time
from pathlib import Path

from django.conf import settings
from django.core.management.base import CommandError
from django.db import connection
from django.utils import timezone


SEED_DIR = Path(settings.BASE_DIR) / "seeders"


def load_seed_data(filename: str):
    path = SEED_DIR / filename
    if not path.exists():
        raise CommandError(f"Seed file not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_date(value):
    if not value:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    return date.fromisoformat(value)


def parse_time(value):
    if not value:
        return None
    if isinstance(value, time):
        return value
    return time.fromisoformat(value)


def parse_datetime(value):
    if not value:
        return None
    if isinstance(value, datetime):
        parsed = value
    else:
        parsed = datetime.fromisoformat(value)
    if timezone.is_naive(parsed):
        return timezone.make_aware(parsed, timezone.get_default_timezone())
    return parsed


def update_timestamp(model, pk, field, value):
    if value is None:
        return
    model.objects.filter(pk=pk).update(**{field: value})


def reset_pk_sequence(model):
    """
    Re-sync autoincrement sequence after inserting fixed IDs in PostgreSQL.
    This prevents duplicate key errors on the next regular INSERT.
    """
    if connection.vendor != "postgresql":
        return

    table_name = model._meta.db_table
    pk_column = model._meta.pk.column

    sql = f"""
    SELECT setval(
        pg_get_serial_sequence('"{table_name}"', '{pk_column}'),
        COALESCE(MAX("{pk_column}"), 1),
        MAX("{pk_column}") IS NOT NULL
    )
    FROM "{table_name}";
    """

    with connection.cursor() as cursor:
        cursor.execute(sql)
