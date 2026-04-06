import re
from collections import Counter

failed_pattern = re.compile(r"Failed login.*user=(\S+).*ip=(\S+)")

def analyze_logs(path):
    users = Counter()
    ips = Counter()
    with open(path) as f:
        for line in f:
            m = failed_pattern.search(line)
            if m:
                users[m.group(1)] += 1
                ips[m.group(2)] += 1
    return users, ips

if __name__ == "__main__":
    users, ips = analyze_logs("auth.log")
    print("Top failed users:", users.most_common(10))
    print("Top failed IPs:", ips.most_common(10))
