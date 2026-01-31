// Arxiv 论文采集器 - AI/ML 最新论文
// 2026-01-30

const axios = require('axios');
const xml2js = require('xml2js');
const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, 'data');
const CACHE_FILE = path.join(__dirname, 'data', 'arxiv-cache.json');

// Arxiv API
const ARXIV_API = 'https://export.arxiv.org/api/query';

// AI/ML 相关分类
const CATEGORIES = [
  { id: 'cs.AI', name: 'AI' },
  { id: 'cs.LG', name: 'ML' },
  { id: 'cs.CL', name: 'NLP' },
  { id: 'cs.NE', name: 'Neural' },
];

// XML 解析器
const parser = new xml2js.Parser({
  explicitArray: false,
  mergeAttrs: true,
});

// 加载缓存
function loadCache() {
  try {
    if (fs.existsSync(CACHE_FILE)) {
      return JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
    }
  } catch (e) {}
  return { items: [], lastFetch: null };
}

function saveCache(cache) {
  fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2));
}

// 抓取单分类论文
async function fetchCategory(cat, limit = 10) {
  try {
    // 简化查询：不用日期过滤，按提交时间排序取最新的
    const response = await axios.get(ARXIV_API, {
      params: {
        search_query: `cat:${cat.id}`,
        sortBy: 'submittedDate',
        sortOrder: 'descending',
        max_results: limit,
      },
      timeout: 30000,
    });
    
    const result = await parser.parseStringPromise(response.data);
    const entries = result.feed.entry || [];
    
    const items = (Array.isArray(entries) ? entries : [entries]).map(entry => ({
      id: entry.id?.split('/abs/')[1] || '',
      title: entry.title?.replace(/\n/g, ' ').trim() || '',
      summary: entry.summary?.replace(/\n/g, ' ').trim() || '',
      authors: entry.author?.map?.(a => a.name) || [entry.author?.name].filter(Boolean),
      category: [cat.name],
      published: entry.published,
      pdf_url: entry.id,
      source: 'Arxiv',
      collectedAt: new Date().toISOString(),
    }));
    
    console.log(`   ✅ ${cat.name}: ${items.length} 篇`);
    return items;
  } catch (error) {
    console.error(`   ❌ ${cat.name}: ${error.response?.status || error.message}`);
    return [];
  }
}

// 抓取所有分类
async function fetchArxiv(limitPerCat = 10) {
  const cache = loadCache();
  const now = Date.now();
  
  // 6 小时内不重复抓取
  if (cache.lastFetch && (now - cache.lastFetch) < 21600000) {
    console.log('⏱️  Arxiv 缓存有效 (6小时内)');
    return cache.items.slice(0, limitPerCat * CATEGORIES.length);
  }
  
  console.log('📥 正在抓取 Arxiv 论文...');
  
  try {
    // 并行抓取所有分类
    const promises = CATEGORIES.map(cat => fetchCategory(cat, limitPerCat));
    const results = await Promise.all(promises);
    
    // 合并
    const allItems = results.flat();
    
    // 按发布时间排序（最新的在前）
    allItems.sort((a, b) => new Date(b.published) - new Date(a.published));
    
    // 去重
    const seen = new Set();
    const uniqueItems = [];
    for (const item of allItems) {
      if (!seen.has(item.id)) {
        seen.add(item.id);
        uniqueItems.push(item);
      }
    }
    
    // 保存缓存
    cache.items = uniqueItems;
    cache.lastFetch = now;
    saveCache(cache);
    
    console.log(`✅ Arxiv 抓取完成: ${uniqueItems.length} 篇论文`);
    return uniqueItems;
    
  } catch (error) {
    console.error('❌ Arxiv 抓取失败:', error.message);
    return cache.items.slice(0, limitPerCat * CATEGORIES.length);
  }
}

// 导出
module.exports = { fetchArxiv, CATEGORIES };

// 测试
if (require.main === module) {
  fetchArxiv(5).then(papers => {
    console.log('\n📚 最新论文:');
    papers.slice(0, 5).forEach((p, i) => {
      console.log(`  ${i+1}. [${p.category[0]}] ${p.title.substring(0, 60)}...`);
    });
  });
}
