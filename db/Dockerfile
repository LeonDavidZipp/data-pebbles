FROM postgres@sha256:f30e3de0ac9cc938dac627ef2231099867c694b5f949fadb924c8c977428c399

COPY init.sql /docker-entrypoint-initdb.d/init.sql

CMD ["postgres", \
    "-c", "shared_preload_libraries=pg_stat_statements", \
    "-c", "pg_stat_statements.track=all", \
    "-c", "shared_buffers=256MB", \
    "-c", "work_mem=16MB", \
    "-c", "maintenance_work_mem=128MB", \
    "-c", "effective_cache_size=512MB", \
    "-c", "random_page_cost=1.1", \
    "-c", "log_min_duration_statement=1000"]
