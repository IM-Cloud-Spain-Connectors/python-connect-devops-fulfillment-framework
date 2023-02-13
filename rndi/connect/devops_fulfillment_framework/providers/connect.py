#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from logging import LoggerAdapter
from typing import Optional, Union

from connect.client import AsyncConnectClient, ConnectClient
from rndi.dicontainer.adapter import BaseServiceProvider as ServiceProvider

AnyConnectClient = Union[ConnectClient, AsyncConnectClient]


class ConnectServiceProvider(ServiceProvider):
    """
    Provides the Connect Services:
    - Connect Open API Client.
    - Connect Logger Adapter.
    - Connect Request Dictionary (Optional).
    """

    def __init__(self, client: AnyConnectClient, logger: LoggerAdapter, request: Optional[dict] = None):
        binds = {
            'client': {'to_instance': client},
            'logger': {'to_instance': logger},
        }

        if request is not None:
            binds['request'] = {'to_instance': request}

        super().__init__(binds)
