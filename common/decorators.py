# -*- coding:utf-8 -*-


def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        key = (cls, args)
        if key not in instances:
            instances[key] = cls(*args, **kwargs)
        return instances[key]
    return get_instance