from threading import Timer
from time import time

CACHE_DICT = {}
EXPIRE_TIMES = {}
DEFAULT_EXPIRE_TIME = 60 * 2


def memoize_cache(cache_name="", cache_key_index=1, ttl=DEFAULT_EXPIRE_TIME):
    def memoize(func):
        memo = {}
        expire = {}

        def wrapper(*args):
            if cache_key_index is not None:
                if cache_name in CACHE_DICT and args[cache_key_index] in CACHE_DICT[cache_name] \
                        and not is_expire_time(cache_name, args[cache_key_index]):
                    return CACHE_DICT[cache_name][args[cache_key_index]]
                else:
                    rv = func(*args)
                    memo[args[cache_key_index]] = rv
                    CACHE_DICT[cache_name] = memo

                    expire[args[cache_key_index]] = time() + ttl
                    EXPIRE_TIMES[cache_name] = expire
                    return rv
            else:
                if cache_name in CACHE_DICT and not is_expire_time(cache_name):
                    return CACHE_DICT[cache_name]
                else:
                    rv = func(*args)
                    CACHE_DICT[cache_name] = rv

                    EXPIRE_TIMES[cache_name] = time() + ttl
                    return rv

        return wrapper

    return memoize


def is_expire_time(cache_name, cache_key=None):
    if cache_key is None:
        if cache_name in EXPIRE_TIMES:
            expire_time = EXPIRE_TIMES[cache_name]
            if expire_time < time():
                return True
    else:
        if cache_name in EXPIRE_TIMES and cache_key in EXPIRE_TIMES[cache_name]:
            expire_time = EXPIRE_TIMES[cache_name][cache_key]
            if expire_time < time():
                return True

    return False


def clean_expired_data(inc):
    for key in list(EXPIRE_TIMES.keys()):
        value = EXPIRE_TIMES[key]
        if type(value) == float:
            if value < time():
                # print("clean_expired_data" + key)
                EXPIRE_TIMES.pop(key, None)
                CACHE_DICT.pop(key, None)
            else:
                # print("not clean_expired_data" + key)
                pass
        elif type(value) == dict:
            data = EXPIRE_TIMES[key]
            for param_key in list(data.keys()):
                param_value = data[param_key]
                if param_value < time():
                    # print("clean_param_expired_data" + str(param_key))
                    data.pop(param_key, None)
                    CACHE_DICT[key].pop(param_key, None)
                    # print(data)
                    # print(CACHE_DICT)
                else:
                    # print("not clean_param_expired_data" + str(param_key))
                    pass
            if not data:
                # print("clean_all_data_by_" + key)
                EXPIRE_TIMES.pop(key, None)
                CACHE_DICT.pop(key, None)
        else:
            pass
    t = Timer(inc, clean_expired_data, (inc,))
    t.start()


clean_expired_data(20)
