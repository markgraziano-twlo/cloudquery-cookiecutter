# Start from a base image
FROM registry.twilio.com/library/python/3.11-slim:3.11

# (Optional) Set a working directory
WORKDIR /app

# Env variables
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false

# Copy requirements.txt and install the Python dependencies
COPY requirements_poetry.txt poetry.lock pyproject.toml ./
RUN pip3 install  -i https://pypi.dev.twilio.com/simple/ --no-cache-dir -r requirements_poetry.txt \
    && poetry install

# Copy the rest of the code
COPY plugin plugin
COPY main.py .

# (Optional) Expose any ports your app uses
EXPOSE 7777

ENTRYPOINT ["poetry", "run", "main"]

# Specify the command to run when the container starts
CMD ["serve", "--address", "[::]:7777", "--log-format", "json", "--log-level", "info"]
