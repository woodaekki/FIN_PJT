<template>
  <div class="product-page">
    <h1 class="banner-copy">예적금 찾기 페이지</h1>

    <aside class="filter-section">
      <h3>금융 상품 필터</h3>
      <hr />
      <div class="filter-group padded-group">
        <label>
          <input type="radio" name="productType" value="all" v-model="productType" class="radio-box" />
          전체 보기
        </label>
        <label>
          <input type="radio" name="productType" value="deposit" v-model="productType" class="radio-box" />
          예금
        </label>
        <label>
          <input type="radio" name="productType" value="saving" v-model="productType" class="radio-box" />
          적금
        </label>
      </div>
      <hr />
      <div class="bank-filter">
        <button
          v-for="bank in uniqueBanks"
          :key="bank"
          @click="toggleBank(bank)"
          :class="['bank-button', { active: selectedBanks.includes(bank) }]"
        >
          {{ bank }}
        </button>
      </div>
    </aside>

    <section class="result-section">
      <div v-if="productType === 'all' || productType === 'deposit'">
        <h3 class="product-top">예금 상품</h3>
        <div class="product-list" v-for="deposit in filteredDeposits" :key="deposit.fin_prdt_cd">
          <div
            class="product-info"
            @click="$router.push({ name: 'product-detail', params: { type: 'deposit', id: deposit.fin_prdt_cd } })"
          >
            <strong>{{ deposit.fin_prdt_nm }}</strong>
            <span class="company">{{ deposit.kor_co_nm }}</span>
            <span class="rate">
              최고 금리: {{ deposit.highest_rate !== null ? deposit.highest_rate + '%' : '정보 없음' }}
            </span>
          </div>
          <div class="product-actions">
            <button class="heart-btn" @click.stop="toggleLike(deposit.fin_prdt_cd, 'deposit')">
              {{ isLiked(deposit.fin_prdt_cd, 'deposit') ? '♥' : '♡' }}
            </button>
          </div>
        </div>
      </div>

      <hr class="line" />

      <div v-if="productType === 'all' || productType === 'saving'">
        <h3 class="product-bottom">적금 상품</h3>
        <div class="product-list" v-for="saving in filteredSavings" :key="saving.fin_prdt_cd">
          <div
            class="product-info"
            @click="$router.push({ name: 'product-detail', params: { type: 'saving', id: saving.fin_prdt_cd } })"
          >
            <strong>{{ saving.fin_prdt_nm }}</strong>
            <span class="company">{{ saving.kor_co_nm }}</span>
            <span class="rate">
              최고 금리: {{ saving.highest_rate !== null ? saving.highest_rate + '%' : '정보 없음' }}
            </span>
          </div>
          <div class="product-actions">
            <button class="heart-btn" @click.stop="toggleLike(saving.fin_prdt_cd, 'saving')">
              {{ isLiked(saving.fin_prdt_cd, 'saving') ? '♥' : '♡' }}
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()
const token = accountStore.token

// 1. 상태 변수 선언
const deposits = ref([])
const savings = ref([])
const selectedBanks = ref([])
const likedDeposits = ref([])
const likedSavings = ref([])
const productType = ref('all')

onMounted(() => {
  const API_URL = 'http://127.0.0.1:8000/api/v2'

  // 2. 예금, 적금, 좋아요 데이터 호출
  axios({
    method: 'get',
    url: `${API_URL}/deposits/`
  })
  .then(res => {
    deposits.value = res.data
    return axios({ method: 'get', url: `${API_URL}/savings/` })
  })
  .then(res => {
    savings.value = res.data
    return axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/profile/my_profile/',
      headers: { Authorization: `Token ${token}` }
    })
  })
  .then(res => {
    likedDeposits.value = res.data.liked_deposits || []
    likedSavings.value = res.data.liked_savings || []
  })
  .catch(() => {
    alert('데이터 요청 실패')
  })
})

// 3. 중복 없이 은행 목록 생성
const uniqueBanks = computed(() => {
  const bankSet = new Set([
    ...deposits.value.map(d => d.kor_co_nm),
    ...savings.value.map(s => s.kor_co_nm)
  ])
  return Array.from(bankSet).sort((a, b) => a.localeCompare(b, 'ko'))
})

// 4. 은행 필터 토글
function toggleBank(bank) {
  const idx = selectedBanks.value.indexOf(bank)
  idx >= 0
    ? selectedBanks.value.splice(idx, 1)
    : selectedBanks.value.push(bank)
}

