#!/bin/bash
set -e

echo "Deploying Airflow DAGs..."

AIRFLOW_HOST="${AIRFLOW_HOST:-http://localhost:8080}"
AIRFLOW_USER="${AIRFLOW_USER:-admin}"
AIRFLOW_PASS="${AIRFLOW_PASS:-admin}"

for dag_file in dags/*.py; do
  echo "Validating $dag_file..."
  python -c "import ast; ast.parse(open('$dag_file').read())"
  echo "  Syntax OK"
done

echo "Uploading DAGs to Airflow server..."
scp -o StrictHostKeyChecking=no dags/*.py ${AIRFLOW_USER}@${AIRFLOW_HOST}:/opt/airflow/dags/

echo "Triggering DAG sync..."
curl -X POST "${AIRFLOW_HOST}/api/v1/dags?limit=100" \
  -u "${AIRFLOW_USER}:${AIRFLOW_PASS}" \
  -H "Content-Type: application/json"

echo "Deployment complete"
