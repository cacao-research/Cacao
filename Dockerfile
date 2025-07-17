# Multi-stage Docker build for testing Cacao framework package
FROM python:3.9-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 1: Build and test the package
FROM base AS builder

# Copy source code
COPY . .

# Install build dependencies
RUN pip install --no-cache-dir build setuptools wheel

# Build the package
RUN python -m build --wheel --sdist

# Stage 2: Clean test environment
FROM base AS test

# Copy built package from builder stage
COPY --from=builder /app/dist/*.whl /tmp/
COPY --from=builder /app/dist/*.tar.gz /tmp/

# Copy test scripts
COPY test/test_package.py /app/
COPY examples/ /app/examples/

# Install the package from wheel (select the latest one to avoid conflicts)
RUN pip install $(ls -t /tmp/*.whl | head -1)

# Set environment variables for testing
ENV PYTHONPATH=/app
ENV CACAO_TEST_MODE=true

# Default command runs the test suite
CMD ["python", "test_package.py"]

# Stage 3: Development test environment (with source)
FROM base AS dev-test

# Copy source code for development testing
COPY . .

# Install in development mode
RUN pip install -e .

# Install additional development dependencies
RUN pip install pytest pytest-asyncio

# Set environment variables
ENV PYTHONPATH=/app
ENV CACAO_TEST_MODE=true

# Default command for development testing
CMD ["python", "test_package.py"]

# Stage 4: Minimal production test
FROM python:3.9-slim AS minimal

# Install only runtime dependencies
RUN pip install --no-cache-dir websockets asyncio watchfiles colorama pywebview

# Copy and install built package
COPY --from=builder /app/dist/*.whl /tmp/
RUN pip install $(ls -t /tmp/*.whl | head -1)

# Copy test script
COPY test/test_package.py /app/
WORKDIR /app

# Test in minimal environment
CMD ["python", "test_package.py"]