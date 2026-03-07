"""
Cacao v2 Server - Reactive Python framework with session-scoped state.

Core exports:
    - App: Main application class with routing and event handling
    - Signal: Reactive state primitive with session scoping
    - Computed: Derived state from other signals
    - Session: Per-client session object
    - Effect: Side effects on signal changes
    - Batch: Batch multiple signal updates
    - Persist: Persist signals to storage
    - Middleware: Event middleware system

Fluent UI (Streamlit-like API):
    - ui: Layout and component builders
    - chart: Chart components
    - data: Data loading and manipulation
"""

# Fluent UI imports
from . import agent, chart, data, llm, observability, tukuy_skills, ui
from .app import App
from .batch import Batch, batch, batch_updates
from .effects import Effect, Watch, effect
from .events import Event, EventRegistry
from .middleware import (
    EventContext,
    MiddlewareChain,
    auth_middleware,
    logging_middleware,
    rate_limit_middleware,
    timeout_middleware,
    transform_middleware,
    validation_middleware,
)
from .observability import (
    PrometheusMetrics,
    SignalRateMonitor,
    SignalRateStats,
    StructuredLogFormatter,
    Tracer,
    enable_metrics,
    enable_signal_monitoring,
    enable_structured_logging,
    enable_tracing,
    get_correlation_id,
    get_metrics,
    get_signal_monitor,
    get_tracer,
    set_correlation_id,
)
from .persist import FileStorage, MemoryStorage, Persist, PersistManager
from .security import (
    RBAC,
    AuditEntry,
    AuditLogger,
    CSRFProtection,
    OAuth2Config,
    OAuth2Provider,
    Role,
    Sanitizer,
    audit_middleware,
    csrf_middleware,
    enable_csrf,
    get_audit_logger,
    get_rbac,
    rbac_middleware,
    register_oauth2,
    require_role,
    sanitization_middleware,
)
from .session import Session, SessionManager
from .session_persist import SessionStore, enable_session_persistence, get_session_store
from .signal import Computed, Signal
from .tasks import BackgroundTaskQueue, TaskInfo, TaskStatus

__all__ = [
    # Core
    "App",
    "Signal",
    "Computed",
    "Session",
    "SessionManager",
    "Event",
    "EventRegistry",
    # Effects
    "Effect",
    "Watch",
    "effect",
    # Batch
    "Batch",
    "batch",
    "batch_updates",
    # Persist
    "Persist",
    "PersistManager",
    "MemoryStorage",
    "FileStorage",
    # Middleware
    "MiddlewareChain",
    "EventContext",
    "logging_middleware",
    "rate_limit_middleware",
    "validation_middleware",
    "auth_middleware",
    "transform_middleware",
    "timeout_middleware",
    # Security
    "CSRFProtection",
    "enable_csrf",
    "csrf_middleware",
    "Sanitizer",
    "sanitization_middleware",
    "OAuth2Config",
    "OAuth2Provider",
    "register_oauth2",
    "Role",
    "RBAC",
    "get_rbac",
    "rbac_middleware",
    "require_role",
    "AuditLogger",
    "AuditEntry",
    "get_audit_logger",
    "audit_middleware",
    # Session Persistence
    "SessionStore",
    "enable_session_persistence",
    "get_session_store",
    # Background Tasks
    "BackgroundTaskQueue",
    "TaskInfo",
    "TaskStatus",
    # Observability
    "observability",
    "enable_structured_logging",
    "StructuredLogFormatter",
    "get_correlation_id",
    "set_correlation_id",
    "PrometheusMetrics",
    "get_metrics",
    "enable_metrics",
    "Tracer",
    "get_tracer",
    "enable_tracing",
    "SignalRateMonitor",
    "SignalRateStats",
    "get_signal_monitor",
    "enable_signal_monitoring",
    # Fluent UI
    "ui",
    "chart",
    "data",
    "llm",
    "tukuy_skills",
    "agent",
]

try:
    from importlib.metadata import version as _get_version

    __version__: str = _get_version("cacao")
except Exception:
    from pathlib import Path as _Path

    _vf = _Path(__file__).resolve().parent.parent / "VERSION"
    __version__ = _vf.read_text().strip() if _vf.exists() else "0.0.0"
