export PYTHONPATH=/opt
alembic upgrade head
cd migrations || exit
rm Dockerfile
