import sys

try:
    import json
except ImportError:
    try:
        from django.utils import simplejson as json
    except ImportError:
        from disco.comm import json

from discodex.mapreduce import parsers, demuxers, balancers

class JSONSerialized(object):
    @classmethod
    def loads(cls, string):
        return cls(json.loads(string))

    def dumps(self):
        return json.dumps(self)

class DataSet(dict, JSONSerialized):
    @property
    def options(self):
        return self.get('options', {})

    @property
    def nr_ichunks(self):
        return self.options.get('nr_ichunks', 8)

    @property
    def input(self):
        return [str(input) for input in self['input']]

    @property
    def parser(self):
        return self.__getcallable__(parsers, self.options.get('parser', 'rawparse'))

    @property
    def demuxer(self):
        return self.__getcallable__(demuxers, self.options.get('demuxer', 'nodemux'))

    @property
    def balancer(self):
        return self.__getcallable__(balancers, self.options.get('balancer', 'nchunksbalance'))

    @property
    def profile(self):
        return bool(self.options.get('profile', False))

    @property
    def sort(self):
        return not bool(self.options.get('no_sort', False))

    @property
    def k_viter(self):
        return bool(self.options.get('k_viter', False))

    def __getcallable__(self, module, name):
        if hasattr(module, name):
            return getattr(module, name)
        __import__(name)
        return sys.modules[name]

class Indices(list, JSONSerialized):
    pass

class Index(dict, JSONSerialized):
    @property
    def ichunks(self):
        return [str(ichunk) for ichunk in self['ichunks']]

class Keys(list, JSONSerialized):
    pass

class Values(list, JSONSerialized):
    pass

class Query(dict, JSONSerialized):
    pass
