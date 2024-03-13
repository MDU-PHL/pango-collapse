# Use an official Python runtime as a parent image with a specific version for consistency
FROM python:3.10.5-slim

LABEL software="pango-collapse"
LABEL software.version="${VER}"
LABEL description="CLI to collapse Pango lineages up to user defined parent lineages for reporting"
LABEL website="https://github.com/MDU-PHL/pango-collapse"
LABEL license="https://github.com/MDU-PHL/pango-collapse?tab=GPL-3.0-1-ov-file#readme"
LABEL maintainer="Wytamma Wirth"
LABEL maintainer.email="wytamma.wirth@unimelb.edu.au"

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app_user

# Set a working directory
WORKDIR /home/app_user

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Switch to the app_user
USER app_user

# Copy application's code
COPY . .

# Install project dependencies
RUN poetry install --no-interaction --no-ansi --no-dev

# Run the application
ENTRYPOINT ["poetry", "run"]
CMD ["pango-collapse", "--help"]