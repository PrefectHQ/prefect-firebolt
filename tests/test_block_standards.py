import pytest
from prefect.testing.standard_test_suites import BlockStandardTestSuite

from prefect_firebolt import FireboltCredentials


@pytest.mark.parametrize("block", [FireboltCredentials])
class TestAllBlocksAdhereToStandards(BlockStandardTestSuite):
    @pytest.fixture
    def block(self, block):
        return block
