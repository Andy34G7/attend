# PESU Attendance Tracker

> [polarhive.net/attend](https://polarhive.net/attend)

Fetches attendance details from PESUAcademy, provides real-time logs, and supports multiple SRN formats and mappings.

![Cron job status](https://api.cron-job.org/jobs/5967927/b0792bab02dda80d/status-7.svg)

## Getting Started

Download [uv](https://docs.astral.sh/uv/getting-started/installation)

```sh
uv run main.py
```

### API

```bash
curl -X POST https://attendanceisallyouneed.vercel.app/api/attendance \
  -H "Content-Type: application/json" \
  -d '{"username": "PES2UG24CS061", "password": "your_password"}'
```

### Model Context Protocol (MCP) Server

Connect your AI assistants (Claude Desktop, Cursor, Antigravity, LLM agents) to your Vercel deployment via MCP over HTTP:

- **Endpoint**: `https://<your-vercel-domain>/api/mcp` or `https://<your-vercel-domain>/mcp`

#### Available MCP Tools

1. **`get_attendance`**: Fetch complete attendance breakdown, percentages, and bunkable classes calculation for a student.
2. **`get_semesters`**: Discover enrolled semester batch IDs and titles.
3. **`calculate_bunkable_classes`**: Calculate skippable/needed classes for any attended/total class numbers.

#### Example MCP JSON-RPC Request

```bash
curl -X POST https://<your-vercel-domain>/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "get_attendance",
      "arguments": {
        "username": "PES2UG24CS061",
        "password": "your_password"
      }
    }
  }'
```

## Contributions

Feel free to open issues and PRs for improvements and feature requests.
