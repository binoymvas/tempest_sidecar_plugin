# -*- coding: utf-8 -*-
# _______________________________________________________
# | File Name: base.py                                  |
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

#Importing require modules
from oslo_log import log as logging
from tempest import config
from tempest import test

CONF = config.CONF
LOG = logging.getLogger(__name__)

class BaseTempestSidecarTest(test.BaseTestCase):

    @classmethod
    def skip_checks(cls):
        pass