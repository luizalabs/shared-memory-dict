# Gunicorn + AioHTTP + AioCache + SharedMemoryDict

## Requirements:
- SharedMemoryDict + AioCache (`pip install shared-memory-cache[aiocache]`)
- AioHTTP
- Gunicorn

## To Run:
```
$ gunicorn main:app --config gunicorn_config.py -w 3 --worker-class aiohttp.GunicornWebWorker 
```

## Write on cache
```
$ curl -d "key=foo&value=bar" localhost:8000/
```

## Read from cache
```
$ curl localhost:8000/?key=foo
```
