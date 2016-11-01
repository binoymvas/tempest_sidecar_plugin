# -*- coding: utf-8 -*-
# _______________________________________________________
# | File Name: plugin.py                                |
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
import os
from tempest import config
from tempest.test_discover import plugins
from tempest_sidecar_plugin import config as config_share

class SidecarPlugin(plugins.TempestPlugin):
    def get_opt_lists(self):
        """Get a list of options for sample config generation"""
        return [(
            config_share.tempest_sidecar_plugin_group.name,
            config_share.TempestSidecarPluginGroup)]

    def load_tests(self):
        """Return the information necessary to load the tests in the plugin.
        Returns:    a tuple with the first value being the test_dir and the second being the top_level
        Return type:    tuple
        """
        base_path = os.path.split(os.path.dirname(
            os.path.abspath(__file__)))[0]
        test_dir = "tempest_sidecar_plugin/tests"
        full_test_dir = os.path.join(base_path, test_dir)
        return full_test_dir, base_path

    def register_opts(self, conf):
        """Add additional configuration options to tempest."""
        config.register_opt_group(
            conf,
            config_share.service_available_group,
            config_share.ServiceAvailableGroup)
        config.register_opt_group(
            conf,
            config_share.tempest_sidecar_plugin_group,
            config_share.TempestSidecarPluginGroup)