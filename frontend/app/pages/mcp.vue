<script setup lang="ts">
const sections = [
  { id: 'overview', label: 'Overview' },
  { id: 'setup', label: 'Setup' },
  { id: 'cursor', label: 'Cursor' },
  { id: 'vscode', label: 'VS Code' },
  { id: 'claude', label: 'Claude Desktop' },
  { id: 'tools', label: 'Available Tools' }
]

const activeSection = ref('overview')

function scrollTo(id: string) {
  activeSection.value = id
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <div class="h-full flex flex-col">
    <!-- Header -->
    <div class="border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-6 py-4">
      <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
        MCP Server
      </h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
        Connect AI assistants to Data Pebbles via the Model Context Protocol
      </p>
    </div>

    <div class="flex-1 overflow-hidden flex">
      <!-- Sidebar nav -->
      <nav class="hidden md:block w-52 shrink-0 border-r border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 overflow-y-auto py-4 px-3">
        <button
          v-for="s in sections"
          :key="s.id"
          class="block w-full text-left px-3 py-1.5 rounded text-sm transition-colors"
          :class="activeSection === s.id
            ? 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white font-medium'
            : 'text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'"
          @click="scrollTo(s.id)"
        >
          {{ s.label }}
        </button>
      </nav>

      <!-- Content -->
      <div class="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-950 p-6 lg:p-10">
        <div class="max-w-3xl mx-auto space-y-12">
          <!-- Overview -->
          <section id="overview">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              Overview
            </h2>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Data Pebbles exposes an <a
                href="https://modelcontextprotocol.io"
                target="_blank"
                rel="noopener noreferrer"
                class="underline hover:text-gray-900 dark:hover:text-white"
              >MCP</a> server that lets AI assistants interact with your data lake directly. All bronze, silver, and gold layer operations are available as MCP tools.
            </p>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              The server is powered by <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded">fastapi-mcp</code> and uses the SSE transport, automatically exposing every API endpoint as an MCP tool.
            </p>
            <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
              <div class="flex items-center gap-2 text-sm">
                <span class="text-gray-500 dark:text-gray-400">Endpoint:</span>
                <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded font-mono">http://localhost:8000/mcp</code>
              </div>
              <div class="flex items-center gap-2 text-sm mt-2">
                <span class="text-gray-500 dark:text-gray-400">Transport:</span>
                <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded font-mono">SSE (Server-Sent Events)</code>
              </div>
            </div>
          </section>

          <!-- Setup -->
          <section id="setup">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              Setup
            </h2>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              The MCP server starts automatically with the backend — no extra configuration needed. When the backend is running, the MCP endpoint is available at <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded">/mcp</code>.
            </p>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              To connect an AI assistant, add the server URL to your client's MCP configuration. The examples below assume the backend is running at <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded">http://localhost:8000</code>.
            </p>
          </section>

          <!-- Cursor -->
          <section id="cursor">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              Cursor
            </h2>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Add the following to your <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded">.cursor/mcp.json</code> in your project root:
            </p>
            <CodeBlock
              lang="json"
              :code="`{
  &quot;mcpServers&quot;: {
    &quot;data-pebbles&quot;: {
      &quot;url&quot;: &quot;http://localhost:8000/mcp&quot;
    }
  }
}`"
            />
          </section>

          <!-- VS Code -->
          <section id="vscode">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              VS Code (GitHub Copilot)
            </h2>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Add the following to your <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded">.vscode/mcp.json</code> in your project root:
            </p>
            <CodeBlock
              lang="json"
              :code="`{
  &quot;servers&quot;: {
    &quot;data-pebbles&quot;: {
      &quot;type&quot;: &quot;sse&quot;,
      &quot;url&quot;: &quot;http://localhost:8000/mcp&quot;
    }
  }
}`"
            />
          </section>

          <!-- Claude Desktop -->
          <section id="claude">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              Claude Desktop
            </h2>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Add the following to your <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded">claude_desktop_config.json</code>:
            </p>
            <CodeBlock
              lang="json"
              :code="`{
  &quot;mcpServers&quot;: {
    &quot;data-pebbles&quot;: {
      &quot;command&quot;: &quot;npx&quot;,
      &quot;args&quot;: [
        &quot;mcp-remote&quot;,
        &quot;http://localhost:8000/mcp&quot;
      ]
    }
  }
}`"
            />
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-3">
              This uses <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded">mcp-remote</code> to bridge the SSE transport to Claude Desktop's stdio transport.
            </p>
          </section>

          <!-- Available Tools -->
          <section id="tools">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              Available Tools
            </h2>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
              All API endpoints are automatically exposed as MCP tools. The AI assistant can call any of the following:
            </p>

            <!-- Bronze tools -->
            <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-2">
              Bronze
            </h3>
            <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden mb-6">
              <table class="w-full text-sm">
                <thead>
                  <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900/50">
                    <th class="text-left py-2 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">
                      Tool
                    </th>
                    <th class="text-left py-2 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">
                      Description
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      create_resource_bronze_post
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Create a new bronze resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_resources_bronze_get
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all bronze resources
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      get_resource_bronze_resource_id_get
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Get metadata for a bronze resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      update_resource_bronze_resource_id_patch
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Rename a bronze resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      delete_resource_bronze_resource_id_delete
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Delete a bronze resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      upload_version_bronze_resource_id_versions_post
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Upload a file version
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_versions_bronze_resource_id_versions_get
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all versions
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      activate_version_bronze_resource_id_versions_version_patch
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Activate a specific version
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      delete_version_bronze_resource_id_versions_version_delete
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Delete a specific version
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Silver tools -->
            <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-2">
              Silver
            </h3>
            <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden mb-6">
              <table class="w-full text-sm">
                <thead>
                  <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900/50">
                    <th class="text-left py-2 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">
                      Tool
                    </th>
                    <th class="text-left py-2 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">
                      Description
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      create_resource_silver_post
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Create a new silver resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_resources_silver_get
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all silver resources
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      get_resource_silver_resource_id_get
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Get metadata for a silver resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      update_resource_silver_resource_id_patch
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Rename a silver resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      delete_resource_silver_resource_id_delete
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Delete a silver resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      upload_version_silver_resource_id_versions_post
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Upload a DataFrame version with bronze lineage
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_versions_silver_resource_id_versions_get
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all versions with lineage info
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Gold tools -->
            <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-2">
              Gold
            </h3>
            <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden">
              <table class="w-full text-sm">
                <thead>
                  <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900/50">
                    <th class="text-left py-2 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">
                      Tool
                    </th>
                    <th class="text-left py-2 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">
                      Description
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      create_resource_gold_post
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Create a new gold resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_resources_gold_get
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all gold resources
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      get_resource_gold_resource_id_get
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Get metadata for a gold resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      update_resource_gold_resource_id_patch
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Rename a gold resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      delete_resource_gold_resource_id_delete
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Delete a gold resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      upload_version_gold_resource_id_versions_post
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Upload a DataFrame version with silver lineage
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_versions_gold_resource_id_versions_get
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all versions with lineage info
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>
