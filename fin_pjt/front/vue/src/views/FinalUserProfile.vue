<template>
  <div class="wrapper">
    <div class="profile-header">
      <h1>
        내 프로필
        <RouterLink :to="{ name: 'userprofile_edit' }" class="edit-btn">수정</RouterLink>
      </h1>
    </div>

    <div v-if="profile">
      <p class="userinfo"><strong>아이디:</strong> {{ profile.user }}</p>
      <p class="userinfo"><strong>닉네임:</strong> {{ profile.nickname }}</p>
      <p class="userinfo"><strong>이메일:</strong> {{ profile.email }}</p>
      <p class="userinfo"><strong>생년월일:</strong> {{ profile.birthdate }}</p>
      <p class="userinfo"><strong>자산:</strong> {{ profile.asset }}</p>
      <p class="userinfo"><strong>월급:</strong> {{ profile.salary }}</p>
    </div>
    <div v-else>
      <p>불러오는 중입니다...</p>
    </div>

    <hr>

    <h1 class="cart">내 관심 상품</h1>
    <section class="product-section">

      <h3>예금</h3>
      <div v-if="likedDepositProducts.length">
        <div
          v-for="item in likedDepositProducts"
          :key="item.fin_prdt_cd"
          class="product-line"
        >
          <span @click.prevent="goToDetail(item.fin_prdt_cd, 'deposit')">
            {{ item.fin_prdt_nm }} - {{ item.kor_co_nm }}
          </span>
          <button @click="toggleLike(item.fin_prdt_cd, 'deposit')">
            {{ profile.liked_deposits.includes(item.fin_prdt_cd) ? '🐾' : '🍚' }}
          </button>
        </div>
      </div>
      <p v-else>관심 등록한 예금 상품이 없습니다.</p>

      <div class="chart-wrapper">
        <canvas ref="depositChartRef"></canvas>
      </div>

      <h3 style="margin-top: 40px">적금</h3>
      <div v-if="likedSavingProducts.length">
        <div
          v-for="item in likedSavingProducts"
          :key="item.fin_prdt_cd"
          class="product-line"
        >
          <span @click.prevent="goToDetail(item.fin_prdt_cd, 'saving')">
            {{ item.fin_prdt_nm }} - {{ item.kor_co_nm }}
          </span>
          <button @click="toggleLike(item.fin_prdt_cd, 'saving')">
            {{ profile.liked_savings.includes(item.fin_prdt_cd) ? '🐾' : '🍚' }}
          </button>
        </div>
      </div>
      <p v-else>관심 등록한 적금 상품이 없습니다.</p>

      <div class="chart-wrapper">
        <canvas ref="savingChartRef"></canvas>
      </div>

    </section>
  </div>
</template>


<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import { useRouter } from 'vue-router'
import { Chart, BarElement, CategoryScale, LinearScale } from 'chart.js'

Chart.register(BarElement, CategoryScale, LinearScale)

const router = useRouter()
const accountStore = useAccountStore()
const token = accountStore.token

const profile = ref(null)
const deposits = ref([])
const savings = ref([])

const depositChartRef = ref(null)
const savingChartRef = ref(null)
const depositChartInstance = ref(null)
const savingChartInstance = ref(null)

onMounted(() => {
  axios.get('http://127.0.0.1:8000/api/v1/profile/my_profile/', { headers: { Authorization: 'Token ' + token } })
    .then(res => {
      profile.value = res.data
      // console.log('profile:', profile.value)
    })

  axios.get('http://127.0.0.1:8000/api/v2/deposits/')
    .then(res => {
      deposits.value = res.data
      // console.log('deposits:', deposits.value)
    })

  axios.get('http://127.0.0.1:8000/api/v2/savings/')
    .then(res => {
      savings.value = res.data
      console.log('savings:', savings.value)
    })
})

const likedDepositProducts = computed(() => {
  if (!profile.value) return []
  return profile.value.liked_deposits.map(code => deposits.value.find(d => d.fin_prdt_cd === code)).filter(Boolean)
})

