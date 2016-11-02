# -*- coding: utf-8 -*-
# _______________________________________________________
# | File Name: test_sidecar.py                          |
# |                                                     |
# | Package Name: Tmpest Sidecar Plugin                 |
# |                                                     |
# | Version: 1                                          |
# |                                                     |
# | Sofatware: Openstack                                |
# |_____________________________________________________|
# | Copyright: 2016@nephoscale.com                      |
# |                                                     |
# | Author:  info@nephoscale.com                        |
# |_____________________________________________________|

#importing required packages
from tempest_sidecar_plugin.tests.api import base
from tempest import test
from tempest import config
import json
import subprocess
from sidecarclient import client
import unittest
import ConfigParser
import os

#Defining the global connection string
_sidecar_ = None
CONF = config.CONF

class TestTempestSidecar(base.BaseTempestSidecarTest):

    @classmethod
    def resource_setup(cls):
        """
        # | Constructor function. Initialization part. We pass the required details for connecting to sidecar client
        # | 
        # | Arguments: class method
        # |
        # | Return Ttype: NA
        """
        
        #Defining the global connection string
        global _sidecar_
 
        #Creating connection if not avaialble
        if not _sidecar_:
            _sidecar_ = client.Client(
                            username=CONF.auth.admin_username,
                            password=CONF.auth.admin_password,
                            auth_url=CONF.identity.uri,
                            region_name=CONF.identity.region,
                            tenant_name=CONF.auth.admin_project_name,
                            timeout=10,
                            insecure=False
                    )
        super(TestTempestSidecar, cls).resource_setup()

    @classmethod
    def resource_cleanup(cls):
        """
        # | Cleanup function. 
        # | 
        # | Arguments: class method
        # |
        # | Return Ttype: NA
        """
        super(TestTempestSidecar, cls).resource_cleanup()

    @test.attr(type="smoke")
    def test_pecan_is_running(self):
        """
        #Function to check if the pecan service is running or not by checking the running process list
        Args:
            self
        Returns:
            NA
        """
        process = subprocess.Popen('lsof -i :9090', shell=True, stdout=subprocess.PIPE)

        #Remove the top header line and fetch the details of the enxt line
        pecan_text = process.stdout.readlines()[1:]
        pecan_text = pecan_text[0]
        service_text = pecan_text.split(' ', 1)[0]
        self.assertEqual(service_text, 'pecan')

    @test.attr(type="smoke")
    def test_event_listing(self):
        """
        Checking if any evacuate events are present
        Args:
            self
        Returns:
            True, if there are any events
        """
        events = _sidecar_.events.list()
        #Checking if there are any events
        self.assertGreaterEqual(len(events), 0)

    @test.attr(type="smoke")
    def test_event_creation(self):
        """
        Testing the event creation process
        Args:
            self
        Returns:
            True, if the details of newly created event are present
        """
        
        #Creating the events
        event = _sidecar_.events.create(
                                           name="eventName1",
                                           node_uuid="897897879jhkjk",
                                           vm_uuid_list=["gvjhsdgvjs7678", "bcjhdhgbskjch786768"]
                                           )
        
        #Getting the details of the events
        event_details = _sidecar_.events.detail(id=event.id)

        #Details should be available if an event is created
        self.assertEqual(event_details.name, 'eventName1')
        
        #Deleting the newly created event after testing
        event_deletion = _sidecar_.events.delete(id=event.id)

    @test.attr(type="smoke")
    def test_event_deletion(self):
        """
        Testing the event deletion process
        We create an event and then try to delete it.
        Args:
            self
        Returns:
            True, if the event has been deleted
        """
        
        #Creating the events
        event = _sidecar_.events.create(
                                           name="eventToBeDeleted",
                                           node_uuid="45assd4555f5d5d5",
                                           vm_uuid_list=["sdsadsadsadadas", "dadasdasdas"]
                                           )
        
        #Deleting the event and loading the event list to ensure that the event doesn't exist
        event_deletion = _sidecar_.events.delete(id=event.id)
        event_list     = _sidecar_.events.list()
        
        #Looping through each event
        for events in event_list:
            self.assertNotEqual(events.id, event.id)

    @test.attr(type="smoke")
    def test_event_edit(self):
        """
        Testing the event updation process
        First we create and event and then edit it's details
        Args:
            self
        Return:
            True, if the event details have been updated successfully
        """
        
        #Creating the events
        event = _sidecar_.events.create(
                                           name="eventBeforeUpdationn",
                                           node_uuid="45sassd4555f5d5d5",
                                           vm_uuid_list=["sdsadsadsasdadas", "dadassdasdas"]
                                           )
        
        #Editing the event and check it's details to ensure that it's updated
        event_edit = _sidecar_.events.edit(id=event.id, name='eventAfterUpdationn')
        event_details = _sidecar_.events.detail(id=event.id)

        self.assertEqual(event_details.name, 'eventAfterUpdationn')
        
        #Deleting the newly created event after testing
        event_deletion = _sidecar_.events.delete(id=event.id)


    @test.attr(type="smoke")
    def test_event_detail_display(self):
        """
        Testing the event details display
        We create an event and test if it's details are displayed correctly.
        The event will be deleted after the testing
        Args:
            self
        Return:
            True, if the event details are displayed correctly
        """
        
        #Creating the events
        event = _sidecar_.events.create(
                                           name="eventDetailDisplayTesting",
                                           node_uuid="45sassd4555f5685d5d5",
                                           vm_uuid_list=["sdsadsadggsasdadas", "dadassdffasdas"]
                                           )
        event_details = _sidecar_.events.detail(id=event.id)
        self.assertEqual(event_details.name, 'eventDetailDisplayTesting')
        self.assertEqual(event_details.node_uuid, '45sassd4555f5685d5d5')
        self.assertEqual(json.dumps(event_details.vm_uuid_list), '["sdsadsadggsasdadas", "dadassdffasdas"]')
        
        #Deleting the newly created event after testing
        event_deletion = _sidecar_.events.delete(id=event.id)

    @test.attr(type="smoke")
    def test_healthcheck_status(self):
        """
        Testing the log creation process
        Args:
            self
        Return:
            True, if any logs exist
        """
        
        #Getting the status of the healthcheck events
        event_logs = _sidecar_.events.evacuate_healthcheck_status()
        self.assertGreaterEqual(len(event_logs), 0)

    @test.attr(type="smoke")
    def test_sidecar_version_listing(self):
        """
        Testing if the versions are listed correctly
        Args:
            self
        Return:
            True, if versions are present in the output
        """
        
        #Getting the version 
        version_details = _sidecar_.versions.list()
        self.assertEqual(version_details[0].version, 'v2')
        self.assertEqual(version_details[0].status, 'current')


    @test.attr(type="smoke")
    def test_dead_time_value(self):
        """
        Function to fetch the value of dead time from config file
        Ensure that the dead time is greater than 3mins
        Args:
            self
        Return:
            True, if the dead time is greater than or equal to 180s
        """
        
        #Getting the details from the conf file
        Config = ConfigParser.ConfigParser()
        Config.read("/etc/sidecar/sidecar.conf")
        
        #Fetch the dead time value which is under the section evacuate_details
        deadtime = Config.get('evacuate_details', 'dead_time')
        self.assertGreaterEqual(deadtime, '180')

    @test.attr(type="smoke")
    def test_failure_threshold_value(self):
        """
        Function to test the failure threshold value and endure that it's minimum limit is 5mins
        Args:
            self
        Return:
            True, if the minimum limit for the failure threshold value is 5mins
        """
        
        #Getting the details from the conf file
        Config = ConfigParser.ConfigParser()
        Config.read("/etc/sidecar/sidecar.conf")
        
        #Fetch the failure threshold value which is present under the section evacuate_details
        threshold_value = Config.get('evacuate_details', 'failure_threshold')
        self.assertGreaterEqual(threshold_value, '300')

    @test.attr(type="smoke")
    def test_keystone_username(self):
        """
        Function to ensure that the keystone username has been correctly set
        Args:
            self
        Return:
            True, if the username is correct
        """
        
        #Getting the details from the conf file
        Config = ConfigParser.ConfigParser()
        Config.read("/etc/sidecar/sidecar.conf")
        keystone_username_conf_val = Config.get('keystone_authtoken', 'username')
        keystone_password_env_val  = os.environ.get('OS_USERNAME')
        self.assertEqual(keystone_username_conf_val, keystone_password_env_val)

    @test.attr(type="smoke")
    def test_keystone_password(self):
        """
        Function to ensure that the keystone password has been correctly set
        Args:
            self
        Return:
            True, if the password is correct
        """
        
        #Getting the details from the conf file
        Config = ConfigParser.ConfigParser()
        Config.read("/etc/sidecar/sidecar.conf")
        keystone_password_conf_val = Config.get('keystone_authtoken', 'password')
        keystone_password_env_val  = os.environ.get('OS_PASSWORD')
        self.assertEqual(keystone_password_conf_val, keystone_password_env_val)
    
    @test.attr(type="smoke")    
    def test_keystone_project_name(self):
        """
        Function to ensure that the keystone project has been correctly set
        Args:
            self
        Return:
            True, if the project is correct
        """

        #Getting the details from the conf file
        Config = ConfigParser.ConfigParser()
        Config.read("/etc/sidecar/sidecar.conf")
        keystone_project_conf_val = Config.get('keystone_authtoken', 'tenant_name')
        keystone_project_env_val  = os.environ.get('OS_TENANT_NAME')
        self.assertEqual(keystone_project_conf_val, keystone_project_env_val)
