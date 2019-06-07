broker_url='redis://redis:6379/2'
result_backend='redis://redis:6379/3'
accept_content = ['application/json']
task_serializer = 'json'
result_serializer = 'json'
enable_utc = True
timezone = 'Europe/London'