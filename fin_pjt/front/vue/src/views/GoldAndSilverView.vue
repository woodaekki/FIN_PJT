<template>
  <div class="container">
    <nav class="banner-img-box">
      <img src="../assets/gold_silver_banner.png" alt="배너 이미지">
    </nav>

    <h1 class="price">{{ title }} 시세</h1>

    <div class="tab">
      <button @click="type = 'gold'" :class="{ active: type === 'gold' }">금</button>
      <button @click="type = 'silver'" :class="{ active: type === 'silver' }">은</button>
    </div>

    <div class="date-picker">
      <label>시작일</label>
      <input type="date" v-model="startDate" />
      <label>종료일</label>
      <input type="date" v-model="endDate" />
    </div>

    <div v-if="chartDataAvailable" class="chart-container">
      <Line :data="chart" :options="option" />
    </div>
    <div v-else>
      <p>선택된 조건에 해당하는 데이터가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useGoldSilverStore } from '@/stores/goldSilver'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const store = useGoldSilverStore()
store.getGoldAndSilverPrices()

const type = ref('gold')
const startDate = ref('2023-01-01')
const endDate = ref('2023-06-30')

const title = computed(() => (type.value === 'gold' ? '금' : '은'))

const chartDataAvailable = computed(() => {
  return store.labels.some(d => d >= startDate.value && d <= endDate.value)
})

const chart = computed(() => {
  const x = []
  const y = []
  for (let i = 0; i < store.labels.length; i++) {
    const d = store.labels[i]
    if (d >= startDate.value && d <= endDate.value) {
      x.push(d.slice(0, 10))
      y.push(type.value === 'gold' ? store.goldPrices[i] : store.silverPrices[i])
    }
  }
  return {
    labels: x,
    datasets: [{
      label: title.value + ' 시세',
      data: y,
      borderWidth: 2,
      borderColor: type.value === 'gold' ? '#f1c40f' : '#95a5a6',
      tension: 0.3
    }]
  }
})

const option = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        font: {
          size: 12
        }
      }
    }
  },
  scales: {
    x: {
      title: {
        display: true,
        text: '날짜'
      }
    },
    y: {
      title: {
        display: true,
        text: '가격 (USD)'
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
  box-sizing: border-box;
}

.banner-img-box {
  width: 100%;
  overflow: hidden;
  position: relative;
}

.banner-img-box img {
  width: 100%;
  height: auto;
  object-fit: contain;
  display: block;
}

.price {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  padding-left: 10px;
  border-left: 4px solid #38b2ac;
  margin-top: 24px;
  margin-bottom: 20px;
  font-family: 'WooridaumB', sans-serif;
}

.tab {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.tab button {
  padding: 8px 16px;
  font-size: 14px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.2s ease-in-out;
}

.tab button:hover {
  background: #f0f0f0;
}

.tab button.active {
  background: #333;
  color: white;
  border-color: #333;
}

.date-picker {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 20px;
  align-items: center;
}

.date-picker label {
  font-size: 14px;
  font-weight: 500;
}

.date-picker input {
  padding: 6px 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background-color: white;
  min-width: 140px;
}

.chart-container {
  background: white;
  padding: 12px;
  width: 100%;
  box-sizing: border-box;
  min-height: 300px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

canvas {
  width: 100% !important;
  height: auto !important;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .container {
    padding: 16px;
  }

  .price {
    font-size: 20px;
  }

  .tab {
    flex-wrap: wrap;
    gap: 8px;
  }

  .tab button {
    font-size: 13px;
    padding: 6px 12px;
    flex: 1 1 45%;
  }

  .date-picker {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }

  .date-picker input {
    width: 100%;
    min-width: unset;
  }

  .chart-container {
    height: 260px;
    padding: 10px;
  }

  canvas {
    height: 100% !important;
  }
}
</style>
