celery -A core worker --loglevel=info
bg_pid=$!
sleep 120
exit 0