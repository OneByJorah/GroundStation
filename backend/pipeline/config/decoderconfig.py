# Copyright (c) 2025 Efstratios Goudelis
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


from dataclasses import dataclass
from typing import Any


@dataclass
class DecoderConfig:
    """
    Resolved decoder configuration with all parameters determined.

    This is the result of parameter resolution from multiple sources:
    - Satellite-specific configuration (gr-satellites database)
    - Transmitter metadata (SatNOGS DB)
    - Smart defaults based on modulation type
    - Manual overrides

    Used to:
    1. Pass pre-resolved parameters to decoders
    2. Compare configurations to detect parameter changes (for decoder restart logic)
    3. Provide single source of truth for decoder parameters
    """

    # Common parameters (all decoders)
    baudrate: int
    framing: str  # 'ax25', 'usp', 'geoscan', 'doka', etc.
    config_source: str  # 'satellite_config', 'smart_default', 'transmitter_metadata', 'manual'

    # FSK-specific parameters (GMSK, GFSK, AFSK)
    deviation: int | None = None  # Frequency deviation in Hz

    # AFSK-specific parameters
    af_carrier: int | None = None  # Audio frequency carrier in Hz (1700 for APRS)

    # BPSK-specific parameters
    differential: bool | None = None  # DBPSK mode

    # LoRa-specific parameters
    sf: int | None = None  # Spreading factor (7-12)
    bw: int | None = None  # Bandwidth (125000, 250000, 500000)
    cr: int | None = None  # Coding rate (1-4, corresponding to 4/5 through 4/8)
    sync_word: list | None = None  # Sync word ([0, 0] for auto-detect)
    preamble_len: int | None = None  # Preamble length (default: 8)
    fldro: bool | None = None  # Low Data Rate Optimization (default: False)

    # Weather satellite specific parameters (SatDump)
    pipeline: str | None = None  # SatDump pipeline name (e.g., 'noaa_apt', 'meteor_m2-x_lrpt')
    target_sample_rate: int | None = (
        None  # Target sample rate for pipeline (e.g., 48000 for APT)
    )

    # Optional metadata
    packet_size: int | None = None  # Expected packet size in bytes

    # Framing-specific parameters (protocol options passed to deframers)
    framing_params: dict[str, Any] | None = None

    # Satellite metadata (for logging, file naming, telemetry parsing)
    satellite: dict | None = None

    # Transmitter metadata (for logging, file naming, reference)
    transmitter: dict | None = None

    def __eq__(self, other):
        """
        Compare configurations to detect parameter changes.

        Used by DecoderManager to determine if decoder needs to be restarted
        when configuration changes (e.g., different satellite selected).

        Returns:
            bool: True if configurations are identical
        """
        if not isinstance(other, DecoderConfig):
            return False

        return (
            self.baudrate == other.baudrate
            and self.framing == other.framing
            and self.deviation == other.deviation
            and self.af_carrier == other.af_carrier
            and self.differential == other.differential
            and self.sf == other.sf
            and self.bw == other.bw
            and self.cr == other.cr
            and self.sync_word == other.sync_word
            and self.preamble_len == other.preamble_len
            and self.fldro == other.fldro
            and self.pipeline == other.pipeline
            and self.target_sample_rate == other.target_sample_rate
            and (self.framing_params or {}) == (other.framing_params or {})
        )

    def __hash__(self):
        """Allow DecoderConfig to be used as dict key"""
        # Convert dicts/lists to hashable representations
        framing_params_tuple = (
            tuple(sorted((self.framing_params or {}).items()))
            if (self.framing_params is not None)
            else None
        )

        return hash(
            (
                self.baudrate,
                self.framing,
                self.deviation,
                self.af_carrier,
                self.differential,
                self.sf,
                self.bw,
                self.cr,
                tuple(self.sync_word) if self.sync_word else None,
                self.preamble_len,
                self.fldro,
                self.pipeline,
                self.target_sample_rate,
                framing_params_tuple,
            ),
        )

    def to_dict(self):
        """Convert to dictionary for logging/serialization"""
        return {
            "baudrate": self.baudrate,
            "framing": self.framing,
            "config_source": self.config_source,
            "deviation": self.deviation,
            "af_carrier": self.af_carrier,
            "differential": self.differential,
            "sf": self.sf,
            "bw": self.bw,
            "cr": self.cr,
            "sync_word": self.sync_word,
            "preamble_len": self.preamble_len,
            "fldro": self.fldro,
            "pipeline": self.pipeline,
            "target_sample_rate": self.target_sample_rate,
            "packet_size": self.packet_size,
            "framing_params": self.framing_params,
            "satellite": self.satellite,
            "transmitter": self.transmitter,
        }
