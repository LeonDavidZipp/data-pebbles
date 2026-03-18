<script setup lang="ts">
const sections = [
  { id: 'installation', label: 'Installation' },
  { id: 'quickstart', label: 'Quick Start' },
  { id: 'projects', label: 'Projects' },
  { id: 'bronze', label: 'Bronze Layer' },
  { id: 'silver', label: 'Silver Layer' },
  { id: 'gold', label: 'Gold Layer' },
  { id: 'transforms', label: 'Transform Decorators' }
]

const activeSection = ref('installation')
const scrollContainer = ref<HTMLElement>()
let isScrolling = false

function scrollTo(id: string) {
  isScrolling = true
  activeSection.value = id
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
  setTimeout(() => {
    isScrolling = false
  }, 800)
}

onMounted(() => {
  const container = scrollContainer.value
  if (!container) return

  const observer = new IntersectionObserver(
    (entries) => {
      if (isScrolling) return
      for (const entry of entries) {
        if (entry.isIntersecting) {
          activeSection.value = entry.target.id
        }
      }
    },
    { root: container, rootMargin: '0px 0px -60% 0px', threshold: 0 }
  )

  for (const s of sections) {
    const el = document.getElementById(s.id)
    if (el) observer.observe(el)
  }

  onUnmounted(() => observer.disconnect())
})
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
      <div
        ref="scrollContainer"
        class="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-950 p-6 lg:p-10"
      >
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

          <!-- Projects -->
          <section id="projects">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              Projects
            </h2>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
              Projects group related resources (bronze/silver/gold). Use the `projects` layer in the SDK to create and manage projects.
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
                      create_project(name, description=None)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Create a new project
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_projects()
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all projects
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      get_project(project_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Get project metadata
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      update_project(project_id, name=None, description=None)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Update project fields
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      delete_project(project_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Delete a project
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
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

# Projects: create and list projects
dp.projects.create_project(&quot;analytics&quot;, description=&quot;Analytics workspace&quot;)
projects = dp.projects.list_projects()

# Bronze: create a resource in a project and upload (.csv, .parquet, .json, .xlsx)
dp.bronze.create_resource(&quot;raw_sales&quot;, project_id=projects[0].id)
dp.bronze.upload(projects[0].id, file_path=&quot;sales.csv&quot;)

# Silver / Gold examples
dp.silver.create_resource(&quot;clean_sales&quot;, project_id=projects[0].id)
dp.gold.create_resource(&quot;sales_summary&quot;, project_id=projects[0].id)"
            />
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-3">
              The client can also be used as a context manager:
            </p>
            <CodeBlock
              code="with DataPebbles(&quot;http://localhost:8000&quot;) as dp:
    resources = dp.bronze.list_resources()"
            />
          </section>

          <!-- Bronze Layer -->
          <section id="bronze">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              Bronze Layer
            </h2>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
              The bronze layer stores raw, unprocessed files. Only <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded">.csv</code>, <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded">.parquet</code>, <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded">.json</code>, and <code class="text-xs bg-gray-200 dark:bg-gray-800 px-1.5 py-0.5 rounded">.xlsx</code> files are accepted.
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
                      create_resource(name)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Create a new bronze resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_resources()
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all bronze resources
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      get_resource(resource_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Get metadata for a resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      update_resource(resource_id, name)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Rename a resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      delete_resource(resource_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Delete a resource and all its versions
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_versions(resource_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all versions of a resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      upload(resource_id, *, file_path=None, data=None, file_name=&quot;upload&quot;)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Upload a file by path or raw bytes (.csv, .parquet, .json, .xlsx)
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      download(resource_id, *, version=None)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Download raw bytes (latest version by default)
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      activate_version(resource_id, version)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Set a version as active
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      delete_version(resource_id, version)
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
                      create_resource(name)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Create a new silver resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_resources()
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all silver resources
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      get_resource(resource_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Get metadata for a resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      update_resource(resource_id, name)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Rename a resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      delete_resource(resource_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Delete a resource and all its versions
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_versions(resource_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all versions with lineage info
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      upload(resource_id, data, *, from_resource_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Upload a DataFrame/LazyFrame with bronze lineage
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      download(resource_id, *, version=None)
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
                      create_resource(name)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Create a new gold resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_resources()
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all gold resources
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      get_resource(resource_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Get metadata for a resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      update_resource(resource_id, name)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Rename a resource
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      delete_resource(resource_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Delete a resource and all its versions
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      list_versions(resource_id)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      List all versions with lineage info
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      upload(resource_id, data, *, from_resource_ids)
                    </td>
                    <td class="py-2 px-4 text-gray-600 dark:text-gray-400">
                      Upload a DataFrame/LazyFrame with silver lineage
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 font-mono text-xs text-gray-900 dark:text-white">
                      download(resource_id, *, version=None)
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
              Transforms bronze → silver. The decorator auto-parses bronze data into a LazyFrame based on the file extension. The decorated function receives a LazyFrame and returns a LazyFrame.
            </p>
            <CodeBlock
              class="mb-3"
              code="@dp.silver_transform(target_id=2, from_bronze_id=1)
def clean(lf: pl.LazyFrame) -> pl.LazyFrame:
    return lf.filter(pl.col(&quot;amount&quot;) > 0)

clean()            # uses latest bronze version
clean(version=5)   # uses a specific bronze version"
            />
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              For CSV files with a non-standard delimiter:
            </p>
            <CodeBlock
              class="mb-6"
              code="@dp.silver_transform(target_id=2, from_bronze_id=1, csv_separator=&quot;;&quot;)
def clean_eu(lf: pl.LazyFrame) -> pl.LazyFrame:
    return lf.filter(pl.col(&quot;amount&quot;) > 0)"
            />

            <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-2">
              gold_transform
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Transforms silver → gold. The decorated function receives a dict mapping silver resource IDs to their LazyFrames and returns a LazyFrame.
            </p>
            <CodeBlock
              code="@dp.gold_transform(target_id=3, from_silver_ids=[1, 2])
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
