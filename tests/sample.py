from connect.eaas.core.responses import BackgroundResponse
from rndi.connect.business_transactions.contracts import BackgroundTransaction, TBackgroundResponse


class SomeCoreTransaction(BackgroundTransaction):
    def __init__(self, client, logger, config, cache):
        self.client = client
        self.logger = logger
        self.config = config
        self.cache = cache

    def name(self) -> str:
        return 'Sample Core Transaction'

    def should_execute(self, request: dict) -> bool:
        return request.get('status', 'undefined') == 'pending'

    def execute(self, request: dict) -> TBackgroundResponse:
        request['message'] = self.__class__
        return BackgroundResponse.done()

    def compensate(self, request: dict, e: Exception) -> TBackgroundResponse:
        raise e
