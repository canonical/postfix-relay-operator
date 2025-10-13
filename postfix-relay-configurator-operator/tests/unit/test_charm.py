# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Unit tests for the Postfix Relay charm."""

from unittest.mock import ANY, Mock, patch

import ops.testing
from ops.testing import Context, State

import charm
from state import ConfigurationError


@patch("charm.State.from_charm", Mock(side_effect=ConfigurationError("Invalid configuration")))
def test_invalid_config(context: Context[charm.PostfixRelayConfiguratorCharm]) -> None:
    """
    arrange: Invalid charm config.
    act: Run the config-changed event hook on the charm.
    assert: The unit status is set to blocked with the correct error message.
    """
    charm_state = State(config={}, leader=True)

    out = context.run(context.on.config_changed(), charm_state)

    assert out.unit_status == ops.testing.BlockedStatus("Invalid config")


@patch.object(
    charm, "construct_postfix_config_params", wraps=charm.construct_postfix_config_params
)
@patch("charm.utils.write_file", Mock())
def test_configure_relay(
    mock_construct_postfix_config_params: Mock,
    context: Context[charm.PostfixRelayConfiguratorCharm],
) -> None:
    """
    arrange: Configure the charm with defaults.
    act: Run the config-changed event hook.
    assert: The charm constructs the correct FQDN.
    """
    charm_state = State(
        config={},
        relations=[],
        leader=True,
    )

    out = context.run(context.on.config_changed(), charm_state)

    mock_construct_postfix_config_params.assert_called_once_with(
        charm_state=ANY,
    )

    assert out.unit_status == ops.testing.ActiveStatus()
