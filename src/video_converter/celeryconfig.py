broker_url = 'redis://redis:6379/0'
result_backend = 'redis://redis:6379/2'
accept_content = ['application/json']
task_serializer = 'json'
result_serializer = 'json'
enable_utc = True
timezone = 'Europe/London'
broker_transport_options = {
    'priority_steps': [0, 1]
}
celery_acks_late = True
celeryd_prefetch_multiplier = 1