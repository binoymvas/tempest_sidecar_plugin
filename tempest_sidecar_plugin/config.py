# -*- coding: utf-8 -*-
# _______________________________________________________
# | File Name: config.py                                |
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
from oslo_config import cfg
from tempest import config

#Adding the groups
service_available_group = cfg.OptGroup(
    name="service_available",
    title="Available OpenStack Services"
)

ServiceAvailableGroup = [
    cfg.BoolOpt("tempest_sidecar_plugin", default=True,
                help="Whether or not sidecar plugin is expected to be available")
]

tempest_sidecar_plugin_group = cfg.OptGroup(
    name="tempest_sidecar",
    title="Tempest Sidecar Test Variables"
)

TempestSidecarPluginGroup = [
    cfg.StrOpt("my_custom_variable", default="custom value",
               help="My custom variable.")
]
