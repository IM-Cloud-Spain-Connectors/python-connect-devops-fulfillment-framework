from typing import List, Type

import pytest
from rndi.connect.business_transaction_middleware.middleware import Middleware
from rndi.connect.business_transactions.contracts import BackgroundTransaction
from rndi.connect.business_transactions.exceptions import TransactionNotSelected
from rndi.connect.devops_fulfillment_framework.application import Saga
from tests.sample import SomeCoreTransaction


def test_saga_should_throw_error_on_resolve_saga_without_transactions(config, sync_client_factory, logger):
    class SampleSaga(Saga):
        def middlewares(self, request: dict) -> List[Type[Middleware]]:
            return []

        def transactions(self, request: dict) -> List[Type[BackgroundTransaction]]:
            return []

    with pytest.raises(TransactionNotSelected):
        SampleSaga \
            .make(config(), sync_client_factory([]), logger()) \
            .resolve({})


def test_saga_should_correctly_select_the_correct_transaction(config, sync_client_factory, logger):
    class SampleSaga(Saga):
        def middlewares(self, request: dict) -> List[Type[Middleware]]:
            return []

        def transactions(self, request: dict) -> List[Type[BackgroundTransaction]]:
            return [
                SomeCoreTransaction,
            ]

    request = {
        'status': 'pending',
    }

    SampleSaga \
        .make(config(), sync_client_factory([]), logger(), request) \
        .resolve(request)

    assert request.get('message') == SomeCoreTransaction
