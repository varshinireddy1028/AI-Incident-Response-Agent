# AI Incident Response Agent with Hindsight Memory

## Overview

AI Incident Response Agent is an intelligent incident analysis system that uses AI and Hindsight memory to help analyze recurring production incidents.

The system recalls similar incidents from the past, uses their root causes and resolutions to analyze the current incident, and stores the new resolution for future use.

## Problem

When production incidents occur repeatedly, engineers often need to search through previous incident records to understand what happened and how it was resolved.

This project provides an AI-powered incident response workflow that can remember previous incidents and use that knowledge when analyzing new incidents.

## Solution

The system follows this workflow:

1. User enters a production incident.
2. AI Incident Response Agent analyzes the incident.
3. Hindsight recalls similar past incidents.
4. The system identifies possible root causes based on previous incidents.
5. Previous resolutions are presented as useful troubleshooting context.
6. The user provides the actual root cause and resolution.
7. The new incident and its outcome are stored in Hindsight memory.
8. Future incidents can use this information.

## Key Features

- AI-assisted incident analysis
- Hindsight-based long-term memory
- Similar incident recall
- Root-cause analysis support
- Resolution storage
- Local LLM support using Ollama
- FastAPI backend
- Simple web-based frontend
- Docker-based Hindsight deployment

## Technology Stack

- Python
- FastAPI
- Hindsight
- Ollama
- Llama 3.2 1B
- HTML
- CSS
- JavaScript
- Docker

## Architecture

```text
User
  |
  v
Web Frontend
  |
  v
FastAPI Backend
  |
  +------> Local LLM (Ollama)
  |
  +------> Hindsight Memory
              |
              +--> Recall past incidents
              |
              +--> Store new resolutions