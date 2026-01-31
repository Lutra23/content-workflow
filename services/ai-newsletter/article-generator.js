// AI 新闻深度分析文章生成器 - 使用云雾 API Gemini
// 2026-01-30

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const { aggregate } = require('./aggregator');

// 云雾 API 配置
const YUNWU_API_URL = process.env.YUNWU_API_URL || 'https://yunwu.ai/v1';
const YUNWU_API_KEY = process.env.YUNWU_API_KEY || 'sk-6vUtyDKZHLtFuRGRJSuua8hk7GF9Xli3k19VyhzVurkfTU93';

const MODEL = 'gemini-3-flash-preview';

// 调用云雾 API
async function callGemini(prompt, maxTokens = 2000) {
  try {
    const response = await axios.post(
      `${YUNWU_API_URL}/chat/completions`,
      {
        model: MODEL,
        messages: [{ role: 'user', content: prompt }],
        max_tokens: maxTokens,
        temperature: 0.7,
      },
      {
        headers: {
          'Authorization': `Bearer ${YUNWU_API_KEY}`,
          'Content-Type': 'application/json',
        },
        timeout: 120,
      }
    );
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('❌ API Error:', error.message);
    return null;
  }
}

// 生成深度分析文章
async function generateArticle() {
  console.log('📝 生成深度分析文章...\n');
  
  // 1. 获取新闻数据
  const { items, stats } = await aggregate(50);
  const today = new Date().toLocaleDateString('zh-CN', {
    year: 'numeric', month: 'long', day: 'numeric', weekday: 'long',
  });
  
  console.log(`📊 数据: HN:${stats.hn} RSS:${stats.rss} 论文:${stats.paper} Reddit:${stats.reddit}`);
  
  // 2. 生成文章（简化版，一次性生成）
  const prompt = `你是资深科技评论员。请根据以下 AI 新闻，写一篇 1500 字的深度分析文章。

要求：
1. 开头引入今日热点 (100字)
2. 分析 3 个最有价值的主题 (每主题 300-400字)
3. 结尾总结 + 行动建议 (200字)
4. 语言专业但易懂，有独特见解
5. 用中文，直接写文章不要大纲
6. 不要重复新闻标题

新闻列表：
${items.slice(0, 15).map((i, idx) => `${idx+1}. ${i.title.substring(0, 80)}`).join('\n')}

请直接输出文章正文：`;

  console.log('🔄 调用 Gemini 生成文章...');
  const content = await callGemini(prompt, 3000);
  
  if (!content) {
    console.error('❌ 生成失败');
    return null;
  }
  
  // 3. 组装完整文章
  const article = `# 🤖 AI 新闻深度分析 | ${today}

> 由 lutra AI 新闻简报服务自动生成
> 数据来源: HN(${stats.hn}) RSS(${stats.rss}) 论文(${stats.paper}) Reddit(${stats.reddit})

---

${content}

---

*AI 相关内容占比: ${Math.round(stats.aiRelated / stats.total * 100)}%*

*本文由 AI 自动生成，仅供参考。*
`;

  // 4. 保存
  const dateStr = new Date().toISOString().split('T')[0];
  const filePath = path.join(__dirname, 'articles', `${dateStr}-analysis.md`);
  fs.writeFileSync(filePath, article);
  
  console.log(`\n✅ 文章已生成: ${filePath}`);
  return article;
}

// 导出
module.exports = { generateArticle };

// 测试
if (require.main === module) {
  generateArticle().then(article => {
    if (article) {
      console.log('\n📄 预览 (前 800 字):');
      console.log(article.substring(0, 800));
    }
  });
}