// 5. 선택된 은행 기준으로 필터링
const filteredDeposits = computed(() =>
  selectedBanks.value.length === 0
    ? deposits.value
    : deposits.value.filter(d => selectedBanks.value.includes(d.kor_co_nm))
)

const filteredSavings = computed(() =>
  selectedBanks.value.length === 0
    ? savings.value
    : savings.value.filter(s => selectedBanks.value.includes(s.kor_co_nm))
)

// 6. 좋아요 상태 확인 및 토글
const isLiked = (code, type) =>
  type === 'deposit'
    ? likedDeposits.value.includes(code)
    : likedSavings.value.includes(code)

function toggleLike(code, type) {
  const likedAlready = isLiked(code, type)
  const method = likedAlready ? 'delete' : 'post'
  const url = `http://127.0.0.1:8000/api/v1/profile/like-${ type === 'saving' ? 'saving' : type }/${code}/`
  axios({
    method,
    url,
    headers: { Authorization: `Token ${token}` }
  })
  .then(() => {
    const listRef = type === 'deposit' ? likedDeposits : likedSavings
    likedAlready
      ? (listRef.value = listRef.value.filter(p => p !== code))
      : listRef.value.push(code)
  })
  .catch(() => {
    alert('관심상품 처리 중 오류')
  })
}
</script>



<style scoped>
.product-page {
  padding: 32px 24px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Noto Sans KR', sans-serif;
  color: #1f2937;
  background-color: rgba(233, 233, 233, 0.832);
}

.banner-copy {
  font-size: 26px;
  font-weight: 600;
  color: black;
  text-align: left;
  border-left: 5px solid #38b2ac;
  padding-left: 6px;
  margin: auto;
  margin-top: 15px;
  margin-bottom: 20px;
  max-width: 1200px;
  box-sizing: border-box; 
  text-indent: 4px; 
}

h3 {
  font-family: 'KakaoSmallSans-Bold';
  font-size: 25px;
}

.cta-section {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto 24px auto;
  padding: 0 24px; 
}

.cta-link {
  display: inline-block;
  background-color: #38b2ac;
  color: white;
  font-size: 18px;
  font-weight: bold;
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.cta-link:hover {
  background-color: #319795;
}

.rate {
  font-size: 15px;
  font-weight: 600;
  color: #374151; 
  background-color: #e1e1e2; 
  margin-top: 10px;
  padding: 4px 8px;
  border-radius: 6px;
  display: inline-block;
}

.filter-section {
  background-color: #ffffff;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  margin-bottom: 40px;  
}

.filter-group {
  display: flex;
  gap: 20px; 
  flex-wrap: wrap; 
}

.filter-group label {
  font-size: 16px;
  color: #4a4a4a;
  display: flex;
  align-items: center; 
}

.filter-group input[type="radio"] {
  margin-right: 10px;  
}

.bank-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 20px;
}

.bank-button {
  background-color: #f3f4f6;
  border: 1px solid #a09e9ec0;
  border-radius: 30px;  
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.bank-button:hover {
  background-color: #2563eb;
  border-color: #2563eb;
  color: white;
}

.bank-button.active {
  background-color: #2563eb;
  color: white;
  border-color: #2563eb;
}

.detail-link {
  font-size: 14px;
  color: #2563eb; 
  font-weight: 500;
  text-decoration: underline;
  transition: color 0.2s ease;
}

.detail-link:hover {
  color: #1e3a8a;  
}

.padded-group {
  padding: 0 25px;
}

.line {
  color: lightgray;
}

.heart-btn {
  font-size: 18px;
  background-color: white;
  border: 1px solid #d1d5db;
  color: #ef4444;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.1s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  margin-left: 8px;
  margin-top: -24px;
}

.heart-btn:hover {
  background-color: #fee2e2;
  transform: scale(1.05);
}

.heart-btn:active {
  background-color: #fecaca;
  transform: scale(0.95);
}

.result-section {
  margin-top: 48px;
}

.product-list {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  margin-bottom: 16px;
  background-color: #ffffff;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
  transition: background-color 0.2s ease;
}

.product-list:hover {
  background-color: #f3f4f6;
}

.product-info {
  display: flex;
  flex-direction: column;
  cursor: pointer;
  flex: 1;
}

.product-info strong {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
}

.product-info .company,
.rate {
  font-size: 14px;
  color: #6b7280;
}

.product-actions {
  display: flex;
  align-items: center;
  margin-left: 20px;
  white-space: nowrap;
}
</style>
