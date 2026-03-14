<script setup lang="ts">
const sections = [
  { id: 'installation', label: 'Installation' },
  { id: 'quickstart', label: 'Quick Start' },
  { id: 'bronze', label: 'Bronze Layer' },
  { id: 'silver', label: 'Silver Layer' },
  { id: 'gold', label: 'Gold Layer' },
  { id: 'transforms', label: 'Transform Decorators' }
]

const activeSection = ref('installation')

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
        SDK Documentation
      </h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
        Python SDK for the Data Pebbles platform
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
          <!-- Installation -->
          <section id="installation">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              Installation
            </h2>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Install the SDK with pip or uv:
            </p>
            <CodeBlock
              code="pip install data-pebbles"
              lang="bash"
            />
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-3">
              Dependencies: <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded">polars</code>, <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded">httpx</code>, <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded">mlflow</code>
            </p>
          </section>

          <!-- Quick Start -->
          <section id="quickstart">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              Quick Start
            </h2>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Create a <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded">DataPebbles</code> client and access the bronze, silver, and gold layers:
            </p>
            <CodeBlock
              code="from data_pebbles import DataPebbles

dp = DataPebbles(&quot;http://localhost:8000&quot;, token=&quot;your-token&quot;)

# List bronze sources
sources = dp.bronze.list_sources()

# Upload a file to bronze
dp.bronze.create_source(&quot;raw_sales&quot;)
dp.bronze.upload(1, file_path=&quot;sales.csv&quot;)

# Download and transform through the layers
raw = dp.bronze.download(1)
df  = dp.silver.download(2)
dp.gold.upload(3, df, from_source_ids=[2])"
            />
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-3">
              The client can also be used as a context manager:
            </p>
            <CodeBlock
              code="with DataPebbles(&quot;http://localhost:8000&quot;) as dp:
    sources = dp.bronze.list_sources()"
            />
          </section>

          <!-- Bronze Layer -->
          <section id="bronze">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              Bronze Layer
            </h2>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
              The bronze layer stores raw, unprocessed files. Upload any file format and download the raw bytes.
            </p>
            <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden">
              <table class="w-full text-sm">
                <thead>
                  <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900/50">
                    <th class="text-left py-2 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">
                      Method
                    </th>
                    <th class="text-left py-2 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">
                      Description
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      create_source(name)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Create a new bronze source
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_sources()
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all bronze sources
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      get_source(source_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Get metadata for a source
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      update_source(source_id, name)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Rename a source
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      delete_source(source_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Delete a source and all its versions
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_versions(source_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all versions of a source
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      upload(source_id, *, file_path=None, data=None)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Upload a file by path or raw bytes
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      download(source_id, *, version=None)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Download raw bytes (latest version by default)
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      activate_version(source_id, version)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Set a version as active
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      delete_version(source_id, version)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Delete a specific version
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- Silver Layer -->
          <section id="silver">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              Silver Layer
            </h2>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
              The silver layer stores cleaned, structured data as Parquet. Upload and download Polars DataFrames/LazyFrames with lineage tracking back to bronze.
            </p>
            <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden">
              <table class="w-full text-sm">
                <thead>
                  <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900/50">
                    <th class="text-left py-2 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">
                      Method
                    </th>
                    <th class="text-left py-2 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">
                      Description
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      create_source(name)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Create a new silver source
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_sources()
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all silver sources
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      get_source(source_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Get metadata for a source
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      update_source(source_id, name)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Rename a source
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      delete_source(source_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Delete a source and all its versions
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_versions(source_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all versions with lineage info
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      upload(source_id, data, *, from_source_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Upload a DataFrame/LazyFrame with bronze lineage
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      download(source_id, *, version=None)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Download as a Polars LazyFrame
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- Gold Layer -->
          <section id="gold">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              Gold Layer
            </h2>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
              The gold layer stores aggregated, business-ready data as Parquet. Supports multi-source lineage from silver.
            </p>
            <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden">
              <table class="w-full text-sm">
                <thead>
                  <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900/50">
                    <th class="text-left py-2 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">
                      Method
                    </th>
                    <th class="text-left py-2 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">
                      Description
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      create_source(name)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Create a new gold source
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_sources()
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all gold sources
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      get_source(source_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Get metadata for a source
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      update_source(source_id, name)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Rename a source
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      delete_source(source_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Delete a source and all its versions
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_versions(source_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all versions with lineage info
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      upload(source_id, data, *, from_source_ids)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Upload a DataFrame/LazyFrame with silver lineage
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      download(source_id, *, version=None)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Download as a Polars LazyFrame
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- Transform Decorators -->
          <section id="transforms">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              Transform Decorators
            </h2>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
              Decorators that automate downloading, transforming, and uploading data between layers with lineage tracking.
            </p>

            <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-2">
              silver_transform
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Transforms bronze → silver. The decorated function receives raw bytes and returns a DataFrame or LazyFrame.
            </p>
            <CodeBlock
              class="mb-6"
              code="@dp.silver_transform(target=2, from_bronze=1)
def clean(raw: bytes) -> pl.LazyFrame:
    return pl.read_csv(raw).lazy().filter(pl.col(&quot;amount&quot;) > 0)

clean()            # uses latest bronze version
clean(version=5)   # uses a specific bronze version"
            />

            <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-2">
              gold_transform
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Transforms silver → gold. The decorated function receives a dict mapping silver source IDs to their LazyFrames.
            </p>
            <CodeBlock
              code="@dp.gold_transform(target=3, from_silver=[1, 2])
def aggregate(sources: dict[int, pl.LazyFrame]) -> pl.LazyFrame:
    return (
        pl.concat(sources.values())
        .group_by(&quot;category&quot;)
        .agg(pl.sum(&quot;amount&quot;))
    )

aggregate()"
            />
          </section>
        </div>
      </div>
    </div>
  </div>
</template>
