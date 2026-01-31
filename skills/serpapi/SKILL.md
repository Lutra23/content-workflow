---
name: serpapi
description: Google Search results via SerpAPI. Real-time search data with rich snippets, knowledge graphs, and direct answers.
homepage: https://serpapi.com
metadata: {"clawdbot":{"emoji":"🔎","requires":{"bins":["curl","node"],"env":["SERPAPI_API_KEY"]},"primaryEnv":"SERPAPI_API_KEY"}}
---

# SerpAPI Search

Real-time Google search results via SerpAPI. Returns rich snippets, knowledge graphs, and direct answers.

## Setup

Configure API key:
```bash
clawdbot config set env.SERPAPI_API_KEY "your-api-key"
```

## Search

```bash
node {baseDir}/scripts/search.mjs "query"
node {baseDir}/scripts/search.mjs "query" -n 10
node {baseDir}/scripts/search.mjs "query" --engine google
node {baseDir}/scripts/search.mjs "query" --engine bing
```

## Options

- `-n <count>`: Number of results (default: 10)
- `--engine <engine>`: Search engine - `google` (default), `bing`, `duckduckgo`, `yahoo`
- `--location <location>`: Location filter (e.g., "United States", "Beijing, China")

## Examples

```bash
# Basic search
node scripts/search.mjs "AI news today"

# More results
node scripts/search.mjs "Claude 3 pricing" -n 5

# Specific engine
node scripts/search.mjs "best VS Code extensions" --engine bing
```

## Output Format

```json
{
  "search_metadata": {...},
  "search_parameters": {...},
  "organic_results": [
    {
      "title": "Result Title",
      "link": "https://...",
      "snippet": "Description...",
      "position": 1
    }
  ],
  "knowledge_graph": {...},
  "top_stories": [...]
}
```

## Notes

- Free tier: 100 searches/month
- Paid: $50/5000 searches
- Faster and more reliable than web scraping
- Supports multiple search engines

## When to Use

- Real-time search results
- Rich snippets and knowledge panels
- Multiple search engine support
- When Tavily results are insufficient
