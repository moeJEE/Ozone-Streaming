# Data Streaming Pipeline Makefile

.PHONY: help install test clean build up down logs

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = :.*?##
