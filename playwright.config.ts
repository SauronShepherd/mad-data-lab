import { defineConfig, devices } from '@playwright/test';
const deployed = process.env.DEPLOYED_APP_URL;
const appToken = process.env.DATABRICKS_APP_TOKEN;
const useWebServer = !deployed && !process.env.SKIP_WEBSERVER;
export default defineConfig({
  testDir: './tests/browser',
  // Live Genie can legitimately take up to the backend's 75s request bound.
  // Keep the test bounded while allowing the real authenticated flow to finish.
  timeout: 120_000,
  use: {
    baseURL: deployed || 'http://127.0.0.1:8000',
    trace: 'retain-on-failure',
    ...(appToken ? { extraHTTPHeaders: { Authorization: `Bearer ${appToken}` } } : {}),
  },
  ...(useWebServer ? { webServer: { command: 'python -m server.run', url: 'http://127.0.0.1:8000/health', reuseExistingServer: true, timeout: 30_000 } } : {}),
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }]
});
