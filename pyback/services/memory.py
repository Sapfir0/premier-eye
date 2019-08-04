import linecache
import os
import tracemalloc
from colorama import Fore


def getUsedRAM(snapshot):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    bytes = sum(stat.size for stat in snapshot.statistics('lineno'))
    kbytes = bytes / 1024
    mbytes = kbytes / 1024
    gbytes = mbytes / 1024
    if mbytes < 300:
        print(Fore.BLUE + "Total allocated size: %.1f MiB" % mbytes)
    elif mbytes >= 300:
        print(Fore.BLUE + "Total allocated size: %.3f GiB" % gbytes)
    else:
        print(Fore.BLUE + "Total allocated size: %.1f KiB" % kbytes)



def display_top(snapshot, key_type='lineno', limit=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    #print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        #print("#%s: %s:%s: %.1f KiB" % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        # if line:
        #     print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        #print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print(Fore.BLUE + "Total allocated size: %.1f KiB" % (total / 1024))
