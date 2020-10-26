Changelog
=========

0.3.1 (2020-10-26)
------------------
- Prevent `KeyError` and `IndexError` on checking expire of Django cache adapter

0.3.0 (2020-10-21)
------------------
- Remove uwsgi lock and use `multiprocessing.Lock` instead

0.2.0 (2020-10-19)
------------------
- Using lock on method `SharedMemoryDict.clear()`

0.1.1 (2020-08-12)
------------------
- Fix typo on hooks
- Remove name-prefix of caches (django and aiocache)

0.1.0 (2020-08-05)
------------------
- First Release :tada:
