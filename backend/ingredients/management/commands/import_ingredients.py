import json

from django.conf import settings
from django.core.management.base import BaseCommand

from ingredients.models import Ingredient


class Command(BaseCommand):
    def fetch_data(self, filename):
        django_root = settings.BASE_DIR
        with open(f"{django_root}/data/{filename}", "r", encoding="utf-8-sig") as f:
            res = f.read().replace("\n", "")
        return json.loads(res)

    def handle(self, *args, **options):
        incoming_data = self.fetch_data("ingredients.json")
        bulk = [Ingredient(**x) for x in incoming_data]
        Ingredient.objects.bulk_create(bulk)
