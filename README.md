# Silk Software/Data Engineer Assignment


**Requirement**

In this exercise we will implement 3 of the most important steps of data pipeline:

- Data Fetching - Implement API clients to fetch raw hosts from a third party vendor (Qualys / Crowdstrike).
- Data Normalization - Implement logic to normalize the hosts into a unified format.
- Data Deduping - Implement logic to determine and merge duplicate hosts.


**Getting started**

Run below command to execute code
```bash
pip3 install -r requirements.txt

python3 main.py
```

### **How it works**

**Normalization**

I identified 'hostname' and 'name' key are same in Crowdstrike and Qualys's data,it can be used as identifier.
As part of normalisation,I ensure that each host struct has 'name' key in it.

**Deduplication**

If both crowdstrike and qualys return same host,both should be merged into one host structure.
Based on available data,there are only two keys(_id,tags) which are common between Crowdstrike and Qaulys,
so i choose to append it in qualys host with "_crowdstrike" as suffix i.e(_id_crowdstrike,tags_crowdstrike) and 
rest of the uncommon keys are merged to qualys host structure.

Merged and deduped data from both Crowdstrike and Qualys is written in 'merged_hosts.json' file.


**Sample output of merged host**

```
(base) nehajain@MacBook-Pro-2 PythonProject_Silk % cat merged_hosts.json| jq ".[].name"
"ip-172-31-19-223.ec2.internal"
"ip-172-31-93-76.ec2.internal"
"ip-172-31-14-41.ec2.internal"
"ip-172-31-27-66.ec2.internal"
"ip-172-31-94-229.ec2.internal"
"EC2AMAZ-E8FAE79"
"ip-172-31-60-172.ec2.internal"
"yoavs-mbp-2.lan"
```

```
(base) nehajain@MacBook-Pro-2 PythonProject_Silk % cat merged_hosts.json| jq '."ip-172-31-19-223.ec2.internal" | keys'
[
  "_id",
  "_id_crowdstrike",
  "account",
  "address",
  "agentInfo",
  "agent_load_flags",
  "agent_local_time",
  "agent_version",
  "biosDescription",
  "bios_manufacturer",
  "bios_version",
  "chassis_type",
  "chassis_type_desc",
  "cid",
  "cloudProvider",
  "config_id_base",
  "config_id_build",
  "config_id_platform",
  "connection_ip",
  "connection_mac_address",
  "cpu_signature",
  "created",
  "default_gateway_ip",
  "device_id",
  "device_policies",
  "dnsHostName",
  "external_ip",
  "first_seen",
  "fqdn",
  "group_hash",
  "groups",
  "hostname",
  "id",
  "instance_id",
  "isDockerHost",
  "kernel_version",
  "lastComplianceScan",
  "lastLoggedOnUser",
  "lastSystemBoot",
  "lastVulnScan",
  "last_seen",
  "local_ip",
  "mac_address",
  "major_version",
  "manufacturer",
  "meta",
  "minor_version",
  "model",
  "modified",
  "modified_timestamp",
  "name",
  "networkGuid",
  "networkInterface",
  "openPort",
  "os",
  "os_version",
  "platform_id",
  "platform_name",
  "policies",
  "processor",
  "product_type_desc",
  "provision_status",
  "qwebHostId",
  "reduced_functionality_mode",
  "serial_number",
  "service_provider",
  "service_provider_account_id",
  "software",
  "sourceInfo",
  "status",
  "system_manufacturer",
  "system_product_name",
  "tags",
  "tags_crowdstrike",
  "timezone",
  "totalMemory",
  "trackingMethod",
  "type",
  "volume",
  "vuln",
  "zone_group"
]
```