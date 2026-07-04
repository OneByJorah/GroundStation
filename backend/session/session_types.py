"""
Lightweight typing models for session and runtime data.

These are intended for annotations and documentation only; they do not
introduce any runtime dependencies or validation. All shapes remain JSON-safe
in public views (e.g., runtime snapshots) and keep existing behavior.
"""

from typing import TypedDict


class SessionConfig(TypedDict, total=False):
    """Per-session SDR configuration payload stored in active_sdr_clients.

    Note: Keys reflect current usage in handlers; this model is permissive
    (total=False) to avoid breaking callers while documenting intent.
    """

    sdr_id: str
    center_freq: float
    sample_rate: float
    gain: float
    fft_size: int
    bias_t: bool
    tuner_agc: bool
    rtl_agc: bool
    fft_window: str
    fft_averaging: int
    antenna: str | None
    recording_path: str | None
    serial_number: str | None
    host: str | None
    port: int | None
    client_id: str
    soapy_agc: bool
    offset_freq: float


class SessionView(TypedDict, total=False):
    """Merged relationship/config view for a session."""

    session_id: str
    sdr_id: str | None
    rig_id: str | None
    vfo: int | None
    config: SessionConfig
    is_internal: bool  # True for internal observations, False for user sessions


class ConsumerMeta(TypedDict, total=False):
    """Metadata for a running consumer (thread) instance.

    Stored internally under ProcessManager.processes for demodulators/recorders/decoders
    as a dict with at least an "instance" and a "subscription_key". The public JSON views
    do not expose the instance; they typically expose the class name per VFO.
    """

    instance: object
    subscription_key: str
    class_name: str | None
    thread_name: str | None
    vfo_number: int | None


class SDRProcessStatus(TypedDict, total=False):
    """Basic status of an SDR worker process."""

    alive: bool
    pid: int | None
    name: str | None


class RuntimeSDRConsumers(TypedDict, total=False):
    """JSON-safe snapshot entry for one SDR in a runtime snapshot."""

    alive: bool
    clients: list[str]
    demodulators: dict[str, dict[int, str | None]]
    recorders: dict[str, str | None]
    decoders: dict[str, dict[int, str | None]]


class RuntimeSnapshot(TypedDict, total=False):
    """Top-level runtime snapshot structure."""

    sessions: dict[str, SessionView]
    sdrs: dict[str, RuntimeSDRConsumers]
