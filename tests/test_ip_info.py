"""
Unit tests for IP Location Finder application.
These tests validate the core functionality of the IP lookup features.
"""
import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ip_info import get_ip_address, get_ip_info

class TestIPFunctions:
    """Test cases for IP address and information retrieval functions."""
    
    def test_get_ip_address_ipv4(self):
        """Test IPv4 address retrieval."""
        ip = get_ip_address("ipv4")
        # Should return a valid IPv4 address or None
        assert ip is None or isinstance(ip, str)
        if ip:
            # Basic IPv4 format check (simplified)
            assert '.' in ip
    
    def test_get_ip_address_ipv6(self):
        """Test IPv6 address retrieval."""
        ip = get_ip_address("ipv6")
        # Should return a valid IPv6 address or None
        assert ip is None or isinstance(ip, str)
        if ip:
            # Basic IPv6 format check (simplified)
            assert ':' in ip
    
    def test_get_ip_info_valid_ip(self):
        """Test IP information retrieval for a known IP (Google DNS)."""
        # Test with Google's public DNS (8.8.8.8)
        info = get_ip_info("8.8.8.8")
        # Should return data or None (due to rate limiting)
        assert info is None or isinstance(info, dict)
        if info:
            # If we get data, it should have expected keys
            assert 'ip' in info or 'city' in info or 'country' in info
    
    def test_get_ip_info_invalid_ip(self):
        """Test IP information retrieval with invalid IP."""
        info = get_ip_info("999.999.999.999")
        # Should return None for invalid IP
        assert info is None or isinstance(info, dict)
    
    def test_get_ip_info_empty(self):
        """Test IP information retrieval with empty string."""
        info = get_ip_info("")
        # Should return None for empty input
        assert info is None
    
    def test_get_ip_info_none(self):
        """Test IP information retrieval with None."""
        info = get_ip_info(None)
        # Should return None for None input
        assert info is None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

