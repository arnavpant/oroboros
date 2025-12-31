#!/bin/bash
echo "🔌 Loading Ouroboros Environment..."
source config/gcp.env
source config/kafka.env
source config/datadog.env
export PYTHONPATH=$PYTHONPATH:.
echo "✅ Environment loaded."