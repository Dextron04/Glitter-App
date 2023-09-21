# myapp/management/commands/import_data.py
import json
from django.core.management.base import BaseCommand
from Glitter.models import TableModel

class Command(BaseCommand):
    help = 'Import data from JSON file'

    def handle(self, *args, **kwargs):
        # Update the file path to point to your JSON file
        file_path = 'valid_list.json'

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for item in data:
                TableModel.objects.create(
                    number=item['number'],
                    description=item['description'],
                    price=item['price'],
                    max_price=item['max price'],
                    strike_price=item['strike price'],
                    volume=item['volume'],
                    expiration_date=item['expiration date']
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
