#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from connect.eaas.core.responses import BackgroundResponse
from rndi.connect.request_offline_criteria.rules import (
    composited_match_offline_asset_and_marketplace_parameter,
    match_request_type,
)
from rndi.dicontainer.adapter import BaseServiceProvider as ServiceProvider


class OfflineServiceProvider(ServiceProvider):
    def register(self):
        self.bind_instance('criteria', [
            composited_match_offline_asset_and_marketplace_parameter,
            match_request_type,
        ])

        # simple and default on_match operation, the request is skipped.
        self.bind_instance('on_match', lambda _: BackgroundResponse.skip())
