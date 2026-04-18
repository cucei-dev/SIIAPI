FROM python:3.11-alpine
RUN pip install uv
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --chown=appuser:appgroup pyproject.toml uv.lock ./
RUN uv sync --no-dev
ENV PATH="/app/.venv/bin:$PATH"
COPY --chown=appuser:appgroup . .
EXPOSE 8000
USER appuser
CMD ["fastapi", "run"]
