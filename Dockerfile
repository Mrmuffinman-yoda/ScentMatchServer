FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY requirements.txt .

RUN uv pip install --system --no-cache -r requirements.txt

# Now copy the rest of your application code.
COPY ./app /app

# Pre-compile Python bytecode using the system python.
RUN python -m compileall /app

# Expose the port your application will run on
EXPOSE 8001