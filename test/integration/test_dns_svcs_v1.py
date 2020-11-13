# -*- coding: utf-8 -*-
# (C) Copyright IBM Corp. 2020.

"""
Integration test code to execute dns zones
"""

from ibm_cloud_networking_services.dns_svcs_v1 import DnsSvcsV1
import os
import unittest

from dotenv import load_dotenv, find_dotenv
configFile = "dns.env"
# load the .env file containing your environment variables
try:
    load_dotenv(find_dotenv(filename=configFile))
except:
    raise unittest.SkipTest('no dns.env file loaded, skipping...')


class TestDNSSvcsV1(unittest.TestCase):
    """The DNS V1 service test class."""

    def setUp(self):
        """ test case setup """
        if not os.path.exists(configFile):
            raise unittest.SkipTest(
                'External configuration not available, skipping...')
        self.instance_id = os.getenv("DNS_SVCS_INSTANCE_ID")
        # create zone class object
        self.zone = DnsSvcsV1.new_instance(service_name="dns_svcs")
        # Delete the resources
        self._clean_dns_zones()

    def tearDown(self):
        """ tear down """
        # Delete the resources
        self._clean_dns_zones()
        print("Clean up complete")

    def _clean_dns_zones(self):
        response = self.zone.list_dnszones(instance_id=self.instance_id)
        assert response is not None
        assert response.status_code == 200
        result = response.get_result()
        if result is not None:
            zones = result.get("dnszones")
            for zone in zones:
                print(zone.get("id"))
                self.zone.delete_dnszone(
                    instance_id=self.instance_id, dnszone_id=zone.get("id"))

    def test_1_pdns_zone_action(self):
        """ test private dns zone create/delete/update/get functionality """
        name = "test.example36.com"
        label = "us-south"
        resp = self.zone.list_dnszones(instance_id=self.instance_id)
        assert resp is not None
        assert resp.status_code == 200

        # create dns zone
        resp = self.zone.create_dnszone(
            instance_id=self.instance_id, name=name, label=label)
        assert resp is not None
        assert resp.status_code == 200
        assert resp.get_result().get("instance_id") == self.instance_id
        assert resp.get_result().get("name") == name
        assert resp.get_result().get("label") == label
        zone_id = resp.get_result().get("id")

        # get dns zone
        resp = self.zone.get_dnszone(
            instance_id=self.instance_id, dnszone_id=zone_id)
        assert resp.status_code == 200
        assert resp.get_result().get("instance_id") == self.instance_id
        assert resp.get_result().get("name") == name
        assert resp.get_result().get("label") == label

        # update dns zone
        label = "us-south-1"
        desc = "test instance"
        resp = self.zone.update_dnszone(
            instance_id=self.instance_id, dnszone_id=zone_id, description=desc, label=label)
        assert resp is not None
        assert resp.status_code == 200
        assert resp.get_result().get("instance_id") == self.instance_id
        assert resp.get_result().get("name") == name
        assert resp.get_result().get("label") == label
        assert resp.get_result().get("description") == desc

        # delete dns zone
        resp = self.zone.delete_dnszone(
            instance_id=self.instance_id, dnszone_id=zone_id)
        assert resp is not None
        assert resp.status_code == 204

    def test_1_pdns_zone_list(self):
        """ test private dns zone list functionality """

        name = "test.example34.com"
        label = "us-south"
        # create dns zone
        resp = self.zone.create_dnszone(
            instance_id=self.instance_id, name=name, label=label)
        assert resp is not None
        assert resp.status_code == 200

        name = "test.example35.com"
        # create dns zone
        resp = self.zone.create_dnszone(
            instance_id=self.instance_id, name=name, label=label)
        assert resp is not None
        assert resp.status_code == 200

        name = "test.example36.com"
        # create dns zone
        resp = self.zone.create_dnszone(
            instance_id=self.instance_id, name=name, label=label)
        assert resp is not None
        assert resp.status_code == 200

        name = "test.example37.com"
        # create dns zone
        resp = self.zone.create_dnszone(
            instance_id=self.instance_id, name=name, label=label)
        assert resp is not None
        assert resp.status_code == 200

        resp = self.zone.list_dnszones(
            instance_id=self.instance_id, offset=1, limit=2)
        assert resp is not None
        assert resp.status_code == 200

    def test_1_pdns_zone_negative(self):
        name = "test.example36.com"
        label = "us-south"
        instance_id = None
        with self.assertRaises(ValueError) as val:
            self.zone.create_dnszone(instance_id=instance_id,
                                     name=name, label=label)
            self.assertEqual(val.exception.msg, 'instance_id must be provided')
        desc = "this is a test"
        dnszone_id = "123456"
        with self.assertRaises(ValueError) as val:
            self.zone.update_dnszone(instance_id=instance_id,
                                     dnszone_id=dnszone_id, description=desc, label=label)
            self.assertEqual(val.exception.msg, 'instance_id must be provided')
        instance_id = "123456"
        dnszone_id = None
        with self.assertRaises(ValueError) as val:
            self.zone.update_dnszone(instance_id=instance_id,
                                     dnszone_id=dnszone_id, description=desc, label=label)
            self.assertEqual(val.exception.msg, 'dnszone_id must be provided')

        instance_id = None
        dnszone_id = "123456"
        with self.assertRaises(ValueError) as val:
            self.zone.delete_dnszone(instance_id=instance_id,
                                     dnszone_id=dnszone_id)
            self.assertEqual(val.exception.msg, 'instance_id must be provided')
        instance_id = "123545"
        dnszone_id = None
        with self.assertRaises(ValueError) as val:
            self.zone.delete_dnszone(instance_id=instance_id,
                                     dnszone_id=dnszone_id)
            self.assertEqual(val.exception.msg, 'dnszone_id must be provided')

        instance_id = None
        dnszone_id = "123456"
        with self.assertRaises(ValueError) as val:
            self.zone.get_dnszone(instance_id=instance_id,
                                  dnszone_id=dnszone_id)
            self.assertEqual(val.exception.msg, 'instance_id must be provided')
        instance_id = "123545"
        dnszone_id = None
        with self.assertRaises(ValueError) as val:
            self.zone.get_dnszone(instance_id=instance_id,
                                  dnszone_id=dnszone_id)
            self.assertEqual(val.exception.msg, 'dnszone_id must be provided')

        instance_id = None
        with self.assertRaises(ValueError) as val:
            self.zone.list_dnszones(instance_id=instance_id)
            self.assertEqual(val.exception.msg, 'instance_id must be provided')


