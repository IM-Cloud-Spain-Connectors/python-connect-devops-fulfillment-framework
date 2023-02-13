#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from typing import Dict

from rndi.dicontainer.adapter import BaseServiceProvider as ServiceProvider


class ConfigurationServiceProvider(ServiceProvider):
    def __init__(self, config: Dict[str, str]):
        binds = {'config': {'to_instance': config}}

        # iterate over all the items in the configuration and register
        # them into the Container as standalone value in lower case.
        # CACHE_DRIVER -> cache_driver
        for key, value in config.items():
            binds[key.lower()] = {'to_instance': value.strip()}

        super().__init__(binds)
