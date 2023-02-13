# Python Connect DevOps Fulfillment Framework

[![Test](https://github.com/othercodes/python-connect-devops-fulfillment-framework/actions/workflows/test.yml/badge.svg)](https://github.com/othercodes/python-connect-devops-fulfillment-framework/actions/workflows/test.yml)

Framework to ease and speedup the development of a Connect DevOps Fulfillment Extension.

## Installation

The easiest way to install the Connect DevOps Fulfillment Framework is to get the latest version from PyPI:

```bash
# using poetry
poetry add rndi-connect-devops-fulfillment-framework
# using pip
pip install rndi-connect-devops-fulfillment-framework
```

## Service Container

The service container is a powerful tool for managing class dependencies and performing dependency injection.
Dependency injection is a fancy phrase that essentially means this: class dependencies are "injected" into the class
via the constructor or, in some cases, "setter" methods.

```python
from rndi.cache.contracts import Cache
from rndi.connect.business_transactions.adapters import BackgroundTransaction


class CreateUserTransaction(BackgroundTransaction):
    def __init__(self, cache: Cache):
        self.cache = cache
```

In this example, the `CreateUserTransaction` needs to use retrieve some data from the cache. So, we will inject a
service that is able to retrieve the data from cache. In this context, our Cache most likely uses SQLiteCache to get
data from cache. However, since the cache adapter is injected, we are able to easily swap it out with another
implementation. We are also able to easily "mock", or create a dummy implementation of the Cache when testing our
application.

For more information about the Service Container please check [DI Container](https://github.com/).

## Service Providers

Service providers are the central place of all fulfillment extensions. Each transaction services and core services, are
bootstrapped via service providers.

But, what do we mean by "bootstrapped"? In general, we mean registering things,
including registering service container bindings and middlewares. Service providers are the central place to configure
your application.

```python
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

```

The example above allows the usage of different cache adapters.

For more information about the Service Container please check [Service Providers](https://github.com/).

## Transactions

Once the package is installed, you need to start declaring your transactions.

```python
from connect.eaas.core.responses import BackgroundResponse
from rndi.connect.business_transactions.adapters import BackgroundTransaction
from rndi.connect.business_transactions.contracts import TBackgroundResponse


class SomeCoreTransaction(BackgroundTransaction):
    def __init__(self, client, logger, config, cache):
        self.client = client
        self.logger = logger
        self.config = config
        self.cache = cache

    def name(self) -> str:
        return 'Sample Transaction'

    def should_execute(self, request: dict) -> bool:
        return True

    def execute(self, request: dict) -> TBackgroundResponse:
        print("Running Execute!")
        return BackgroundResponse.done()

    def compensate(self, request: dict, e: Exception) -> TBackgroundResponse:
        raise e

```

## Sagas

Next we need to declare the complete flow or `Saga` that will contain the different transactions:

```python
from typing import List, Type
from rndi.connect.devops_fulfillment_framework.application import Saga
from rndi.connect.business_transaction_middleware.middleware import Middleware
from rndi.connect.business_transactions.adapters import BackgroundTransaction
from extension.transactions import SomeCoreTransaction


class PurchaseSaga(Saga):
    def middlewares(self, request: dict) -> List[Type[Middleware]]:
        return []

    def transactions(self, request: dict) -> List[Type[BackgroundTransaction]]:
        return [
            SomeCoreTransaction,
        ]

```

Finally, we just need to execute the saga in the correct method of the fulfillment extension:

```python
from connect.eaas.core.decorators import event
from connect.eaas.core.extension import EventsApplicationBase
from extension.sagas import PurchaseSaga


class SampleFulfillmentExtensionEventsApplication(EventsApplicationBase):
    @event('asset_purchase_request_processing', statuses=['pending'])
    def handle_asset_purchase_request_processing(self, request):
        self.logger.info(f"Obtained request with id {request['id']}")
        return PurchaseSaga.make(self.config, self.client, self.logger).resolve(request)
```
