import { defineConfig, devices } from '@playwright/test';
export default defineConfig({
  testDir: './tests/browser',
  timeout: 30_000,
  use: { baseURL: 'http://127.0.0.1:8000', trace: 'retain-on-failure' },
  webServer: { command: 'python -m server.run', url: 'http://127.0.0.1:8000/health', reuseExistingServer: true, timeout: 30_000 },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }]
});
