import re
import sys, os

if len(sys.argv) < 2:
    sys.exit("Usage: %s filename" % sys.argv[0])

filename = sys.argv[1]

if not os.path.exists(filename):
    sys.exit("Error: File %s not found" % sys.argv[1])

stat_regex = re.compile(r"([A-Za-z]+ [A-Z][A-Za-z]+) \bbatted\b[\s]([0-9]+ )\btimes with\b( [0-9] )\bhits and\b [0-9] \bruns\b")
with open(filename) as file_contents:
    raw_stats = {}

    for line in file_contents:
        stat_match = stat_regex.match(line)

        if stat_match is not None:
            name = stat_match.group(1)
            bats = int(stat_match.group(2))
            hits = int(stat_match.group(3))

            

            if name in raw_stats:
                raw_stats[name]['raw_bats'] += bats
                raw_stats[name]['raw_hits'] += hits
            else:
                raw_stats[name] = {
                    'raw_bats': bats,
                    'raw_hits': hits
                }

def find_average(num, den):
    avg = num / den
    avg = round(avg, 3)
    avg = f'{avg:.3f}'
    return avg

result = {}

for name in raw_stats:
    average = find_average(float(raw_stats[name]['raw_hits']), float(raw_stats[name]['raw_bats']))
    result[name] = average

liststats = sorted(result.items(), key = lambda kv:float(kv[1]), reverse = True)

for elem in liststats:
    print(elem[0], ": ", elem[1])