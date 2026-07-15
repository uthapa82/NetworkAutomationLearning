#!/usr/bin/env python3
"""
Upload configurations to EVE-NG nodes
This script uploads the generated configs to running nodes
"""

from evengsdk.client import EvengClient
import yaml
import os
import getpass
import time

def upload_node_config(eve, lab_path, node_id, config_content):
    """Upload configuration to a specific node"""
    try:
        # Using EVE-NG API to set node configuration
        resp = eve.api.upload_node_config(
            lab_path, 
            node_id, 
            config_content
        )
        return resp.get('status') == 'success'
    except Exception as e:
        print(f"    Error: {e}")
        return False

# Get credentials
username = input("Username: ")
password = getpass.getpass("Password: ")

# Connect to EVE-NG
host = input("EVE-NG Host (IP or URL): ")
eve = EvengClient(host, ssl_verify=False, protocol="http", port=80)
eve.disable_insecure_warnings()
eve.login(username=username, password=password)

print("\u2714 Connected to EVE-NG successfully\n")

# Load lab topology
with open("lab_topology.yml") as f:
    lab_data = yaml.safe_load(f)

lab_name = lab_data["lab"]["name"]
lab_path = lab_data["lab"].get("path", "/")
full_lab_path = f"{lab_path}{lab_name}.unl"

print(f"Lab: {lab_name}")
print(f"Path: {full_lab_path}\n")

# Get all nodes in the lab
print("Fetching nodes from lab...")
nodes_resp = eve.api.list_nodes(full_lab_path)

if not nodes_resp or 'data' not in nodes_resp:
    print("\u2716 Could not retrieve nodes from lab")
    eve.logout()
    exit(1)

nodes_in_lab = nodes_resp['data']
print(f"✓ Found {len(nodes_in_lab)} nodes\n")

print("="*70)
print("Uploading Configurations")
print("="*70)

# Upload configs for each node
success_count = 0
for node_id, node_info in nodes_in_lab.items():
    node_name = node_info.get('name')
    config_file = f"configs/{node_name}.cfg"
    
    if os.path.exists(config_file):
        print(f"\n[{node_name}]")
        print(f"Reading config from: {config_file}")
        
        with open(config_file, 'r') as f:
            config_content = f.read()
        
        print(f"Uploading configuration...")
        if upload_node_config(eve, full_lab_path, node_id, config_content):
            print(f"\u2714 Configuration uploaded successfully")
            success_count += 1
        else:
            print(f"\u2716 Failed to upload configuration")
    else:
        print(f"\n[{node_name}] !!  No config file found")

print("\n" + "="*70)
print(f"Upload Summary: {success_count}/{len(nodes_in_lab)} successful")
print("="*70)


# Logout
# eve.logout()
# print("\n Done!")