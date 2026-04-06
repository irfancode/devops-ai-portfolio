# AI-Generated Monitoring & Log Analysis

> **AI-Assisted DevOps POC**: Demonstrates how AI accelerates monitoring setup, from PromQL queries to Grafana dashboards and log analysis scripts.

## Overview

This project shows how to go from zero to full observability in a day using AI to generate:
- **Prometheus recording rules and alerts** for latency, error rate, CPU saturation
- **Grafana dashboards** for API health and background job monitoring
- **Python log analysis scripts** for security and operational insights

## Quick Start

### Prometheus Setup
```bash
# Copy rules to your Prometheus config directory
cp prometheus/rules/*.yml /etc/prometheus/rules/
cp prometheus/alerts/*.yml /etc/prometheus/alerts/

# Reload Prometheus
curl -X POST http://localhost:9090/-/reload
```

### Grafana Dashboards
Import dashboards via Grafana UI:
1. Go to Dashboards > Import
2. Upload JSON from `grafana/dashboards/`
3. Select your Prometheus data source

### Log Analysis
```bash
cd logs
python analyze_failed_logins.py
python analyze_error_rates.py
```

## AI-Assisted Components

| Component | AI Role | Human Refinement |
|-----------|---------|------------------|
| PromQL queries | Generated initial queries | Optimized for cardinality, added recording rules |
| Alert thresholds | Suggested baseline values | Tuned based on SLO targets |
| Grafana panels | Created panel layouts | Added drill-down links, annotations |
| Log parsers | Generated regex patterns | Optimized for production log formats |

See [AI-usage.md](./AI-usage.md) for detailed breakdown.

## Alerting Strategy

### SLO-Based Alerts
- **Latency**: 95th percentile > 500ms for 5 minutes
- **Error Rate**: > 1% of requests over 5 minutes
- **Saturation**: CPU > 80% or Memory > 85% for 10 minutes

### Escalation Path
1. Warning → Slack notification
2. Critical → PagerDuty
3. Page → On-call engineer

## License

MIT
