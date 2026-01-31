// 每日定时任务 - 早上 8:00 自动生成简报和文章
// 2026-01-30

const cron = require('node-cron');
const { aggregate, generateBriefing } = require('./aggregator');
const { generateArticle } = require('./article-generator');
const fs = require('fs');
const path = require('path');

const BRIEFINGS_DIR = path.join(__dirname, 'briefings');
const ARTICLES_DIR = path.join(__dirname, 'articles');

// 确保目录存在
if (!fs.existsSync(BRIEFINGS_DIR)) {
  fs.mkdirSync(BRIEFINGS_DIR, { recursive: true });
}

// 生成并保存今日简报
async function generateTodayBriefing() {
  console.log('\n🕘 定时任务触发: 生成今日简报');
  const startTime = Date.now();
  
  try {
    // 聚合新闻
    const items = await aggregate(20);
    const briefing = generateBriefing(items);
    
    // 保存文件
    const dateStr = new Date().toISOString().split('T')[0];
    const filePath = path.join(BRIEFINGS_DIR, `${dateStr}.json`);
    fs.writeFileSync(filePath, JSON.stringify(briefing, null, 2));
    
    // 同时保存 Markdown 版本
    const mdPath = path.join(BRIEFINGS_DIR, `${dateStr}.md`);
    const markdown = generateMarkdown(briefing);
    fs.writeFileSync(mdPath, markdown);
    
    console.log(`✅ 简报已生成: ${filePath}`);
    console.log(`   Markdown: ${mdPath}`);
    console.log(`   耗时: ${Date.now() - startTime}ms`);
    
    return briefing;
  } catch (error) {
    console.error('❌ 生成失败:', error.message);
    throw error;
  }
}

// 生成 Markdown 格式
function generateMarkdown(briefing) {
  const { date, summary, topAI } = briefing;
  
  let md = `# 🤖 AI 新闻简报 - ${date}\n\n`;
  md += `> 自动生成 | 共 ${summary.total} 条新闻\n\n`;
  md += `---\n\n`;
  md += `## 📊 今日概览\n\n`;
  md += `- **AI 相关**: ${summary.ai} 条\n`;
  md += `- **生成时间**: ${new Date().toLocaleString('zh-CN')}\n\n`;
  md += `---\n\n`;
  md += `## 🔥 Top AI 新闻\n\n`;
  
  topAI.forEach((item, i) => {
    md += `### ${i+1}. ${item.title}\n\n`;
    md += `- **来源**: ${item.domain}\n`;
    md += `- **热度**: ${item.score} points\n`;
    md += `- **链接**: ${item.url || item.link}\n\n`;
  });
  
  md += `---\n\n`;
  md += `*由 lutra AI 新闻简报服务自动生成*\n`;
  
  return md;
}

// 启动定时任务
function startScheduler() {
  // 每天早上 8:00 运行
  cron.schedule('0 8 * * *', async () => {
    console.log('\n🕘 定时任务触发');
    await generateTodayBriefing();
    await generateTodayArticle();
  });
  
  console.log('⏰ 定时任务已启动');
  console.log('   每天 8:00 自动生成简报 + 文章');
  
  // 也立即运行一次（测试用）
  console.log('\n🚀 立即生成今日内容...');
  return generateTodayBriefing().then(() => generateTodayArticle());
}

// 生成今日文章
async function generateTodayArticle() {
  console.log('\n📝 生成今日分析文章...');
  const startTime = Date.now();
  
  try {
    await generateArticle();
    console.log(`✅ 文章已生成，耗时: ${Date.now() - startTime}ms`);
  } catch (error) {
    console.error('❌ 文章生成失败:', error.message);
  }
}

// 导出
module.exports = { startScheduler, generateTodayBriefing };

// 测试运行
if (require.main === module) {
  startScheduler();
}
