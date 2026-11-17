FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY flavour_graph ./flavour_graph
RUN pip install --no-cache-dir -e .
ENV DATA_DIR=/data
CMD ["uvicorn", "flavour_graph.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