class TestResourceRecordsV1(unittest.TestCase):
    """The Resourse records V1 service test class."""

    def setUp(self):
        """ test case setup """
        if not os.path.exists(configFile):
            raise unittest.SkipTest(
                'External configuration not available, skipping...')
        self.instance_id = os.getenv("DNS_SVCS_INSTANCE_ID")
        self.zone_id = ""
        # create zone class object
        self.zone = DnsSvcsV1.new_instance(service_name="dns_svcs")
        # create resource record service class object
        self.record = DnsSvcsV1.new_instance(
            service_name="dns_svcs")
        self._create_dns_zones()

    def tearDown(self):
        """ tear down """
        # Delete the resources
        self._clean_dns_resource_records()
        print("Clean up complete")

    def _create_dns_zones(self):
        name = "test.example36.com"
        label = "us-south"
        resp = self.zone.create_dnszone(
            instance_id=self.instance_id, name=name, label=label)
        assert resp is not None
        assert resp.status_code == 200
        self.zone_id = resp.get_result().get("id")

    def _clean_dns_resource_records(self):
        # list all dns resource records
        response = self.record.list_resource_records(
            instance_id=self.instance_id, dnszone_id=self.zone_id)
        assert response is not None
        assert response.status_code == 200
        result = response.get_result().get("resource_records")
        for record in result:
            # delete resource record
            self.record.delete_resource_record(
                instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record.get("id"))

        # delete dns zones
        response = self.zone.list_dnszones(instance_id=self.instance_id)
        assert response is not None
        assert response.status_code == 200
        result = response.get_result().get("dnszones")
        for zone in result:
            self.zone.delete_dnszone(
                instance_id=self.instance_id, dnszone_id=zone.get("id"))

    def test_1_resource_records_actions(self):
        """ DNS record actions """
        record_type = 'A'
        name = 'test.example.com'
        content = '2.2.2.2'
        ttl = 60
        rdata = {
            'ip': content
        }
        # create resource record
        resp = self.record.create_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, type=record_type, ttl=ttl, name=name, rdata=rdata)
        assert resp is not None
        assert resp.status_code == 200
        record_id = resp.get_result().get("id")

        # update resource record
        name = 'test.example43.com'
        content = '2.2.2.3'
        ttl = 60
        rdata = {
            'ip': content
        }
        resp = self.record.update_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id,
            type=record_type, ttl=ttl, name=name, rdata=rdata)
        assert resp is not None
        assert resp.status_code == 200

        # get resource record
        resp = self.record.get_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id)
        assert resp is not None
        assert resp.status_code == 200

        # delete resource record
        resp = self.record.delete_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id)
        assert resp is not None
        assert resp.status_code == 204

    def test_2_resource_records_actions(self):
        """ DNS record AAAA actions """
        record_type = 'AAAA'
        name = 'test.example.com'
        ttl = 60
        rdata = {
            'ip': '2001::1'
        }
        # create resource record
        resp = self.record.create_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, type=record_type, ttl=ttl, name=name, rdata=rdata)
        assert resp is not None
        assert resp.status_code == 200
        record_id = resp.get_result().get("id")

        # update resource record
        name = 'test.example43.com'
        ttl = 120
        rdata = {
            'ip': '2002::2'
        }
        resp = self.record.update_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id,
            type=record_type, ttl=ttl, name=name, rdata=rdata)
        assert resp is not None
        assert resp.status_code == 200

        # get resource record
        resp = self.record.get_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id)
        assert resp is not None
        assert resp.status_code == 200

        # delete resource record
        resp = self.record.delete_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id)
        assert resp is not None
        assert resp.status_code == 204

    def test_3_resource_records_actions(self):
        """ DNS record CNAME actions """
        record_type = 'CNAME'
        name = 'test.example56.com'
        ttl = 60
        rdata = {
            'cname': 'test.example56.com'
        }
        # create resource record
        resp = self.record.create_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, type=record_type, ttl=ttl, name=name, rdata=rdata)
        assert resp is not None
        assert resp.status_code == 200
        record_id = resp.get_result().get("id")

        # update resource record
        name = 'test.example43.com'
        ttl = 120
        rdata = {
            'cname': 'test.example43.com'
        }
        resp = self.record.update_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id,
            type=record_type, ttl=ttl, name=name, rdata=rdata)
        assert resp is not None
        assert resp.status_code == 200

        # get resource record
        resp = self.record.get_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id)
        assert resp is not None
        assert resp.status_code == 200

        # delete resource record
        resp = self.record.delete_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id)
        assert resp is not None
        assert resp.status_code == 204

    def test_4_resource_records_actions(self):
        """ DNS record MX actions """
        record_type = 'MX'
        name = 'test.example76.com'
        ttl = 60
        rdata = {
            'exchange': 'mail.test.example76.com',
            'preference': 256
        }
        # create resource record
        resp = self.record.create_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, type=record_type, ttl=ttl, name=name, rdata=rdata)
        assert resp is not None
        assert resp.status_code == 200
        record_id = resp.get_result().get("id")

        # update resource record
        name = 'test.example43.com'
        ttl = 120
        rdata = {
            'exchange': 'mail.test.example43.com',
            'preference': 256
        }
        resp = self.record.update_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id,
            type=record_type, ttl=ttl, name=name, rdata=rdata)
        assert resp is not None
        assert resp.status_code == 200

        # get resource record
        resp = self.record.get_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id)
        assert resp is not None
        assert resp.status_code == 200

        # delete resource record
        resp = self.record.delete_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id)
        assert resp is not None
        assert resp.status_code == 204

    def test_5_resource_records_actions(self):
        """ DNS record SRV actions """
        record_type = 'SRV'
        name = 'test.example76.com'
        ttl = 60
        rdata = {
            "priority": 100,
            "weight": 100,
            "port": 8000,
            "target": "test.example76.com"
        }
        service_name = "_sip"
        protocol = "udp"
        # create resource record
        resp = self.record.create_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, type=record_type,
            ttl=ttl, name=name, rdata=rdata, service=service_name, protocol=protocol)
        assert resp is not None
        assert resp.status_code == 200
        record_id = resp.get_result().get("id")

        # update resource record
        name = 'test.example43.com'
        ttl = 120
        rdata = {
            "priority": 200,
            "weight": 200,
            "port": 8001,
            "target": "test.example43.com"
        }
        service_name = "_sip"
        protocol = "tcp"
        resp = self.record.update_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id,
            type=record_type, ttl=ttl, name=name, rdata=rdata, service=service_name, protocol=protocol)
        assert resp is not None
        assert resp.status_code == 200

        # get resource record
        resp = self.record.get_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id)
        assert resp is not None
        assert resp.status_code == 200

        # delete resource record
        resp = self.record.delete_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id)
        assert resp is not None
        assert resp.status_code == 204

    def test_6_resource_records_actions(self):
        """ DNS record PTR actions """

        record_type = 'A'
        name = 'example76'
        content = '2.2.2.2'
        ttl = 60
        rdata = {
            'ip': content
        }
        # create resource record
        resp = self.record.create_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, type=record_type, ttl=ttl, name=name, rdata=rdata)
        assert resp is not None
        assert resp.status_code == 200

        record_type = 'A'
        name = 'example43'
        content = '2.2.2.3'
        ttl = 60
        rdata = {
            'ip': content
        }
        # create resource record
        resp = self.record.create_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, type=record_type, ttl=ttl, name=name, rdata=rdata)
        assert resp is not None
        assert resp.status_code == 200

        record_type = 'PTR'
        name = '2.2.2.2'
        ttl = 60
        rdata = {
            "ptrdname": "example76.test.example36.com"
        }
        # create resource record
        resp = self.record.create_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, type=record_type,
            ttl=ttl, rdata=rdata, name=name)
        assert resp is not None
        assert resp.status_code == 200
        record_id = resp.get_result().get("id")

        # update resource record
        ttl = 120
        resp = self.record.update_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id, ttl=ttl)
        assert resp is not None
        assert resp.status_code == 200

        # get resource record
        resp = self.record.get_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id)
        assert resp is not None
        assert resp.status_code == 200

        # delete resource record
        resp = self.record.delete_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id)
        assert resp is not None
        assert resp.status_code == 204

    def test_7_resource_records_actions(self):
        """ DNS record TXT actions """
        record_type = 'TXT'
        name = 'test.example76.com'
        ttl = 60
        rdata = {
            'text': 'this a text record'
        }
        # create resource record
        resp = self.record.create_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, type=record_type,
            ttl=ttl, name=name, rdata=rdata)
        assert resp is not None
        assert resp.status_code == 200
        record_id = resp.get_result().get("id")

        # update resource record
        name = 'test.example43.com'
        ttl = 120
        rdata = {
            'text': 'this a text record update'
        }
        resp = self.record.update_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id,
            type=record_type, ttl=ttl, name=name, rdata=rdata)
        assert resp is not None
        assert resp.status_code == 200

        # get resource record
        resp = self.record.get_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id)
        assert resp is not None
        assert resp.status_code == 200

        # delete resource record
        resp = self.record.delete_resource_record(
            instance_id=self.instance_id, dnszone_id=self.zone_id, record_id=record_id)
        assert resp is not None
        assert resp.status_code == 204

    def test_1_resource_records_negative(self):
        instance_id = None
        dnszone_id = "123456"
        with self.assertRaises(ValueError) as val:
            self.record.create_resource_record(instance_id=instance_id,
                                               dnszone_id=dnszone_id)
            self.assertEqual(val.exception.msg, 'instance_id must be provided')
        instance_id = "123456"
        dnszone_id = None
        with self.assertRaises(ValueError) as val:
            self.record.create_resource_record(instance_id=instance_id,
                                               dnszone_id=dnszone_id)
            self.assertEqual(val.exception.msg, 'dnszone_id must be provided')

        instance_id = None
        dnszone_id = "123456"
        with self.assertRaises(ValueError) as val:
            self.record.update_resource_record(instance_id=instance_id,
                                               dnszone_id=dnszone_id, record_id=None)
            self.assertEqual(val.exception.msg, 'instance_id must be provided')
        instance_id = "123456"
        dnszone_id = None
        with self.assertRaises(ValueError) as val:
            self.record.update_resource_record(instance_id=instance_id,
                                               dnszone_id=dnszone_id, record_id=None)
            self.assertEqual(val.exception.msg, 'dnszone_id must be provided')

        instance_id = "123456"
        dnszone_id = "12345"
        with self.assertRaises(ValueError) as val:
            self.record.update_resource_record(instance_id=instance_id,
                                               dnszone_id=dnszone_id, record_id=None)
            self.assertEqual(val.exception.msg, 'record_id must be provided')

        instance_id = None
        dnszone_id = "123456"
        with self.assertRaises(ValueError) as val:
            self.record.delete_resource_record(instance_id=instance_id,
                                               dnszone_id=dnszone_id, record_id=None)
            self.assertEqual(val.exception.msg, 'instance_id must be provided')
        instance_id = "123456"
        dnszone_id = None
        with self.assertRaises(ValueError) as val:
            self.record.delete_resource_record(instance_id=instance_id,
                                               dnszone_id=dnszone_id, record_id=None)
            self.assertEqual(val.exception.msg, 'dnszone_id must be provided')
        instance_id = "123456"
        dnszone_id = "12345"
        with self.assertRaises(ValueError) as val:
            self.record.delete_resource_record(instance_id=instance_id,
                                               dnszone_id=dnszone_id, record_id=None)
            self.assertEqual(val.exception.msg, 'record_id must be provided')

        instance_id = None
        dnszone_id = "123456"
        with self.assertRaises(ValueError) as val:
            self.record.get_resource_record(instance_id=instance_id,
                                            dnszone_id=dnszone_id, record_id=None)
            self.assertEqual(val.exception.msg, 'instance_id must be provided')
        instance_id = "123456"
        dnszone_id = None
        with self.assertRaises(ValueError) as val:
            self.record.get_resource_record(instance_id=instance_id,
                                            dnszone_id=dnszone_id, record_id=None)
            self.assertEqual(val.exception.msg, 'dnszone_id must be provided')
        instance_id = "123456"
        dnszone_id = "12345"
        with self.assertRaises(ValueError) as val:
            self.record.get_resource_record(instance_id=instance_id,
                                            dnszone_id=dnszone_id, record_id=None)
            self.assertEqual(val.exception.msg, 'record_id must be provided')

        instance_id = None
        dnszone_id = "123456"
        with self.assertRaises(ValueError) as val:
            self.record.list_resource_records(instance_id=instance_id,
                                              dnszone_id=dnszone_id)
            self.assertEqual(val.exception.msg, 'instance_id must be provided')
        instance_id = "123456"
        dnszone_id = None
        with self.assertRaises(ValueError) as val:
            self.record.list_resource_records(instance_id=instance_id,
                                              dnszone_id=dnszone_id)
            self.assertEqual(val.exception.msg, 'dnszone_id must be provided')


