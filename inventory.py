#!/usr/bin/env python
target = "192.168.56.0/24"

"""Local network discovery inventory script
Generates an Ansible inventory of all hosts on a local network that
have port 22 open, ensure file has chmod +x).
"""

import argparse
import json
import nmap
import socket
import time

class LocalNetworkInventory(object):
  def __init__(self):
    """Main execution path"""
    self.parse_cli_args()

    data_to_print = ""

    if self.args.host:
      data_to_print = self.get_host_info()
    else:
      # Default action is to list instances, so we don't bother
      # checking `self.args.list`.
      data_to_print = self.json_format_dict(self.get_inventory())

    print data_to_print


  def parse_cli_args(self):
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
      description="Produce an Ansible Inventory file comprised of hosts on the local network"
    )
    parser.add_argument(
      "--list",
      action="store_true",
      default=True,
      help="List instances (default: True)"
    )
    parser.add_argument(
      "--host",
      action="store",
      help="Get all the variables about a specific instance"
    )
    self.args = parser.parse_args()


  def get_inventory(self):
    """Populate `self.inventory` with hosts on the local network that
    are accessible via SSH.
    """
    return { "all": { "hosts": self.lookup_local_ips() }}


  def json_format_dict(self, data):
    return json.dumps(data, sort_keys=True, indent=2)
  

  def lookup_local_ips(self):
    """Lookup IPs of hosts connected to the local network"""
    nm = nmap.PortScanner()
    nm.scan(hosts=target, arguments="-p 22 --open")
    return nm.all_hosts()


  def get_host_info(self):
    """Get variables about a specific host"""
    return self.json_format_dict({})


LocalNetworkInventory()
