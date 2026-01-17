"""Pytest fixtures for aiosupermicro tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses

from aiosupermicro import SupermicroRedfishClient

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict[str, Any]:
    """Load a JSON fixture file."""
    fixture_path = FIXTURES_DIR / f"{name}.json"
    with open(fixture_path) as f:
        return json.load(f)


@pytest.fixture
def mock_aiohttp() -> aioresponses:
    """Mock aiohttp responses."""
    with aioresponses() as m:
        yield m


@pytest.fixture
def base_url() -> str:
    """Base URL for tests."""
    return "https://192.168.1.100"


@pytest.fixture
def mock_session_response(mock_aiohttp: aioresponses, base_url: str) -> None:
    """Mock successful session creation."""
    mock_aiohttp.post(
        f"{base_url}/redfish/v1/SessionService/Sessions",
        payload={"SessionTimeout": 300},
        headers={"X-Auth-Token": "test-token", "Location": "/redfish/v1/SessionService/Sessions/1"},
    )


@pytest.fixture
async def client(
    mock_aiohttp: aioresponses,
    mock_session_response: None,
    base_url: str,
) -> SupermicroRedfishClient:
    """Create client with mocked session."""
    async with ClientSession() as session:
        client = SupermicroRedfishClient(
            session=session,
            host="192.168.1.100",
            username="ADMIN",
            password="ADMIN",
        )
        yield client


# Fixture data
SYSTEM_RESPONSE: dict[str, Any] = {
    "Id": "1",
    "Name": "System",
    "UUID": "12345678-1234-1234-1234-123456789012",
    "Manufacturer": "Supermicro",
    "Model": "X12STH-SYS",
    "SerialNumber": "S123456789",
    "PowerState": "On",
    "BiosVersion": "BIOS Date: 01/01/2024 Ver 2.1",
    "IndicatorLED": "Off",
    "Status": {
        "State": "Enabled",
        "Health": "OK",
        "HealthRollup": "OK",
    },
    "ProcessorSummary": {
        "Count": 1,
        "Model": "Intel Xeon W-1290",
        "Status": {"State": "Enabled", "Health": "OK"},
    },
    "MemorySummary": {
        "TotalSystemMemoryGiB": 128,
        "Status": {"State": "Enabled", "Health": "OK"},
    },
    "Boot": {
        "BootSourceOverrideTarget": "None",
        "BootSourceOverrideEnabled": "Disabled",
        "BootSourceOverrideTarget@Redfish.AllowableValues": [
            "None", "Pxe", "Hdd", "Cd", "BiosSetup"
        ],
    },
    "Actions": {
        "#ComputerSystem.Reset": {
            "ResetType@Redfish.AllowableValues": [
                "On", "ForceOff", "GracefulShutdown", "GracefulRestart", "ForceRestart"
            ],
        },
    },
}

CHASSIS_RESPONSE: dict[str, Any] = {
    "Id": "1",
    "Name": "Chassis",
    "ChassisType": "RackMount",
    "Manufacturer": "Supermicro",
    "Model": "CSE-815TQ-1MR",
    "SerialNumber": "C123456789",
    "PowerState": "On",
    "IndicatorLED": "Off",
    "Status": {
        "State": "Enabled",
        "Health": "OK",
        "HealthRollup": "OK",
    },
    "PhysicalSecurity": {
        "IntrusionSensor": "Normal",
        "IntrusionSensorNumber": 170,
    },
    "Oem": {
        "Supermicro": {
            "BoardSerialNumber": "BM123456789",
            "BoardID": "0x0A1B",
        },
    },
}

THERMAL_RESPONSE: dict[str, Any] = {
    "Id": "Thermal",
    "Name": "Thermal",
    "Temperatures": [
        {
            "MemberId": "0",
            "Name": "CPU Temp",
            "ReadingCelsius": 45,
            "Status": {"State": "Enabled", "Health": "OK"},
            "UpperThresholdCritical": 95,
            "PhysicalContext": "CPU",
        },
        {
            "MemberId": "1",
            "Name": "System Temp",
            "ReadingCelsius": 32,
            "Status": {"State": "Enabled", "Health": "OK"},
            "UpperThresholdCritical": 80,
            "PhysicalContext": "SystemBoard",
        },
    ],
    "Fans": [
        {
            "MemberId": "0",
            "Name": "FAN1",
            "Reading": 3500,
            "Status": {"State": "Enabled", "Health": "OK"},
            "LowerThresholdCritical": 500,
        },
        {
            "MemberId": "1",
            "Name": "FAN2",
            "Reading": 3600,
            "Status": {"State": "Enabled", "Health": "OK"},
            "LowerThresholdCritical": 500,
        },
    ],
}

POWER_RESPONSE: dict[str, Any] = {
    "Id": "Power",
    "Name": "Power",
    "PowerControl": [
        {
            "MemberId": "0",
            "Name": "Server Power Control",
            "PowerConsumedWatts": 150,
            "PowerCapacityWatts": 400,
            "Status": {"State": "Enabled", "Health": "OK"},
            "PowerMetrics": {
                "MinConsumedWatts": 120,
                "MaxConsumedWatts": 200,
                "AverageConsumedWatts": 155,
            },
        },
    ],
    "Voltages": [
        {
            "MemberId": "0",
            "Name": "12V",
            "ReadingVolts": 12.1,
            "Status": {"State": "Enabled", "Health": "OK"},
            "UpperThresholdCritical": 13.2,
            "LowerThresholdCritical": 10.8,
        },
        {
            "MemberId": "1",
            "Name": "5V",
            "ReadingVolts": 5.0,
            "Status": {"State": "Enabled", "Health": "OK"},
        },
    ],
    "PowerSupplies": [
        {
            "MemberId": "0",
            "Name": "PSU1",
            "Status": {"State": "Enabled", "Health": "OK"},
            "PowerSupplyType": "AC",
            "PowerCapacityWatts": 400,
        },
    ],
    "Oem": {
        "Supermicro": {
            "Battery": {
                "Name": "VBAT",
                "Status": {"State": "Enabled", "Health": "OK"},
            },
        },
    },
}

MANAGER_RESPONSE: dict[str, Any] = {
    "Id": "1",
    "Name": "Manager",
    "ManagerType": "BMC",
    "UUID": "87654321-4321-4321-4321-210987654321",
    "FirmwareVersion": "1.0.0",
    "Model": "ASPEED",
    "DateTime": "2024-01-15T10:30:00+00:00",
    "DateTimeLocalOffset": "+00:00",
    "LastResetTime": "2024-01-10T08:00:00+00:00",
    "PowerState": "On",
    "Status": {
        "State": "Enabled",
        "Health": "OK",
    },
}

NETWORK_PROTOCOL_RESPONSE: dict[str, Any] = {
    "Id": "NetworkProtocol",
    "Name": "Manager Network Protocol",
    "HostName": "bmc",
    "FQDN": "bmc.local",
    "HTTP": {"ProtocolEnabled": False, "Port": 80},
    "HTTPS": {"ProtocolEnabled": True, "Port": 443},
    "SSH": {"ProtocolEnabled": True, "Port": 22},
    "IPMI": {"ProtocolEnabled": True, "Port": 623},
    "SNMP": {"ProtocolEnabled": False, "Port": 161},
    "KVMIP": {"ProtocolEnabled": True, "Port": 5900},
    "VirtualMedia": {"ProtocolEnabled": True, "Port": 623},
}

FAN_MODE_RESPONSE: dict[str, Any] = {
    "Mode": "Optimal",
    "Mode@Redfish.AllowableValues": ["Standard", "FullSpeed", "Optimal", "HeavyIO"],
}

NTP_RESPONSE: dict[str, Any] = {
    "NTPEnable": True,
    "PrimaryNTPServer": "pool.ntp.org",
    "SecondaryNTPServer": "",
}

LLDP_RESPONSE: dict[str, Any] = {
    "LLDPEnabled": True,
}

SNOOPING_RESPONSE: dict[str, Any] = {
    "PostCode": "0x00",
}

LICENSE_RESPONSE: dict[str, Any] = {
    "Licenses": [
        {
            "LicenseID": "SFT-OOB-LIC",
            "LicenseType": "OOB License",
            "LicenseStatus": "Active",
        },
    ],
}

SERVICE_ROOT_RESPONSE: dict[str, Any] = {
    "RedfishVersion": "1.8.0",
    "UUID": "12345678-1234-1234-1234-123456789012",
    "Product": "Supermicro Redfish Service",
    "Vendor": "Supermicro",
    "Name": "Root Service",
}