class TestPermittedNetworksForDnsZonesV1(unittest.TestCase):
    """The Permitted Networks for DNS V1 service test class."""

    def setUp(self):
        """ test case setup """
        if not os.path.exists(configFile):
            raise unittest.SkipTest(
                'External configuration not available, skipping...')
        self.instance_id = os.getenv("DNS_SVCS_INSTANCE_ID")
        self.vpc_crn = os.getenv("DNS_SVCS_VPC_CRN")
        self.zone_id = ""
        # create zone class object
        self.zone = DnsSvcsV1.new_instance(service_name="dns_svcs")
        self._create_dns_zones()
        # create permitted nework class object
        self.nw = DnsSvcsV1.new_instance(
            service_name="dns_svcs")

    def tearDown(self):
        """ tear down """
        # Delete the resources
        print("Clean up complete")

    def _create_dns_zones(self):
        name = "test.example36.com"
        label = "us-south"
        resp = self.zone.create_dnszone(
            instance_id=self.instance_id, name=name, label=label)
        assert resp is not None
        assert resp.status_code == 200
        self.zone_id = resp.get_result().get("id")

    def _clean_dns_resource_records(self):
        # delete dns zones
        response = self.zone.list_dnszones(instance_id=self.instance_id)
        assert response is not None
        assert response.status_code == 200
        result = response.get_result().get("dnszones")
        for zone in result:
            self.zone.delete_dnszone(
                instance_id=self.instance_id, dnszone_id=zone.get("id"))

    def test_1_permitted_network_actions(self):
        """ test pdns permitted network """
        pnw = {
            'vpc_crn': self.vpc_crn
        }
        # permit = [pnw]
        resp = self.nw.create_permitted_network(
            instance_id=self.instance_id, dnszone_id=self.zone_id, type='vpc', permitted_network=pnw)
        assert resp is not None
        assert resp.status_code == 200
        network_id = resp.get_result().get("id")

        resp = self.nw.get_permitted_network(
            instance_id=self.instance_id, dnszone_id=self.zone_id, permitted_network_id=network_id)
        assert resp is not None
        assert resp.status_code == 200

        resp = self.nw.list_permitted_networks(
            instance_id=self.instance_id, dnszone_id=self.zone_id)
        assert resp is not None
        assert resp.status_code == 200

        resp = self.nw.delete_permitted_network(
            instance_id=self.instance_id, dnszone_id=self.zone_id, permitted_network_id=network_id)
        assert resp is not None
        assert resp.status_code == 202

    def test_1_permitted_network_negative(self):
        instance_id = None
        dnszone_id = "123456"
        with self.assertRaises(ValueError) as val:
            self.nw.create_permitted_network(instance_id=instance_id,
                                             dnszone_id=dnszone_id)
            self.assertEqual(val.exception.msg, 'instance_id must be provided')
        instance_id = "123456"
        dnszone_id = None
        with self.assertRaises(ValueError) as val:
            self.nw.create_permitted_network(instance_id=instance_id,
                                             dnszone_id=dnszone_id)
            self.assertEqual(val.exception.msg, 'dnszone_id must be provided')

        instance_id = None
        dnszone_id = "123456"
        with self.assertRaises(ValueError) as val:
            self.nw.delete_permitted_network(instance_id=instance_id,
                                             dnszone_id=dnszone_id, permitted_network_id=None)
            self.assertEqual(val.exception.msg, 'instance_id must be provided')
        instance_id = "123456"
        dnszone_id = None
        with self.assertRaises(ValueError) as val:
            self.nw.delete_permitted_network(instance_id=instance_id,
                                             dnszone_id=dnszone_id, permitted_network_id=None)
            self.assertEqual(val.exception.msg, 'dnszone_id must be provided')

        instance_id = None
        dnszone_id = "123456"
        with self.assertRaises(ValueError) as val:
            self.nw.get_permitted_network(instance_id=instance_id,
                                          dnszone_id=dnszone_id, permitted_network_id=None)
            self.assertEqual(val.exception.msg, 'instance_id must be provided')
        instance_id = "123456"
        dnszone_id = None
        with self.assertRaises(ValueError) as val:
            self.nw.get_permitted_network(instance_id=instance_id,
                                          dnszone_id=dnszone_id, permitted_network_id=None)
            self.assertEqual(val.exception.msg, 'dnszone_id must be provided')

        instance_id = None
        dnszone_id = "123456"
        with self.assertRaises(ValueError) as val:
            self.nw.list_permitted_networks(instance_id=instance_id,
                                            dnszone_id=dnszone_id)
            self.assertEqual(val.exception.msg, 'instance_id must be provided')
        instance_id = "123456"
        dnszone_id = None
        with self.assertRaises(ValueError) as val:
            self.nw.list_permitted_networks(instance_id=instance_id,
                                            dnszone_id=dnszone_id)
            self.assertEqual(val.exception.msg, 'dnszone_id must be provided')


