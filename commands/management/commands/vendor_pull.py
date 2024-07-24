from pathlib import Path
from typing import Any

from django.core.management import BaseCommand
from django.conf import settings
import helpers

STATICFILES_VENDOR_DIRS = getattr(settings, 'STATICFILES_VENDOR_DIRS')

VENDOR_STATICFILES = {
    "flowbite.min.css": "https://cdn.jsdelivr.net/npm/flowbite@2.4.1/dist/flowbite.min.css",
    "flowbite.min.js": "https://cdn.jsdelivr.net/npm/flowbite@2.4.1/dist/flowbite.min.js",
}


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Downloading Vendor static files...")
        completed_urls = []

        for name, url in VENDOR_STATICFILES.items():
            outpath = Path(STATICFILES_VENDOR_DIRS[0][0]) / 'vendors' / name
            download_success = helpers.download_to_local(url, outpath)
            if download_success:
                completed_urls.append(url)
            else:
                self.stdout.write(self.style.ERROR(f'Failed to download {url}'))

        if set(completed_urls) == set(VENDOR_STATICFILES.values()):
            self.stdout.write(self.style.SUCCESS('Successfully Updated Vendor static files.'))
        else:
            self.stdout.write(self.style.ERROR('Some static files were not downloaded.'))
        # return super().handle(*args, **options)
