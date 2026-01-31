// 新闻聚合器 - 合并多个数据源
// 2026-01-31

const fs = require('fs');
const path = require('path');
const { fetchTopStories } = require('./collectors/hn.cjs');
const { fetchTrendingAI } = require('./collectors/github.cjs');

const DATA_DIR = path.join(__dirname, 'data');
const COMBINED_FILE = path.join(DATA_DIR, 'combined.json');

// AI 关键词权重
const AI_KEYWORDS = [
  { word: 'ai', weight: 1 },
  { word: 'llm', weight: 2 },
  { word: 'gpt', weight: 2 },
  { word: 'claude', weight: 2 },
  { word: 'agent', weight: 2 },
  { word: 'machine learning', weight: 1.5 },
  { word: 'neural', weight: 1.5 },
  { word: 'deep learning', weight: 1.5 },
  { word: 'automation', weight: 1 },
  { word: 'generative', weight: 1.5 },
  { word: 'copilot', weight: 1 },
  { word: 'langchain', weight: 2 },
  { word: 'rag', weight: 2 },
  { word: 'vector', weight: 1.5 },
  { word: 'embedding', weight: 2 },
];

// 计算 AI 相关性分数
function calculateAIScore(text) {
  const lower = (text || '').toLowerCase();
  let score = 0;
  
  for (const { word, weight } of AI_KEYWORDS) {
    if (lower.includes(word)) {
      score += weight;
    }
  }
  
  return score;
}

// 合并并排序新闻
async function aggregate(limit = 50) {
  console.log('🔄 聚合数据源...');
  
  // 并行抓取数据源
  const [hnItems, githubItems] = await Promise.all([
    fetchTopStories(30),
    fetchTrendingAI(10),
  ]);
  
  // 合并所有数据源
  const allItems = [
    // HN 热门
    ...hnItems.map(item => ({
      ...item,
      type: 'hn',
      text: item.title + ' ' + item.domain,
    })),
    // GitHub 热门
    ...githubItems.map(item => ({
      ...item,
      type: 'github',
      domain: 'github.com',
      text: item.title + ' ' + item.description,
    })),
  ];
  
  // 计算 AI 分数
  const scoredItems = allItems.map(item => ({
    ...item,
    aiScore: calculateAIScore(item.text),
    importance: calculateImportance(item),
  }));
  
  // 排序：AI 相关性优先，然后是重要性
  scoredItems.sort((a, b) => {
    if (a.aiScore > 0 && b.aiScore === 0) return -1;
    if (a.aiScore === 0 && b.aiScore > 0) return 1;
    return b.importance - a.importance;
  });
  
  // 去重
  const unique = [];
  const seenTitles = new Set();
  
  for (const item of scoredItems) {
    const titleKey = item.title.toLowerCase().substring(0, 60);
    if (!seenTitles.has(titleKey)) {
      seenTitles.add(titleKey);
      unique.push(item);
    }
  }
  
  // 保存
  const result = unique.slice(0, limit);
  fs.writeFileSync(COMBINED_FILE, JSON.stringify(result, null, 2));
  
  // 统计
  const stats = {
    total: result.length,
    hn: result.filter(i => i.type === 'hn').length,
    github: result.filter(i => i.type === 'github').length,
    aiRelated: result.filter(i => i.aiScore > 0).length,
  };
  
  console.log(`✅ 聚合完成: ${stats.total} 条 (HN:${stats.hn} GitHub:${stats.github})`);
  console.log(`   AI 相关: ${stats.aiRelated}`);
  
  return { items: result, stats };
}

// 计算重要性分数
function calculateImportance(item) {
  let score = item.score || 0;
  
  // 类型加权
  const typeWeight = { hn: 1.2, github: 1.3 };
  score *= typeWeight[item.type] || 1;
  
  // AI 相关加权
  if (item.aiScore > 0) score *= 1.5;
  
  return score;
}

// 生成今日简报
function generateBriefing(items) {
  const today = new Date().toLocaleDateString('zh-CN', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
  
  const aiNews = items.filter(i => i.aiScore > 0);
  const byType = {
    hn: items.filter(i => i.type === 'hn'),
    github: items.filter(i => i.type === 'github'),
  };
  
  return {
    date: today,
    summary: {
      total: items.length,
      ai: aiNews.length,
      byType,
    },
    topHN: byType.hn.slice(0, 3),
    topGitHub: byType.github.slice(0, 3),
    generatedAt: new Date().toISOString(),
  };
}

// 导出
module.exports = { aggregate, generateBriefing };

// 测试
if (require.main === module) {
  aggregate(30).then(({ items, stats }) => {
    console.log('\n📊 数据统计:', stats);
    console.log('\n📋 Top 新闻:');
    items.slice(0, 5).forEach((item, i) => {
      const icon = { hn: '📈', github: '⭐' }[item.type] || '📝';
      console.log(`  ${i+1}. ${icon} ${item.title.substring(0, 50)}...`);
    });
  });
}