class TestGlobalLoadBalancersV1 (unittest.TestCase):
    """The Global Load Balancers for DNS V1 service test class."""

    def setUp(self):
        """ test case setup """

        if not os.path.exists(configFile):
            raise unittest.SkipTest(
                'External configuration not available, skipping...')

        self.instance_id = os.getenv("DNS_SVCS_INSTANCE_ID")
        self.zone_id = ""

        # create zone class object
        self.zone = DnsSvcsV1.new_instance(service_name="dns_svcs")

        # create global load balancers record class object
        self.globalLoadBalancers = DnsSvcsV1.new_instance(
            service_name="dns_svcs")
        self._create_dns_zones()

    def tearDown(self):
        """ tear down """
        # Delete Global load balancers
        self._clean_dns_globalloadbalancers()
        print("Clean up complete")

    def _create_dns_zones(self):
        name = "test.example36.com"
        label = "us-south"
        resp = self.zone.create_dnszone(
            instance_id=self.instance_id, name=name, label=label)
        assert resp is not None
        assert resp.status_code == 200
        self.zone_id = resp.get_result().get("id")

    def _clean_dns_globalloadbalancers(self):
        # delete all dns Load Balancer
        response = self.globalLoadBalancers.list_load_balancers(
            instance_id=self.instance_id, dnszone_id=self.zone_id)
        assert response is not None
        assert response.status_code == 200
        loadbalancers = {}
        loadbalancers = response.get_result().get("load_balancers")
        for loadbalancer in loadbalancers:
            self.globalLoadBalancers.delete_load_balancer(
                instance_id=self.instance_id, dnszone_id=self.zone_id, lb_id=loadbalancer.get("id"))
            assert response is not None
        # delete all dns Pools
        response = self.globalLoadBalancers.list_pools(
            instance_id=self.instance_id)
        assert response is not None
        assert response.status_code == 200
        pools = {}
        pools = response.get_result().get("pools")
        for pool in pools:
            self.globalLoadBalancers.delete_pool(
                instance_id=self.instance_id, pool_id=pool.get("id"))
            assert response is not None
        # delete all dns Monitors
        response = self.globalLoadBalancers.list_monitors(
            instance_id=self.instance_id)
        assert response is not None
        assert response.status_code == 200
        monitors = {}
        monitors = response.get_result().get("monitors")
        for monitor in monitors:
            self.globalLoadBalancers.delete_monitor(
                instance_id=self.instance_id, monitor_id=monitor.get("id"))
            assert response is not None
        # delete dns zones
        response = self.zone.list_dnszones(instance_id=self.instance_id)
        assert response is not None
        assert response.status_code == 200
        result = response.get_result().get("dnszones")
        for zone in result:
            self.zone.delete_dnszone(
                instance_id=self.instance_id, dnszone_id=zone.get("id"))

    ################## global load balancers integration test cases ##################
    def test_1_dns_globalloadbalancers(self):
        """ create,get,update,delete GLB monitor """

        name = 'testmonitor1'
        lbtype = 'HTTP'
        description = 'Creating testmonitor1'
        port = 8080
        interval = 60
        retries = 0
        timeout = 5
        method = 'GET'
        path = "helth"
        header = {"Host": ["example.com"], "X-App-ID": ["abc123"]}
        allow_insecure = True
        expected_body = "alive"
        # Create monitor
        response = self.globalLoadBalancers.create_monitor(
            instance_id=self.instance_id, name=name, type=lbtype, description=description, port=port, interval=interval, retries=retries, timeout=timeout)
        assert response is not None
        assert response.status_code == 200
        self.monitor_id = response.get_result().get("id")
        assert name == response.get_result().get("name")
        assert lbtype == response.get_result().get("type")
        assert description == response.get_result().get("description")
        assert interval == response.get_result().get("interval")
        # Get monitor
        response = self.globalLoadBalancers.get_monitor(
            instance_id=self.instance_id, monitor_id=self.monitor_id)
        assert response is not None
        assert response.status_code == 200
        # Update monitor
        lbtype = 'HTTPS'
        description = 'Updating testmonitor1'
        interval = 70
        timeout = 10
        response = self.globalLoadBalancers.update_monitor(
            instance_id=self.instance_id, monitor_id=self.monitor_id, type=lbtype, description=description, interval=interval, timeout=timeout)
        assert response is not None
        assert response.status_code == 200
        assert lbtype == response.get_result().get("type")
        assert description == response.get_result().get("description")

        """ createcreate,get,update,delete  GLB Pool """

        # Create Pools
        name = "testPool"
        origins = [{"name": "app-server-1",
                    "address": "10.10.10.8", "enabled": True}]
        description = "create testpool"
        enabled = True
        healthy_origins_threshold = 1
        response = self.globalLoadBalancers.create_pool(instance_id=self.instance_id, name=name, origins=origins,
                                                        description=description, enabled=enabled, healthy_origins_threshold=healthy_origins_threshold)
        assert response is not None
        assert response.status_code == 200
        self.pool_id = response.get_result().get("id")
        assert name == response.get_result().get("name")
        assert description == response.get_result().get("description")
        assert enabled == response.get_result().get("enabled")
        assert healthy_origins_threshold == response.get_result().get(
            "healthy_origins_threshold")
        # GET pool
        response = self.globalLoadBalancers.get_pool(
            instance_id=self.instance_id, pool_id=self.pool_id)
        assert response is not None
        assert response.status_code == 200
        # Update pool
        name = "updatetestPool"
        description = "update testpool"
        response = self.globalLoadBalancers.update_pool(
            instance_id=self.instance_id, pool_id=self.pool_id, name=name, description=description)
        assert response is not None
        assert response.status_code == 200
        assert name == response.get_result().get("name")
        assert description == response.get_result().get("description")

        """ create,get,update,list,delete GLB LB """

        name = 'testloadbalancer'
        description = 'Creating testloadbalancer'
        default_pools = [self.pool_id]
        enabled = True
        ttl = 120
        # Create Load balancer
        response = self.globalLoadBalancers.create_load_balancer(instance_id=self.instance_id, dnszone_id=self.zone_id, name=name,
                                                                 fallback_pool=self.pool_id, default_pools=default_pools, description=description, enabled=enabled, ttl=ttl)
        assert response is not None
        assert response.status_code == 200
        self.loadbalancer_id = response.get_result().get("id")
        assert description == response.get_result().get("description")
        assert enabled == response.get_result().get("enabled")
        assert ttl == response.get_result().get("ttl")
        # GET Load balancer
        response = self.globalLoadBalancers.get_load_balancer(
            instance_id=self.instance_id, dnszone_id=self.zone_id, lb_id=self.loadbalancer_id)
        assert response is not None
        assert response.status_code == 200
        # Update Load balancer
        name = "updatetestLoadbalancer"
        description = "update testLoadbalancer"
        response = self.globalLoadBalancers.update_load_balancer(
            instance_id=self.instance_id, dnszone_id=self.zone_id, lb_id=self.loadbalancer_id, name=name, description=description)
        assert response is not None
        assert response.status_code == 200
        assert description == response.get_result().get("description")
        # List Load balancer
        response = self.globalLoadBalancers.list_load_balancers(
            instance_id=self.instance_id, dnszone_id=self.zone_id)
        assert response is not None
        assert response.status_code == 200

        # Delete Load balancer/Pool/Monitor
        response = self.globalLoadBalancers.delete_load_balancer(
            instance_id=self.instance_id, dnszone_id=self.zone_id, lb_id=self.loadbalancer_id)
        assert response is not None
        assert response.status_code == 204
        response = self.globalLoadBalancers.delete_pool(
            instance_id=self.instance_id, pool_id=self.pool_id)
        assert response is not None
        assert response.status_code == 204
        response = self.globalLoadBalancers.delete_monitor(
            instance_id=self.instance_id, monitor_id=self.monitor_id)
        assert response is not None
        assert response.status_code == 204

    def test_2_list_dns_globalloadbalancers(self):

        # List monitor
        for i in range(3):
            name = 'testmonitor'+str(i)
            lbtype = 'HTTP'
            description = 'Creating testmonitor '+str(i)
            response = self.globalLoadBalancers.create_monitor(
                instance_id=self.instance_id, name=name, type=lbtype, description=description)
            assert response is not None
            assert response.status_code == 200
        response = self.globalLoadBalancers.list_monitors(
            instance_id=self.instance_id)
        assert response is not None
        assert response.status_code == 200

        # List Pools
        for i in range(3):
            name = "testPool"+str(i)
            origins = [{"name": "app-server-"+str(i),
                        "address": "10.10.10.8", "enabled": True}]
            description = "create testpool"+str(i)
            enabled = True
            healthy_origins_threshold = 1
            response = self.globalLoadBalancers.create_pool(
                instance_id=self.instance_id, name=name, origins=origins, description=description, enabled=enabled, healthy_origins_threshold=healthy_origins_threshold)
            assert response is not None
            assert response.status_code == 200
        response = self.globalLoadBalancers.list_pools(
            instance_id=self.instance_id)
        assert response is not None
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
