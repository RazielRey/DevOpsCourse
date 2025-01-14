#!/usr/bin/env python3

import boto3
import json
import sys

# AWS EC2 client
ec2 = boto3.client("ec2")

def generate_inventory():
    # Get all running instances
    filters = [
        {"Name": "instance-state-name", "Values": ["running"]}
    ]
    
    response = ec2.describe_instances(Filters=filters)
    
    # Initialize inventory structure
    inventory = {
        "_meta": {
            "hostvars": {}
        },
        "all": {
            "children": ["aws_ec2", "ec2_jenkins", "ec2_nfs"]
        },
        "aws_ec2": {
            "hosts": []
        },
        "ec2_jenkins": {
            "hosts": []
        },
        "ec2_nfs": {
            "hosts": []
        }
    }

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            # Check if it's a Raziel instance
            is_raziel = False
            for tag in instance.get("Tags", []):
                if tag["Key"] == "Name" and tag["Value"].startswith("raziel_"):
                    is_raziel = True
                    break
            
            if not is_raziel:
                continue

            if "PublicDnsName" not in instance or not instance["PublicDnsName"]:
                continue
            
            hostname = instance["PublicDnsName"]
            
            # Add instance to aws_ec2 group
            inventory["aws_ec2"]["hosts"].append(hostname)

            # Add instance details to hostvars
            inventory["_meta"]["hostvars"][hostname] = {
                "ansible_host": instance.get("PublicIpAddress"),
                "instance_id": instance["InstanceId"],
                "private_ip": instance.get("PrivateIpAddress"),
                "public_ip": instance.get("PublicIpAddress"),
                "tags": {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])}
            }

            # Add to purpose-specific group
            if "Tags" in instance:
                for tag in instance["Tags"]:
                    if tag["Key"] == "Purpose":
                        group_name = f"ec2_{tag['Value'].lower()}"
                        if group_name in inventory:
                            inventory[group_name]["hosts"].append(hostname)

    return inventory

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: dynamic_inventory.py [--list | --host <hostname>]")
        sys.exit(1)

    if sys.argv[1] == "--list":
        print(json.dumps(generate_inventory(), indent=2))
    elif sys.argv[1] == "--host":
        print(json.dumps({}))
    else:
        print("Invalid argument")
        sys.exit(1)
