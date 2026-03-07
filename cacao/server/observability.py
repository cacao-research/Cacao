"""
Observability module for Cacao.

Provides:
    - Structured logging with correlation IDs
    - Prometheus metrics export
    - OpenTelemetry tracing
    - Signal update rate monitoring
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from collections import defaultdict, deque
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any

from .log import get_logger

logger = get_logger("cacao.observability")

# =============================================================================
# Correlation IDs
# =============================================================================

# Context variable holding the current correlation ID for the request/session
_correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")


def get_correlation_id() -> str:
    """Get the current correlation ID."""
    return _correlation_id.get()


def set_correlation_id(cid: str | None = None) -> str:
    """Set the correlation ID for the current context.

    Args:
        cid: Explicit correlation ID. Auto-generated if not provided.

    Returns:
        The correlation ID that was set.
    """
    if not cid:
        cid = uuid.uuid4().hex[:16]
    _correlation_id.set(cid)
    return cid


class StructuredLogFormatter(logging.Formatter):
    """JSON structured log formatter with correlation ID support.

    Emits one JSON object per line with fields:
        timestamp, level, logger, message, correlation_id, label, and any extras.
    """

    def format(self, record: logging.LogRecord) -> str:
        entry: dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S.")
            + f"{int(record.msecs):03d}Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        cid = _correlation_id.get()
        if cid:
            entry["correlation_id"] = cid

        label = getattr(record, "label", None)
        if label:
            entry["label"] = label

        session_id = getattr(record, "session_id", None)
        if session_id:
            entry["session_id"] = session_id

        if record.exc_info and record.exc_info[0] is not None:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
            if record.exc_text:
                entry["exception"] = record.exc_text

        return json.dumps(entry, default=str)


def enable_structured_logging(*, level: str = "INFO") -> None:
    """Replace the default Cacao log handler with a JSON structured formatter.

    Args:
        level: Minimum log level.
    """
    root = logging.getLogger("cacao")
    root.handlers.clear()

    handler = logging.StreamHandler()
    handler.setFormatter(StructuredLogFormatter())
    root.addHandler(handler)
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    logger.info("Structured logging enabled", extra={"label": "observability"})


# =============================================================================
# Prometheus Metrics
# =============================================================================


class _Counter:
    """A simple counter metric."""

    __slots__ = ("_name", "_help", "_values")

    def __init__(self, name: str, help_text: str) -> None:
        self._name = name
        self._help = help_text
        self._values: dict[tuple[tuple[str, str], ...], float] = defaultdict(float)

    def inc(self, value: float = 1.0, **labels: str) -> None:
        key = tuple(sorted(labels.items()))
        self._values[key] += value

    def collect(self) -> str:
        lines = [f"# HELP {self._name} {self._help}", f"# TYPE {self._name} counter"]
        for label_pairs, val in sorted(self._values.items()):
            label_str = self._format_labels(label_pairs)
            lines.append(f"{self._name}{label_str} {val}")
        if not self._values:
            lines.append(f"{self._name} 0")
        return "\n".join(lines)

    @staticmethod
    def _format_labels(pairs: tuple[tuple[str, str], ...]) -> str:
        if not pairs:
            return ""
        inner = ",".join(f'{k}="{v}"' for k, v in pairs)
        return "{" + inner + "}"


class _Gauge:
    """A simple gauge metric."""

    __slots__ = ("_name", "_help", "_values")

    def __init__(self, name: str, help_text: str) -> None:
        self._name = name
        self._help = help_text
        self._values: dict[tuple[tuple[str, str], ...], float] = defaultdict(float)

    def set(self, value: float, **labels: str) -> None:
        key = tuple(sorted(labels.items()))
        self._values[key] = value

    def inc(self, value: float = 1.0, **labels: str) -> None:
        key = tuple(sorted(labels.items()))
        self._values[key] += value

    def dec(self, value: float = 1.0, **labels: str) -> None:
        key = tuple(sorted(labels.items()))
        self._values[key] -= value

    def collect(self) -> str:
        lines = [f"# HELP {self._name} {self._help}", f"# TYPE {self._name} gauge"]
        for label_pairs, val in sorted(self._values.items()):
            label_str = _Counter._format_labels(label_pairs)
            lines.append(f"{self._name}{label_str} {val}")
        if not self._values:
            lines.append(f"{self._name} 0")
        return "\n".join(lines)


class _Histogram:
    """A simple histogram metric with predefined buckets."""

    __slots__ = ("_name", "_help", "_buckets", "_observations")

    DEFAULT_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)

    def __init__(
        self,
        name: str,
        help_text: str,
        buckets: tuple[float, ...] | None = None,
    ) -> None:
        self._name = name
        self._help = help_text
        self._buckets = buckets or self.DEFAULT_BUCKETS
        self._observations: list[float] = []

    def observe(self, value: float) -> None:
        self._observations.append(value)

    def collect(self) -> str:
        lines = [f"# HELP {self._name} {self._help}", f"# TYPE {self._name} histogram"]
        total = len(self._observations)
        sum_val = sum(self._observations)

        for bound in self._buckets:
            count = sum(1 for v in self._observations if v <= bound)
            lines.append(f'{self._name}_bucket{{le="{bound}"}} {count}')
        lines.append(f'{self._name}_bucket{{le="+Inf"}} {total}')
        lines.append(f"{self._name}_sum {sum_val}")
        lines.append(f"{self._name}_count {total}")
        return "\n".join(lines)


class PrometheusMetrics:
    """
    Built-in Prometheus metrics for Cacao.

    Tracks WebSocket connections, events, signal updates, errors,
    and request latencies. Exposes a ``/metrics`` endpoint in
    Prometheus text format.
    """

    def __init__(self) -> None:
        # Counters
        self.ws_connections_total = _Counter(
            "cacao_ws_connections_total",
            "Total WebSocket connections since server start",
        )
        self.ws_disconnections_total = _Counter(
            "cacao_ws_disconnections_total",
            "Total WebSocket disconnections since server start",
        )
        self.events_total = _Counter(
            "cacao_events_total",
            "Total events processed",
        )
        self.signal_updates_total = _Counter(
            "cacao_signal_updates_total",
            "Total signal value updates",
        )
        self.errors_total = _Counter(
            "cacao_errors_total",
            "Total errors encountered",
        )

        # Gauges
        self.active_sessions = _Gauge(
            "cacao_active_sessions",
            "Currently active WebSocket sessions",
        )

        # Histograms
        self.event_duration_seconds = _Histogram(
            "cacao_event_duration_seconds",
            "Event handler execution duration in seconds",
        )

    def collect(self) -> str:
        """Collect all metrics in Prometheus text exposition format."""
        parts = [
            self.ws_connections_total.collect(),
            self.ws_disconnections_total.collect(),
            self.events_total.collect(),
            self.signal_updates_total.collect(),
            self.errors_total.collect(),
            self.active_sessions.collect(),
            self.event_duration_seconds.collect(),
        ]
        return "\n\n".join(parts) + "\n"


# Global metrics instance
_metrics: PrometheusMetrics | None = None


def get_metrics() -> PrometheusMetrics:
    """Get the global Prometheus metrics instance, creating it if needed."""
    global _metrics
    if _metrics is None:
        _metrics = PrometheusMetrics()
    return _metrics


def enable_metrics() -> PrometheusMetrics:
    """Enable Prometheus metrics collection.

    Returns:
        The PrometheusMetrics instance.
    """
    metrics = get_metrics()
    logger.info("Prometheus metrics enabled", extra={"label": "observability"})
    return metrics


# =============================================================================
# OpenTelemetry Tracing
# =============================================================================


@dataclass
class Span:
    """A lightweight trace span.

    When OpenTelemetry is installed, this wraps the real OTel span.
    Otherwise it acts as a no-op fallback so tracing calls never error.
    """

    name: str
    trace_id: str = ""
    span_id: str = ""
    parent_span_id: str = ""
    start_time: float = field(default_factory=time.monotonic)
    end_time: float = 0.0
    attributes: dict[str, Any] = field(default_factory=dict)
    status: str = "OK"
    _otel_span: Any = None  # real OTel span if available

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value
        if self._otel_span:
            self._otel_span.set_attribute(key, value)

    def set_status(self, status: str, description: str = "") -> None:
        self.status = status
        if self._otel_span:
            try:
                from opentelemetry.trace import StatusCode  # type: ignore[import-not-found]

                code = StatusCode.ERROR if status == "ERROR" else StatusCode.OK
                self._otel_span.set_status(code, description)
            except ImportError:
                pass

    def end(self) -> None:
        self.end_time = time.monotonic()
        if self._otel_span:
            self._otel_span.end()

    @property
    def duration_ms(self) -> float:
        end = self.end_time or time.monotonic()
        return (end - self.start_time) * 1000


class Tracer:
    """
    Tracing abstraction for Cacao.

    If ``opentelemetry-api`` and ``opentelemetry-sdk`` are installed,
    wraps the real OpenTelemetry tracer. Otherwise, provides a lightweight
    in-process tracer that still produces useful span data (logged and
    queryable via ``get_recent_spans``).
    """

    def __init__(self, service_name: str = "cacao") -> None:
        self._service_name = service_name
        self._otel_tracer: Any = None
        self._recent_spans: deque[Span] = deque(maxlen=500)

        # Try to initialize real OpenTelemetry
        try:
            from opentelemetry import trace  # type: ignore[import-not-found]
            from opentelemetry.sdk.resources import Resource  # type: ignore[import-not-found]
            from opentelemetry.sdk.trace import TracerProvider  # type: ignore[import-not-found]

            resource = Resource.create({"service.name": service_name})
            provider = TracerProvider(resource=resource)
            trace.set_tracer_provider(provider)
            self._otel_tracer = trace.get_tracer(service_name)
            logger.info(
                "OpenTelemetry tracing initialized (service=%s)",
                service_name,
                extra={"label": "observability"},
            )
        except ImportError:
            logger.info(
                "OpenTelemetry not installed; using built-in span tracking",
                extra={"label": "observability"},
            )

    def start_span(self, name: str, **attributes: Any) -> Span:
        """Start a new trace span.

        Args:
            name: Span name (e.g. "ws.event", "signal.update").
            **attributes: Initial span attributes.

        Returns:
            A Span object. Call ``span.end()`` when done.
        """
        otel_span = None
        trace_id = uuid.uuid4().hex[:32]
        span_id = uuid.uuid4().hex[:16]

        if self._otel_tracer:
            otel_span = self._otel_tracer.start_span(name, attributes=attributes)
            # Extract real IDs from OTel context
            ctx = otel_span.get_span_context()
            if ctx:
                trace_id = format(ctx.trace_id, "032x")
                span_id = format(ctx.span_id, "016x")

        span = Span(
            name=name,
            trace_id=trace_id,
            span_id=span_id,
            attributes=dict(attributes),
            _otel_span=otel_span,
        )
        self._recent_spans.append(span)
        return span

    def get_recent_spans(self, limit: int = 50) -> list[Span]:
        """Get recently completed spans.

        Args:
            limit: Maximum number of spans to return.

        Returns:
            List of recent Span objects, most recent first.
        """
        spans = list(self._recent_spans)
        return list(reversed(spans[-limit:]))

    def add_exporter(self, exporter: Any) -> None:
        """Add an OpenTelemetry span exporter (e.g. OTLP, Jaeger, Zipkin).

        Args:
            exporter: An OTel SpanExporter instance.
        """
        if not self._otel_tracer:
            logger.warning(
                "Cannot add exporter: OpenTelemetry SDK not installed",
                extra={"label": "observability"},
            )
            return

        try:
            from opentelemetry import trace
            from opentelemetry.sdk.trace.export import (  # type: ignore[import-not-found]
                BatchSpanProcessor,
            )

            provider = trace.get_tracer_provider()
            if hasattr(provider, "add_span_processor"):
                provider.add_span_processor(BatchSpanProcessor(exporter))
                logger.info(
                    "Added span exporter: %s",
                    type(exporter).__name__,
                    extra={"label": "observability"},
                )
        except ImportError:
            pass


# Global tracer instance
_tracer: Tracer | None = None


def get_tracer() -> Tracer:
    """Get the global tracer instance, creating it if needed."""
    global _tracer
    if _tracer is None:
        _tracer = Tracer()
    return _tracer


def enable_tracing(service_name: str = "cacao") -> Tracer:
    """Enable distributed tracing.

    Args:
        service_name: Service name for trace identification.

    Returns:
        The Tracer instance.
    """
    global _tracer
    _tracer = Tracer(service_name=service_name)
    return _tracer


# =============================================================================
# Signal Update Rate Monitoring
# =============================================================================


@dataclass
class SignalRateStats:
    """Rate statistics for a single signal."""

    signal_name: str
    updates_total: int = 0
    updates_per_second: float = 0.0
    updates_last_minute: int = 0
    peak_rate_per_second: float = 0.0
    last_update_time: float = 0.0


class SignalRateMonitor:
    """
    Monitors signal update rates.

    Tracks per-signal update counts and computes rolling rates.
    Useful for detecting hot signals, runaway update loops, and
    performance bottlenecks.
    """

    def __init__(self, *, window_seconds: float = 60.0) -> None:
        """
        Args:
            window_seconds: Rolling window for rate calculations.
        """
        self._window = window_seconds
        # signal_name -> list of timestamps
        self._timestamps: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=10000))
        self._totals: dict[str, int] = defaultdict(int)
        self._peak_rates: dict[str, float] = defaultdict(float)

    def record_update(self, signal_name: str) -> None:
        """Record a signal update event.

        Args:
            signal_name: Name of the signal that was updated.
        """
        now = time.monotonic()
        self._timestamps[signal_name].append(now)
        self._totals[signal_name] += 1

        # Update peak rate (computed over a 1-second window)
        recent = self._timestamps[signal_name]
        one_sec_ago = now - 1.0
        count_last_sec = sum(1 for t in recent if t > one_sec_ago)
        rate = float(count_last_sec)
        if rate > self._peak_rates[signal_name]:
            self._peak_rates[signal_name] = rate

    def get_stats(self, signal_name: str) -> SignalRateStats:
        """Get rate stats for a specific signal.

        Args:
            signal_name: The signal to query.

        Returns:
            SignalRateStats for the signal.
        """
        now = time.monotonic()
        timestamps = self._timestamps.get(signal_name, deque())

        # Count updates in the window
        cutoff = now - self._window
        in_window = sum(1 for t in timestamps if t > cutoff)

        # Current rate (updates per second over the window)
        rate = in_window / self._window if self._window > 0 else 0.0

        return SignalRateStats(
            signal_name=signal_name,
            updates_total=self._totals.get(signal_name, 0),
            updates_per_second=round(rate, 2),
            updates_last_minute=in_window,
            peak_rate_per_second=self._peak_rates.get(signal_name, 0.0),
            last_update_time=timestamps[-1] if timestamps else 0.0,
        )

    def get_all_stats(self) -> list[SignalRateStats]:
        """Get rate stats for all monitored signals.

        Returns:
            List of SignalRateStats sorted by total updates (descending).
        """
        stats = [self.get_stats(name) for name in self._totals]
        stats.sort(key=lambda s: s.updates_total, reverse=True)
        return stats

    def get_hot_signals(self, threshold_per_second: float = 10.0) -> list[SignalRateStats]:
        """Get signals with update rates above a threshold.

        Args:
            threshold_per_second: Minimum updates/sec to be considered hot.

        Returns:
            List of SignalRateStats for hot signals.
        """
        return [s for s in self.get_all_stats() if s.updates_per_second >= threshold_per_second]

    def reset(self) -> None:
        """Reset all monitoring data."""
        self._timestamps.clear()
        self._totals.clear()
        self._peak_rates.clear()


# Global signal rate monitor
_signal_monitor: SignalRateMonitor | None = None


def get_signal_monitor() -> SignalRateMonitor:
    """Get the global signal rate monitor, creating it if needed."""
    global _signal_monitor
    if _signal_monitor is None:
        _signal_monitor = SignalRateMonitor()
    return _signal_monitor


def enable_signal_monitoring(*, window_seconds: float = 60.0) -> SignalRateMonitor:
    """Enable signal update rate monitoring.

    Args:
        window_seconds: Rolling window for rate calculations.

    Returns:
        The SignalRateMonitor instance.
    """
    global _signal_monitor
    _signal_monitor = SignalRateMonitor(window_seconds=window_seconds)
    logger.info("Signal rate monitoring enabled", extra={"label": "observability"})
    return _signal_monitor
