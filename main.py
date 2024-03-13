import json
import logging

from silk_client import CrowdStrikeClient
from silk_client import QualysClient

BATCH_SIZE = 1
TOTAL_HOSTS = 6

def fetch_hosts(client, identifier):
    hosts = {}
    for skip_count in range(0, TOTAL_HOSTS, BATCH_SIZE):
        try:
            for host in client.get_hosts(skip_count):
                if identifier in host:
                    hosts[host[identifier]] = host
        except Exception as e:
            logging.error("host fetch error: %s", e)
            break
    return hosts

def fetch():
    print("Fetching CrowdStrike data...")
    crowdstrike_hosts = fetch_hosts(CrowdStrikeClient(), identifier="hostname")

    print("Fetching Qualys data...")
    qualys_hosts = fetch_hosts(QualysClient(), identifier="name")

    return crowdstrike_hosts, qualys_hosts


def merge_host(crowdstrike_host, qualys_host):
    '''
    Merge crowdstrike and qualys host
    '''
    for key,value in  crowdstrike_host.items():
        if key in qualys_host:
            if qualys_host[key] != value:
                qualys_host[key+"_crowdstrike"] = value
        else:
            qualys_host[key] = value
    return qualys_host

def deduplicate_data(crowdstrike_hosts, qualys_hosts):
    logging.info("merging hosts")
    logging.info("crowdstrike hosts size: %d", len((crowdstrike_hosts)))
    logging.info("crowdstrike hosts size: %d", len((qualys_hosts)))
    for hostname, host in crowdstrike_hosts.items():
        if hostname in qualys_hosts:
            qualys_hosts[hostname] = merge_host(host, qualys_hosts[hostname])
        else:
            qualys_hosts[hostname] = host
    return qualys_hosts

def pipeline():
    crowdstrike_hosts, qualys_hosts = fetch()
    merged_hosts = deduplicate_data(crowdstrike_hosts, qualys_hosts)
    json.dump(merged_hosts, open('merged_hosts.json', 'w'))

def main():
    pipeline()

if __name__ == "__main__":
    main()