const likedSavingProducts = computed(() => {
  if (!profile.value) return []
  return profile.value.liked_savings.map(code => savings.value.find(s => s.fin_prdt_cd === code)).filter(Boolean)
})

function drawChart(refEl, instanceRef, products, label, bgColor, borderColor) {
  if (!refEl.value) return
  if (instanceRef.value) {
    instanceRef.value.destroy()
    instanceRef.value = null
  }
  instanceRef.value = new Chart(refEl.value, {
    type: 'bar',
    data: {
      labels: products.map(p => p.fin_prdt_nm),
      datasets: [{ label, data: products.map(p => p.highest_rate || 0), backgroundColor: bgColor, borderColor, borderWidth: 1 }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: { y: { beginAtZero: true, ticks: { precision: 2, callback: v => v.toFixed(2) + '%' } } }
    }
  })
}

watch(likedDepositProducts, val => drawChart(depositChartRef, depositChartInstance, val, '예금 최고 금리(%)', 'rgba(30, 64, 175, 0.5)', '#1e3a8a'), { immediate: true })
watch(likedSavingProducts, val => drawChart(savingChartRef, savingChartInstance, val, '적금 최고 금리(%)', 'rgba(30, 64, 175, 0.7)', '#1E40AF'), { immediate: true })

function toggleLike(productCode, type) {
  const isDeposit = (type === 'deposit')
  const list = isDeposit ? profile.value.liked_deposits : profile.value.liked_savings
  const alreadyLiked = list.includes(productCode)
  const method = alreadyLiked ? 'delete' : 'post'
  axios({ method, url: `http://127.0.0.1:8000/api/v1/profile/like-${type}/${productCode}/`, headers: { Authorization: 'Token ' + token } })
    .then(() => {
      if (alreadyLiked) {
        if (isDeposit) profile.value.liked_deposits = list.filter(c => c !== productCode)
        else profile.value.liked_savings = list.filter(c => c !== productCode)
      } else {
        list.push(productCode)
      }
    })
}

function goToDetail(productCode, type) {
  router.push({ name: 'product-detail', params: { type, id: productCode } })
}
</script>

<style scoped>
.wrapper {
  max-width: 1000px;
  margin: 0 auto;
  font-family: 'Noto Sans KR', sans-serif;
  padding: 40px 24px;
  background-color: rgba(243, 243, 243, 0.928);
  min-height: 100vh;
  color: #1f2937; 
  font-size: 16px;
  line-height: 1.6;
}

.profile-header h1 {
  display: inline-flex;
  align-items: center;
  font-size: 28px;
  color: #1e293b; 
  gap: 12px;
  margin-bottom: 32px;
}

.edit-btn {
  font-size: 14px;
  color: #6b7280; 
  background-color: transparent;
  border: 1px solid #d1d5db; 
  padding: 4px 10px;
  border-radius: 6px;
  text-decoration: none;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.edit-btn:hover {
  background-color: #e2e8f0; 
  color: #374151; 
}

.userinfo {
  font-size: 17px;
  margin-bottom: 8px;
}

h1 {
  font-size: 28px;
  margin-bottom: 32px;
  color: #1e293b;
}

h3 {
  margin-top: 32px;
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 12px;
}

hr {
  margin: 40px 0;
  border: 0;
  border-top: 1px solid #0000005e;
}

.cart {
  margin-bottom: 40px;
}

.product-section {
  margin-bottom: 40px;
}

.product-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #ced0d3;
  font-size: 15px;
}

.product-line span {
  color: #334155; 
  cursor: pointer;
}

.product-line span:hover {
  text-decoration: underline;
}

button {
  background-color: transparent;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.chart-wrapper {
  background-color: #ffffff;
  border: 1px solid #cbd5e1; 
  border-radius: 10px;
  padding: 24px;
  margin: 24px 0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

canvas {
  width: 100% !important;
  height: 280px !important; 
}
</style>
