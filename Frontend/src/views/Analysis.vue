<template>
  <div class="flex min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    <Sidebar :isOpen="isOpen" @close="isOpen = false" />

    <div class="flex-1 flex flex-col md:ml-64">
      <Navbar @toggle-sidebar="isOpen = !isOpen" />

      <!-- Content -->
      <main class="w-full py-8 px-4 sm:px-6 lg:px-8">
        <div class="space-y-8 max-w-6xl ml-4">
          <!-- Header -->
          <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Product Analysis</h1>
            <p class="mt-2 text-gray-600 dark:text-gray-400">Analyze product performance and trends</p>
          </div>

          <!-- Analysis Content -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
            <div class="p-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Sales and orders Chart -->
                <div class="flex flex-col gap-6">
                  <div class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow">
                    <h3 class="text-lg font-semibold mb-4">Total Sales</h3>
                    <canvas id="totalSalesChart"></canvas>
                  </div>
                  <div class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow">
                    <h3 class="text-lg font-semibold mb-4">Number of Orders</h3>
                    <canvas id="ordersChart"></canvas>
                  </div>
                </div>

                <!-- Product wise sales and monthy growth Chart -->
                <div class="flex flex-col gap-6">
                  <div class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow">
                    <h3 class="text-lg font-semibold mb-4">Product-wise Sales (2025)</h3>
                    <canvas id="productSalesChart"></canvas>
                  </div>
                  <div class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow">
                    <h3 class="text-lg font-semibold mb-4">Monthly Growth</h3>
                    <canvas id="monthlyGrowthChart"></canvas>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { Chart, registerables } from "chart.js"
Chart.register(...registerables)
import Sidebar from '@/components/Sidebar.vue'
import Navbar from '@/components/Navbar.vue'
import { useApi } from '@/composables/useApi'

let totalSalesChart: Chart | null = null
let productSalesChart: Chart | null = null
let monthlyGrowthChart: Chart | null = null
let ordersChart: Chart | null = null

const api = useApi()

onMounted(async () => {
  let analytics: any[] = []
  try { analytics = await api.get<any[]>(`/analysis/products`) } catch (e) { analytics = [] }

  // Chart 1 — Total Sales for 3 years
  const ctx1 = document.getElementById("totalSalesChart") as HTMLCanvasElement
  const salesByYear: Record<string, number> = {}
  analytics.forEach(a => { salesByYear[a.year] = (salesByYear[a.year] || 0) + (a.monthly_revenue || 0) })
  const labels1 = Object.keys(salesByYear).sort()
  totalSalesChart = new Chart(ctx1, {
    type: "line",
    data: {
      labels: labels1,
      datasets: [
        {
          label: "Total Sales (₹ in Lakhs)",
          data: labels1.map(y => Math.round((salesByYear[y] || 0) / 100000)),
          borderColor: "#3b82f6",
          backgroundColor: "rgba(59,130,246,0.2)",
          fill: true,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: { enabled: true },
        legend: { position: "top" }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  })

  // Chart 2 — Number of Orders
  const ctx2 = document.getElementById("ordersChart") as HTMLCanvasElement
  const ordersByYear: Record<string, number> = {}
  analytics.forEach(a => { ordersByYear[a.year] = (ordersByYear[a.year] || 0) + (a.total_orders || 0) })
  const labels2 = Object.keys(ordersByYear).sort()
  ordersChart = new Chart(ctx2, {
    type: "bar",
    data: {
      labels: labels2,
      datasets: [
        {
          label: "Orders (in Thousands)",
          data: labels2.map(y => Math.round((ordersByYear[y] || 0) / 1000)),
          backgroundColor: "#f59e0b",
          borderRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        tooltip: {
          callbacks: {
            label: function (context: any) {
              const val = context.parsed?.y ?? 0
              return `${val}k Orders`
            }
          }
        }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  })

  // Chart 3 — Product-wise Sales (2025)
  const ctx3 = document.getElementById("productSalesChart") as HTMLCanvasElement
  const byProduct: Record<string, number> = {}
  analytics.forEach(a => { byProduct[a.product_id] = (byProduct[a.product_id] || 0) + (a.monthly_revenue || 0) })
  const prodLabels = Object.keys(byProduct).slice(0, 5).map(id => `#${id}`)
  const prodData = Object.keys(byProduct).slice(0, 5).map(id => byProduct[id])
  productSalesChart = new Chart(ctx3, {
    type: "bar",
    data: {
      labels: prodLabels,
      datasets: [
        {
          label: "Sales (₹)",
          data: prodData,
          backgroundColor: [
            "#3b82f6",
            "#10b981",
            "#f59e0b",
            "#ef4444",
            "#8b5cf6"
          ]
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  })

  // Chart 4 — Monthly Growth (hover shows growth %)
  const ctx4 = document.getElementById("monthlyGrowthChart") as HTMLCanvasElement
  const monthlySales: number[] = Array(12).fill(0)
  analytics.filter(a => a.year === (new Date()).getFullYear()).forEach(a => { const m = (a.month||1)-1; monthlySales[m] += a.monthly_revenue||0 })
  const growth = monthlySales.map((val, i) =>
    i === 0 ? 0 : (((val - monthlySales[i - 1]) / monthlySales[i - 1]) * 100).toFixed(1)
  )

  monthlyGrowthChart = new Chart(ctx4, {
    type: "line",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      datasets: [
        {
          label: "Monthly Sales (₹)",
          data: monthlySales,
          borderColor: "#10b981",
          backgroundColor: "rgba(16,185,129,0.2)",
          fill: true,
          tension: 0.4
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          callbacks: {
            label: function (context: any) {
              const idx = context.dataIndex
              const yValue = context.parsed?.y ?? 0;
              return `₹${yValue.toLocaleString()} (${growth[idx]}%)`;
            }
          }
        },
        legend: { position: "top" }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  })
})

onBeforeUnmount(() => {
  totalSalesChart?.destroy()
  ordersChart?.destroy()
  productSalesChart?.destroy()
  monthlyGrowthChart?.destroy()
})

const isOpen = ref(false)
</script>
