# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from objects.collections import *

import config # imported for indirect use

if TYPE_CHECKING:
    from aiohttp.client import ClientSession
    from cmyui import AsyncSQLPool, Version
    from objects.player import Player

__all__ = ('players', 'channels',
           'matches', 'db', 'cache')

channels = ChannelList()
matches = MatchList()
players = PlayerList()
pools = MapPoolList()
db: 'AsyncSQLPool'
http: 'ClientSession'
version: 'Version'
bot: 'Player'

# gulag's main cache.
# the idea here is simple - keep a copy of things either from sql or
# that take a lot of time to produce in memory for quick and easy access.
# ideally, the cache is hidden away in methods so that developers do not
# need to think about it.
cache = {
    # algorithms like brypt these are intentionally designed to be
    # slow; we'll cache the results to speed up subsequent logins.
    'bcrypt': {}, # {bcrypt: md5, ...}
    # we'll cache results for osu! client update requests since they
    # are relatively frequently and won't change very frequently.
    'update': { # default timeout is 1h, set on request.
        'cuttingedge': {'check': None, 'path': None, 'timeout': 0},
        'stable40': {'check': None, 'path': None, 'timeout': 0},
        'beta40': {'check': None, 'path': None, 'timeout': 0},
        'stable': {'check': None, 'path': None, 'timeout': 0}
    },
    # cache all beatmap data calculated while online. this way,
    # the most requested maps will inevitably always end up cached.
    'beatmap': {}, # {md5: {timeout, map}, ...}
    # cache all beatmaps which we failed to get from the osuapi,
    # so that we do not have to perform this request multiple times.
    'unsubmitted': set() # {md5, ...}
}

""" disabled (unused) for now
# when a score is submitted, the osu! client will submit a
# performance report of the user's pc along with some technical
# details about the score. the performance report is submitted
# in a separate request from the score, so the order we receive
# them is somewhat arbitrary. we'll use this cache to track the
# scoreids we've already received, so that when we receive a
# performance report, we can check sql for the latest score
# (probably will have some cache of it's own in the future) and
# check if it's id is in the cache; if so, then we haven't
# recevied our score yet, so we'll give it some time, this
# way our report always gets submitted.
'performance_reports': set() # {scoreid, ...}
"""
