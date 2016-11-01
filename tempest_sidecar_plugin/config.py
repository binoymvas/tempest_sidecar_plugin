from oslo_config import cfg
from tempest import config

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
