"""Tests de validation """

import socket

from unittest.mock import patch

import pytest
from network_toolkit.validation import (
    ValidationError,
    parse_port_range,
    resolve_target,
    validate_port_range,
    validate_threads,
)


class TestParsePortRange:
    """Test pour parse_port_range"""

#--- parse_port_range ---

    def test_valid_range(self):
        assert parse_port_range("20-100") == (20, 100)


    def test_single_port(self):
        assert parse_port_range("3306-3306") == (3306, 3306)

    
    def test_full_range(self):
        assert parse_port_range("1-65535") == (1, 65535)


    def test_missing_dash(self):
        with pytest.raises(ValidationError, match="Format de plage invalide"):
            parse_port_range("20")


    def test_non_numeric(self):
        with pytest.raises(ValidationError, match="nombres entiers"):
            parse_port_range("abc-def")

    def test_reversed_range(self):
        with pytest.raises(ValidationError, match="Plage inversée"):
            parse_port_range("100-20")

    def test_port_zero(self):
        with pytest.raises(ValidationError, match="hors bornes"):
            parse_port_range("0-100")

    
    def test_port_too_high(self):
        with pytest.raises(ValidationError, match="hors bornes"):
            parse_port_range("100-70000")


    def test_empty_after_dash(self):
        with pytest.raises(ValidationError):
            parse_port_range("20-")


    def test_empty_before_dash(self):
        with pytest.raises(ValidationError):
            parse_port_range("-100")

    def test_empty_string(self):
        with pytest.raises(ValidationError):
            parse_port_range("")


# --- validate_port_range ---

class TestValidatePortRange:
    def test_valid_bounds(self):
        validate_port_range(1, 65535)
        validate_port_range(20, 100)
        validate_port_range(3306, 3306)

    def test_zero_start(self):
        with pytest.raises(ValidationError):
            validate_port_range(0, 100)


    def test_too_high_end(self):
        with pytest.raises(ValidationError):
            validate_port_range(100, 70000)


    def test_reversed(self):
        with pytest.raises(ValidationError):
            validate_port_range(100, 20)
    

    def test_negative(self):
        with pytest.raises(ValidationError):
            validate_port_range(-1, 100)

# --- Tests pour validate_threads ---

class TestValidateThreads:
    @pytest.mark.parametrize("n", [1, 50, 100, 500])
    def test_valid(self, n):
        validate_threads(n)

    
    @pytest.mark.parametrize("n", [0, -1, 501, 1000])
    def test_invalid(self, n):
        with pytest.raises(ValidationError):
            validate_threads(n)



# --- Test pour resolve_target ---

class TestResolveTarget:
    def test_ip_literal(self):
        assert resolve_target("127.0.0.1") == "127.0.0.1"

    def test_localhost(self):
        assert resolve_target("localhost") == "127.0.0.1"

    def test_empty(self):
        with pytest.raises(ValidationError):
            resolve_target("")

    def test_withespace(self):
        with pytest.raises(ValidationError):
            resolve_target("  ")

    @patch("network_toolkit.validation.socket.gethostbyname")
    def test_unresolvable(self, mock_gethostbyname):
        mock_gethostbyname.side_effect = socket.gaierror("Name not known")
        with pytest.raises(ValidationError, match="Impossible de résoudre"):
            resolve_target("inexistant.invalid")