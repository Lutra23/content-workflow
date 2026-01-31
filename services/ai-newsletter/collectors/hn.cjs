// 数据采集器 - Hacker News
// 2026-01-30, 使用内置 fetch

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, 'data');
const CACHE_FILE = path.join(DATA_DIR, 'hn-cache.json');

// 确保目录存在
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

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

// 获取 HN Top Stories
async function fetchTopStories(limit = 30) {
  const cache = loadCache();
  const now = Date.now();
  const CACHE_DURATION = 30 * 60 * 1000; // 30分钟缓存
  
  // 检查缓存
  if (cache.items && cache.items.length > 0 && (now - cache.lastFetch) < CACHE_DURATION) {
    console.log(`📦 使用 HN 缓存 (${Math.round((now - cache.lastFetch) / 60000)}分钟前)`);
    return cache.items.slice(0, limit);
  }
  
  try {
    // 获取 Top Stories IDs
    const idsRes = await fetch('https://hacker-news.firebaseio.com/v0/topstories.json');
    const ids = await idsRes.json();
    
    // 并行获取前 N 个故事详情
    const topIds = ids.slice(0, limit);
    const stories = await Promise.all(
      topIds.map(async (id) => {
        try {
          const res = await fetch(`https://hacker-news.firebaseio.com/v0/item/${id}.json`);
          return await res.json();
        } catch (e) {
          return null;
        }
      })
    );
    
    // 过滤并格式化
    const items = stories
      .filter(s => s && s.url) // 只保留有 URL 的
      .map(s => ({
        id: `hn-${s.id}`,
        type: 'hn',
        title: s.title,
        url: s.url,
        domain: new URL(s.url).hostname.replace('www.', ''),
        score: s.score,
        author: s.by,
        timestamp: s.time,
        text: s.title,
      }));
    
    // 更新缓存
    saveCache({ items, lastFetch: now });
    
    console.log(`🔄 获取 HN Top Stories: ${items.length} 条`);
    return items;
  } catch (e) {
    console.error('❌ HN API 错误:', e.message);
    return cache.items || [];
  }
}

// 导出
module.exports = { fetchTopStories };

// 测试
if (require.main === module) {
  fetchTopStories(5).then(stories => {
    console.log('\n📊 HN Top Stories:');
    stories.forEach((s, i) => {
      console.log(`  ${i+1}. [${s.score}] ${s.title}`);
      console.log(`     ${s.domain}`);
    });
  }).catch(console.error);
}
