#!/bin/bash
docker build --tag=teller:sha-$(git rev-parse --short=7 HEAD) .
