#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from __future__ import annotations

import inspect
from abc import ABC, abstractmethod
from logging import LoggerAdapter
from typing import Dict, List, Optional, Type, Union

from connect.client import AsyncConnectClient, ConnectClient
from connect.eaas.core.responses import BackgroundResponse
from rndi.connect.business_transaction_middleware.middleware import make_middleware_callstack, Middleware
from rndi.connect.business_transactions.adapters import prepare, select
from rndi.connect.business_transactions.contracts import BackgroundTransaction
from rndi.dicontainer.adapter import BaseServiceProvider as ServiceProvider, Container
from rndi.connect.devops_fulfillment_framework.providers.cache import CacheServiceProvider
from rndi.connect.devops_fulfillment_framework.providers.configuration import ConfigurationServiceProvider
from rndi.connect.devops_fulfillment_framework.providers.connect import ConnectServiceProvider
from rndi.connect.devops_fulfillment_framework.providers.offline import OfflineServiceProvider

AnyConnectClient = Union[ConnectClient, AsyncConnectClient]


class Saga(ABC):
    providers: Dict[str, Type[ServiceProvider]] = {
        'cache': CacheServiceProvider,
        'offline': OfflineServiceProvider,
    }

    def __init__(self, providers: Optional[Dict[str, ServiceProvider]] = None):
        # first, instantiate the service providers.
        defaults = {key: provider() for key, provider in self.__class__.providers.items()}
        # update the service providers with the given ones (already instantiated).
        if providers is not None:
            defaults.update(providers)

        self.__container = Container([provider for _, provider in defaults.items()])

    @classmethod
    def make(
            cls,
            config: Dict[str, str],
            client: AnyConnectClient,
            logger: LoggerAdapter,
            request: Optional[dict] = None,
    ) -> Saga:
        return cls({
            'config': ConfigurationServiceProvider(config),
            'connect': ConnectServiceProvider(client, logger, request),
        })

    @property
    def container(self) -> Container:
        return self.__container

    @abstractmethod
    def transactions(self, request: dict) -> List[Type[BackgroundTransaction]]:
        """
        Provide the list of transactions for the Saga.

        :param request: dict The Connect request dictionary.
        :return: List[Type[BackgroundTransaction]]
        """

    @abstractmethod
    def middlewares(self, request: dict) -> List[Type[Middleware]]:
        """
        Provide the list of Middlewares for each transaction of the saga.

        :param request: dict The Connect request dictionary.
        :return: List[Type[Middleware]]
        """

    def resolve(self, request: dict) -> BackgroundResponse:
        transactions: List[BackgroundTransaction] = [
            self.container.get(t) if inspect.isclass(t) else t for t in self.transactions(request)
        ]

        middlewares: List[Middleware] = [
            self.container.get(m) if inspect.isclass(m) else m for m in self.middlewares(request)
        ]

        transaction = make_middleware_callstack(middlewares, prepare(select(transactions, request)))

        return transaction(request)
