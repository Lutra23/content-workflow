// RSS 采集器 - AI 垂直媒体
// 2026-01-30

const Parser = require('rss-parser');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const parser = new Parser();
const DATA_DIR = path.join(__dirname, 'data');
const CACHE_FILE = path.join(DATA_DIR, 'rss-cache.json');

// RSS 源配置
const FEEDS = [
  // 传统媒体
  {
    name: 'MIT AI',
    url: 'https://news.mit.edu/rss/topic/artificial-intelligence2',
    keywords: ['ai', 'llm', 'machine learning'],
  },
  {
    name: 'OpenAI Blog',
    url: 'https://openai.com/blog/rss.xml',
    keywords: [],
  },
  {
    name: 'Google AI',
    url: 'http://googleaiblog.blogspot.com/atom.xml',
    keywords: [],
  },
  {
    name: 'AI Weekly',
    url: 'https://www.linkedin.com/people/ai-weekly/rss',
    keywords: [],
  },
  {
    name: 'The Batch',
    url: 'https://www.deeplearning.ai/the-batch/feed/',
    keywords: [],
  },
  // Reddit RSS (无需认证)
  {
    name: 'Reddit: LocalLLaMA',
    url: 'https://www.reddit.com/r/LocalLLaMA/.rss',
    keywords: [],
  },
  {
    name: 'Reddit: MachineLearning',
    url: 'https://www.reddit.com/r/MachineLearning/.rss',
    keywords: [],
  },
  {
    name: 'Reddit: ClaudeAI',
    url: 'https://www.reddit.com/r/ClaudeAI/.rss',
    keywords: [],
  },
  {
    name: 'Reddit: ChatGPT',
    url: 'https://www.reddit.com/r/ChatGPT/.rss',
    keywords: [],
  },
  // 开发者社区
  {
    name: 'Hacker News',
    url: 'https://news.ycombinator.com/rss',
    keywords: [],
  },
];

// 加载缓存
function loadCache() {
  try {
    if (fs.existsSync(CACHE_FILE)) {
      return JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
    }
  } catch (e) {}
  return { items: [], lastFetch: null };
}

// 保存缓存
function saveCache(cache) {
  fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2));
}

// 抓取单个 RSS 源
async function fetchFeed(feedConfig) {
  try {
    const feed = await parser.parseURL(feedConfig.url);
    
    return feed.items.slice(0, 10).map(item => ({
      title: item.title,
      link: item.link,
      pubDate: item.pubDate || item.isoDate,
      content: item.contentSnippet || item.content || '',
      source: feedConfig.name,
      collectedAt: new Date().toISOString(),
    }));
  } catch (error) {
    console.error(`❌ ${feedConfig.name}: ${error.message}`);
    return [];
  }
}

// 抓取所有 RSS
async function fetchAll(maxFeeds = null) {
  const cache = loadCache();
  const now = Date.now();
  
  // 重复抓2 小时内不取
  if (cache.lastFetch && (now - cache.lastFetch) < 7200000) {
    console.log('⏱️  RSS 缓存有效 (2小时内)');
    return cache.items;
  }
  
  console.log('📥 正在抓取 RSS 源...');
  
  const feedsToFetch = maxFeeds ? FEEDS.slice(0, maxFeeds) : FEEDS;
  const promises = feedsToFetch.map(feed => fetchFeed(feed));
  const results = await Promise.all(promises);
  
  // 合并去重
  const allItems = results.flat();
  const seenLinks = new Set();
  const uniqueItems = [];
  
  for (const item of allItems) {
    if (!seenLinks.has(item.link)) {
      seenLinks.add(item.link);
      uniqueItems.push(item);
    }
  }
  
  // 保存缓存
  cache.items = uniqueItems;
  cache.lastFetch = now;
  saveCache(cache);
  
  console.log(`✅ RSS 抓取完成: ${uniqueItems.length} 条 (去重后)`);
  return uniqueItems;
}

// 导出
module.exports = { fetchAll, FEEDS };

// 测试运行
if (require.main === module) {
  fetchAll(3).then(items => {
    console.log('\n📰 RSS 最新:');
    items.slice(0, 5).forEach((item, i) => {
      console.log(`  ${i+1}. [${item.source}] ${item.title.substring(0, 60)}...`);
    });
  });
}
