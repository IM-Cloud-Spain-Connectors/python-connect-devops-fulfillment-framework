#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from logging import LoggerAdapter

from rndi.cache.adapters.sqlite.adapter import provide_sqlite_cache_adapter
from rndi.cache.contracts import Cache
from rndi.cache.provider import provide_cache
from rndi.dicontainer.adapter import BaseServiceProvider as ServiceProvider


class CacheServiceProvider(ServiceProvider):
    def provide_cache(self, config: dict, logger: LoggerAdapter) -> Cache:
        return provide_cache(config, logger, {
            'sqlite': provide_sqlite_cache_adapter,
        })
