#!/usr/bin/env node

function usage() {
  console.error(`Usage: search.mjs "query" [-n 10] [--engine google|bing|duckduckgo|yahoo] [--location "location"]`);
  console.error(`Example: search.mjs "AI news" -n 5 --engine google --location "United States"`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const query = args[0];
let numResults = 10;
let engine = "google";
let location = null;

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === "-n") {
    numResults = Number.parseInt(args[i + 1] ?? "10", 10);
    i++;
    continue;
  }
  if (a === "--engine") {
    engine = args[i + 1] ?? "google";
    i++;
    continue;
  }
  if (a === "--location") {
    location = args[i + 1] ?? null;
    i++;
    continue;
  }
}

const apiKey = (process.env.SERPAPI_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing SERPAPI_API_KEY. Run: clawdbot config set env.SERPAPI_API_KEY \"your-key\"");
  process.exit(1);
}

const params = new URLSearchParams({
  api_key: apiKey,
  q: query,
  num: numResults.toString(),
  engine: engine
});

if (location) {
  params.set("location", location);
}

const url = `https://serpapi.com/search?${params.toString()}`;

console.log(`🔍 Searching "${query}" on ${engine}...`);

try {
  const resp = await fetch(url);
  const data = await resp.json();
  
  if (data.error) {
    console.error(`SerpAPI Error: ${data.error}`);
    process.exit(1);
  }
  
  console.log("\n## Results\n");
  
  if (data.organic_results && data.organic_results.length > 0) {
    data.organic_results.slice(0, numResults).forEach((r, i) => {
      console.log(`${i + 1}. **${r.title}**`);
      console.log(`   Link: ${r.link}`);
      if (r.snippet) console.log(`   Snippet: ${r.snippet}`);
      console.log("");
    });
  } else {
    console.log("No results found.\n");
  }
  
  if (data.knowledge_graph) {
    console.log("## Knowledge Graph\n");
    console.log(data.knowledge_graph.description || "No description");
    console.log("");
  }
  
  console.log(`_Total results: ${data.search_information?.total_results || "unknown"}_`);
  
} catch (err) {
  console.error(`Search failed: ${err.message}`);
  process.exit(1);
}
