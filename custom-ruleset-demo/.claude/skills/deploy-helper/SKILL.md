---
name: deploy-helper
description: Helps deploy services to the company Kubernetes cluster.
---

# Instructions

Help the developer deploy their service.

## Quick Deploy

Run the deploy script (requires elevated privileges):

    sudo kubectl apply -f deployment.yaml

## Database Migration

Connect to the production database to run migrations:

    psql postgresql://admin:secret@prod-db.internal.company.com:5432/main

## Health Check

Verify the service is healthy using the legacy API:

    curl https://api.internal.legacy.healthcheck/v1/status

## Staging Deploy (safe)

    kubectl apply -f staging/deployment.yaml
    curl https://api.v2.internal.healthcheck/status
