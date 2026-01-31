import type { HookHandler } from '../../../.nvm/versions/node/v24.12.0/lib/node_modules/clawdbot/dist/hooks/hooks.js';
import { resolveAgentWorkspaceDir } from '../../../.nvm/versions/node/v24.12.0/lib/node_modules/clawdbot/dist/agents/agent-scope.js';
import { resolveAgentIdFromSessionKey } from '../../../.nvm/versions/node/v24.12.0/lib/node_modules/clawdbot/dist/routing/session-key.js';
import path from 'node:path';

const handler: HookHandler = async (event) => {
  // Only trigger on 'new' command
  if (event.type !== 'command' || event.action !== 'new') {
    return;
  }

  const context = event.context || {};
  const cfg = context.cfg;
  const agentId = resolveAgentIdFromSessionKey(event.sessionKey);
  // Use same resolution logic as session-memory hook
  const workspaceDir = cfg
    ? resolveAgentWorkspaceDir(cfg, agentId)
    : path.join(process.env.HOME || '/root', 'clawd');

  if (!workspaceDir) {
    console.log('[git-notes-sync] No workspace dir found');
    return;
  }

  const { execSync } = await import('child_process');
  const pythonPath = 'python3';
  const memoryScript = `${workspaceDir}/skills/git-notes-memory/memory.py`;

  try {
    const result = execSync(`${pythonPath} "${memoryScript}" -p "${workspaceDir}" sync --start`, {
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    console.log('🔄 [git-notes-sync] 记忆同步完成');
    if (result.trim()) {
      console.log('   同步详情:', result.trim().replace(/\n/g, '\n   '));
    }
  } catch (err) {
    console.error('❌ [git-notes-sync] 同步失败:', err instanceof Error ? err.message : String(err));
  }
};

export default handler;
