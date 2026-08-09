FROM python:3.14-slim AS base



# Prevent Python from writing pyc files and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Ensure virtual environment binaries (uvicorn, streamlit, etc.) are in PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

WORKDIR /app

# Copy the uv binary directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy uv package definition and lock files for layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies into the virtual environment using uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

COPY app/ ./app/


# -----------------------------
# Backend
# -----------------------------
FROM base AS backend
EXPOSE 8000
CMD ["uvicorn", "app.presentation.api.app:app", "--host", "0.0.0.0", "--port", "8000"]



# -----------------------------
# Streamlit UI
# -----------------------------
FROM base AS ui
EXPOSE 8501
CMD ["streamlit", "run", "app/ui/streamlit/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]