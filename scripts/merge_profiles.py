#!/usr/bin/env python3

import pstats
from os import listdir

profiling_dir = "profiling/"

profiles = listdir(profiling_dir)

stats = None

for p in profiles:
    if not stats:
        stats = pstats.Stats(profiling_dir + p)
    else:
        stats.add(profiling_dir + p)

if stats:
    stats.dump_stats("combined_profile.prof")
