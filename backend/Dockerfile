# #################################################################### #
#                                                                      #
# base image                                                           #
#                                                                      #
# #################################################################### #

FROM python:3.13-slim-trixie AS base


# #################################################################### #
#                                                                      #
# builder image                                                        #
#                                                                      #
# #################################################################### #

FROM base AS builder

WORKDIR /app

RUN pip install uv \
    && apt-get update -qq \
    && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml ./pyproject.toml
RUN pip install uv && \
    uv venv && \
    uv pip install --upgrade pip && \
    uv pip install -r pyproject.toml


# #################################################################### #
#                                                                      #
# prod image                                                           #
#                                                                      #
# #################################################################### #

FROM base AS prod

ENV PYTHONPATH=/app

WORKDIR /app

RUN pip install uv \
    && apt-get update -qq \
    && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r appusergroup && \
    useradd -r -g appusergroup -s /bin/bash -d /home/appuser appuser && \
    mkdir -p /home/appuser && \
    chown -R appuser:appusergroup /home/appuser

RUN mkdir -p /app/logs && \
    chown -R appuser:appusergroup /app/logs

COPY --from=builder --chown=appuser:appusergroup /app/.venv ./.venv
COPY --chown=appuser:appusergroup ./src ./src

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD /bin/bash -c "source .venv/bin/activate && python -c \"import os; os.path.exists('/app/logs/healthcheck') or exit(1)\""

EXPOSE 8080

USER appuser

CMD ["/bin/bash", "-c", "source .venv/bin/activate && fastapi run src/api/closed/main.py --app app --host 0.0.0.0 --port 8080"]