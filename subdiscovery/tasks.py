from __future__ import absolute_import, unicode_literals
from celery import shared_task

import subprocess
from utils import send_slack_notification
from subdiscovery.models import Domain, Subdomain

@shared_task
def find_subdomains():
    domains = Domain.objects.all()

    for domain in domains:
        args = ['assetfinder', '--subs-only', domain.name]
        subdomains_found = (subprocess.run(args, check=True, stdout=subprocess.PIPE) \
                .stdout.decode().split('\n'))

        # Remove empty strings
        subdomains_found = filter(None, subdomains_found)

        subdomains_existing = Subdomain.objects.filter(domain=domain).values('name')

        is_first_run = True if len(subdomains_existing) == 0 else False
        not_in_db = set(subdomains_found) - set(sub['name'] for sub in subdomains_existing)

        for e in not_in_db:
            s = Subdomain(domain=domain, name=e)
            s.save()
            if not is_first_run:
                send_slack_notification(f'Found Subdomain: {e}')

