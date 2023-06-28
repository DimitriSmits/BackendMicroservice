export APP_SECRET='secret'
export POSTGRES_USER='dockerpostgres'
export POSTGRES_PASSWORD='admin'
export POSTGRES_DB='dockerpostgres'
export POSTGRES_HOSTNAME='db'
# Wait for database to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOSTNAME -U $POSTGRES_USER -d $POSTGRES_DB -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 20
done
sleep 20
echo "Database ready"
# Start FastAPI
uvicorn main:app --host 0.0.0.0 --port 8002