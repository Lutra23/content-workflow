// GitHub 数据采集器 - 使用 Search API
// 2026-01-31

const https = require('https');

const GITHUB_API = 'https://api.github.com';

// 缓存
let cache = null;
let lastFetch = 0;
const CACHE_DURATION = 4 * 60 * 60 * 1000; // 4小时

/**
 * 搜索热门 AI 仓库
 */
async function fetchTrendingAI(limit = 10) {
  const now = Date.now();
  
  // 检查缓存
  if (cache && (now - lastFetch) < CACHE_DURATION) {
    console.log('📦 使用 GitHub 缓存');
    return cache.slice(0, limit);
  }
  
  // AI 相关关键词搜索
  const query = 'topic:ai topic:machine-learning topic:llm topic:agent sort:stars-desc';
  const url = `${GITHUB_API}/search/repositories?q=${encodeURIComponent(query)}&per_page=${limit}`;
  
  console.log(`🔄 获取 GitHub AI 热门: ${url}`);
  
  return new Promise((resolve, reject) => {
    https.get(url, {
      headers: {
        'User-Agent': 'Clawdbot-AI-Newsletter',
        'Accept': 'application/vnd.github.v3+json',
      }
    }, (res) => {
      let data = '';
      
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          const repos = (result.items || []).map(repo => ({
            id: `gh-${repo.owner.login}-${repo.name}`,
            type: 'github',
            title: `${repo.owner.login}/${repo.name}`,
            description: repo.description || '',
            url: repo.html_url,
            author: repo.owner.login,
            repo: repo.name,
            language: repo.language,
            stars: repo.stargazers_count,
            forks: repo.forks_count,
            todayStars: 0, // API 不提供今日 stars
            updated: repo.updated_at,
            text: `${repo.full_name} ${repo.description} ${repo.language}`.toLowerCase(),
            aiScore: calculateAIScore(repo.description + ' ' + repo.language),
            importance: calculateImportance(repo),
          }));
          
          // 更新缓存
          cache = repos;
          lastFetch = now;
          
          resolve(repos.slice(0, limit));
        } catch (e) {
          console.error('❌ GitHub API 解析失败:', e.message);
          resolve([]);
        }
      });
    }).on('error', (e) => {
      console.error('❌ GitHub API 请求失败:', e.message);
      resolve([]);
    });
  });
}

/**
 * 获取最近创建的 AI 仓库
 */
async function fetchNewAIProjects(limit = 10) {
  const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
  const query = `topic:ai created:>${sevenDaysAgo} sort:created-desc`;
  const url = `${GITHUB_API}/search/repositories?q=${encodeURIComponent(query)}&per_page=${limit}`;
  
  console.log(`🔄 获取新 AI 项目: ${url}`);
  
  return new Promise((resolve, reject) => {
    https.get(url, {
      headers: {
        'User-Agent': 'Clawdbot-AI-Newsletter',
        'Accept': 'application/vnd.github.v3+json',
      }
    }, (res) => {
      let data = '';
      
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          const repos = (result.items || []).map(repo => ({
            id: `gh-new-${repo.owner.login}-${repo.name}`,
            type: 'github-new',
            title: `${repo.owner.login}/${repo.name}`,
            description: repo.description || '',
            url: repo.html_url,
            author: repo.owner.login,
            repo: repo.name,
            language: repo.language,
            stars: repo.stargazers_count,
            forks: repo.forks_count,
            created: repo.created_at,
            text: `${repo.full_name} ${repo.description} ${repo.language}`.toLowerCase(),
            aiScore: calculateAIScore(repo.description + ' ' + repo.language),
            importance: calculateImportance(repo),
          }));
          
          resolve(repos);
        } catch (e) {
          console.error('❌ GitHub API 解析失败:', e.message);
          resolve([]);
        }
      });
    }).on('error', (e) => {
      console.error('❌ GitHub API 请求失败:', e.message);
      resolve([]);
    });
  });
}

/**
 * AI 相关性评分
 */
function calculateAIScore(text) {
  const aiKeywords = ['ai', 'llm', 'gpt', 'claude', 'agent', 'machine learning', 
                      'neural', 'deep learning', 'langchain', 'rag', 'copilot',
                      'automation', 'generative', 'vector', 'embedding', 'python',
                      'rag', 'retrieval', 'fine-tuning', 'training'];
  const lower = (text || '').toLowerCase();
  let score = 0;
  
  for (const word of aiKeywords) {
    if (lower.includes(word)) score += 1;
  }
  
  return score;
}

/**
 * 重要性评分
 */
function calculateImportance(repo) {
  let score = repo.stargazers_count * 0.5 + repo.forks_count * 0.3;
  
  // 新仓库加分
  const age = (Date.now() - new Date(repo.created_at).getTime()) / (24 * 60 * 60 * 1000);
  if (age < 7) score += 50 / (age + 1);
  
  return score;
}

// 导出
module.exports = { fetchTrendingAI, fetchNewAIProjects };

// 测试
if (require.main === module) {
  console.log('\n🔍 GitHub AI 热门仓库:');
  fetchTrendingAI(5).then(repos => {
    console.log(`\n📊 获取到 ${repos.length} 个仓库`);
    repos.forEach((repo, i) => {
      console.log(`  ${i+1}. ⭐${repo.stars} ${repo.title}`);
      console.log(`     ${repo.description?.substring(0, 60) || 'No description'}`);
    });
  }).catch(console.error);
}
