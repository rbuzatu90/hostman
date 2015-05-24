# -*- coding: utf-8 -*-
import sys
import os
print sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'hostman')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'hosts')))
print sys.path
import pytest
from hosts import Hosts, HostsEntry, exception, utils
import hostman


def test_add_single_ipv4_host(tmpdir):
    """
    Test the addition of an ipv4 host succeeds
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost\n")
    new_entry = '3.4.5.6 bob jane.com'
    hostman.add(entry=new_entry, path=hosts_file.strpath)
    hosts = Hosts(path=hosts_file.strpath)
    assert hosts.count(new_entry).get('address_matches') == 1

def test_backup_hosts_file(tmpdir):
    """
    Test the addition of an ipv4 host succeeds
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost\n")
    test_extension = 'test'
    hostman.backup_hosts(source=hosts_file.strpath, extension=test_extension)
    backup_path_split = hosts_file.strpath.split('/')
    new_filename = ".{0}.{1}".format(backup_path_split[-1], test_extension)
    backup_path_split[-1] = new_filename
    backup_path = "/".join(backup_path_split)
    hosts = Hosts(path=backup_path)
    assert hosts.count('127.0.0.1\tlocalhost\n').get('address_matches') == 1

def test_backup_hosts_file_fails_with_invalid_source(tmpdir):
    """
    Test the addition of an ipv4 host succeeds
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost\n")
    with pytest.raises(Exception):
        hostman.backup_hosts(source="invalid")
