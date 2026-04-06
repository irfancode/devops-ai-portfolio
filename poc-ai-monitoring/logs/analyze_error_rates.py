import re
from collections import Counter
from datetime import datetime

error_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (ERROR|CRITICAL) (.*)")
endpoint_pattern = re.compile(r"endpoint=(\S+)")

def analyze_errors(path):
    errors = Counter()
    endpoints = Counter()
    hourly_errors = Counter()
    
    with open(path) as f:
        for line in f:
            m = error_pattern.search(line)
            if m:
                timestamp, level, message = m.groups()
                errors[message.strip()] += 1
                
                ep = endpoint_pattern.search(message)
                if ep:
                    endpoints[ep.group(1)] += 1
                
                hour = timestamp[:13]
                hourly_errors[hour] += 1
    
    return errors, endpoints, hourly_errors

if __name__ == "__main__":
    errors, endpoints, hourly = analyze_errors("app.log")
    print("Top errors:", errors.most_common(10))
    print("Top error endpoints:", endpoints.most_common(10))
    print("Hourly error distribution:", sorted(hourly.items()))
