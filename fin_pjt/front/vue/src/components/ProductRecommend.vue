<template>
  <div class="container">
    <div class="banner-box">
      <div class="banner-img-box">
        <img src="../assets/products_banner.png" alt="예적금 배너" />
      </div>
    </div>

    <div class="cta-container">
      <RouterLink :to="{ name: 'product' }" class="cta-link">
        상품 목록 보러가기
      </RouterLink>
    </div>

    <div class="section-title">
      <h1>맞춤상품 추천</h1>
    </div>

    <section class="filter-section">
      <h2 class="text">정보 입력</h2>
      <p class="mini-text">고객님의 정보를 입력해주세요.</p>
      <hr />
      <div class="filter-group">
        <label>
          <input type="radio" name="productType" value="all" v-model="productType" /> 전체 보기
        </label>
        <label>
          <input type="radio" name="productType" value="deposit" v-model="productType" /> 예금만 보기
        </label>
        <label>
          <input type="radio" name="productType" value="saving" v-model="productType" /> 적금만 보기
        </label>
        <button class="recommend-btn" @click="onClickFetchRecommendations">추천받기</button>
      </div>
      <hr />

      <div class="search-filter">
        <div class="filter-item">
          <h4 class="text">나이 검색</h4>
          <select v-model="selectedAgeGroup">
            <option value=""> 선택 안함 </option>
            <option value="20s">20대 이하</option>
            <option value="30s">30대</option>
            <option value="40s">40대</option>
            <option value="50s">50대</option>
            <option value="60s">60대</option>
            <option value="70s">70대</option>
            <option value="80plus">80대 이상</option>
          </select>
        </div>

        <div class="filter-item">
          <h4 class="text">지역 검색</h4>
          <select v-model="selectedProvince">
            <option value="">선택 안함</option>
            <option v-for="province in provinces" :key="province" :value="province">{{ province }}</option>
          </select>
        </div>

        <div class="filter-item">
          <h4 class="text">직군 정렬</h4>
          <select v-model="selectedJob">
            <option v-for="job in jobs" :key="job" :value="job">{{ job }}</option>
          </select>
        </div>

        <div class="filter-item">
          <h4 class="text">소득 선택 </h4>
          <select v-model="selectedIncome">
            <option v-for="range in incomeRanges" :key="range.value" :value="range.value">{{ range.label }}</option>
          </select>
          <p class="mini-text">(*세전 월급 입력하세요)</p>
        </div>
      </div>
      <hr>

      <section v-if="showResults" class="result-section">
        <h3 class="product-top">예금 추천</h3>
        <div v-if="filteredDeposits.length === 0" class="product-list">찾으시는 상품이 없습니다.</div>
        <div class="product-list" v-for="deposit in filteredDeposits" :key="deposit.product_name">
          <div class="product-info" @click="onClickProduct(deposit.product_name, 'deposit')">
            <strong>{{ deposit.product_name }}</strong>
            <span class="company">{{ deposit.bank_name }} — <b>{{ deposit.count }}명 사용</b></span>
          </div>
          <button class="heart-btn" @click.stop="onClickToggleLike(deposit.product_name, 'deposit')">
            {{ likedDeposits.includes(deposit.product_name) ? '♥' : '♡' }}
          </button>
        </div>

        <h3 class="product-bottom">적금 추천</h3>
        <div v-if="filteredSavings.length === 0" class="product-list">찾으시는 상품이 없습니다.</div>
        <div class="product-list" v-for="saving in filteredSavings" :key="saving.product_name">
          <div class="product-info" @click="onClickProduct(saving.product_name, 'saving')">
            <strong>{{ saving.product_name }}</strong>
            <span class="company">{{ saving.bank_name }} — <b>{{ saving.count }}명 사용</b></span>
          </div>
          <button class="heart-btn" @click.stop="onClickToggleLike(saving.product_name, 'saving')">
            {{ likedSavings.includes(saving.product_name) ? '♥' : '♡' }}
          </button>
        </div>
      </section>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import { useRouter } from 'vue-router'

const router = useRouter()
const accountStore = useAccountStore()
const token = accountStore.token

const selectedAgeGroup = ref('')
const selectedProvince = ref('')
const selectedJob = ref('선택 안함')
const selectedIncome = ref(0)
const productType = ref('all')
const provinces = ref([])
const jobs = ref([])
const incomeRanges = ref([])

const recommendations = ref({ deposits: [], savings: [] })
const likedDeposits = ref([])
const likedSavings = ref([])

const showResults = ref(false)

onMounted(() => {
  axios.get('/districts_by_province.json')
    .then(res1 => {
      provinces.value = Object.keys(res1.data)

      axios.get('/jobs.json')
        .then(res2 => {
          jobs.value = res2.data
          axios.get('/income_ranges.json')
            .then(res3 => {
              incomeRanges.value = res3.data
              axios.get('http://127.0.0.1:8000/api/v1/profile/my_profile/', {
                headers: { Authorization: `Token ${token}` }
              })
                .then(res4 => {
                  likedDeposits.value = res4.data.liked_deposits || []
                  likedSavings.value = res4.data.liked_savings || []
                })
            }) 
        })  
    })
})

const onClickFetchRecommendations = () => {
  axios.get('http://127.0.0.1:8000/api/v6/recommend/', {
    params: {
      age_group: selectedAgeGroup.value,
      income: selectedIncome.value,
      job: selectedJob.value,
      city: selectedProvince.value
    }
  })
    .then(res => {
      recommendations.value = res.data
      showResults.value = true
    })
}

const filteredDeposits = computed(() => {
  if (productType.value === 'saving') return []
  return recommendations.value.deposits || []
})

const filteredSavings = computed(() => {
  if (productType.value === 'deposit') return []
  return recommendations.value.savings || []
})

const onClickToggleLike = (productName, type) => {
  const list = type === 'deposit' ? likedDeposits : likedSavings
  const alreadyLiked = list.value.includes(productName)
  const method = alreadyLiked ? 'delete' : 'post'

  axios({
    method,
    url: `http://127.0.0.1:8000/api/v1/profile/like-${type}/${productName}/`,
    headers: { Authorization: `Token ${token}` }
  })
    .then(() => {
      if (alreadyLiked) {
        list.value = list.value.filter(p => p !== productName)
      } else {
        list.value.push(productName)
      }
    })
}

const onClickProduct = (productName, type) => {
  axios.get('http://127.0.0.1:8000/api/v2/get-product-code/', {
    params: {
      product_name: productName,
      type: type
    }
  })
    .then(res => {
      const code = Array.isArray(res.data) && res.data.length > 0 ? res.data[0] : null
      if (!code) return
      router.push({ name: 'product-detail', params: { type, id: code } })
    })
}
</script>

<style scoped>
.container {
  max-width: 1000px;
  min-height: 100vh;
  margin: 0 auto;
  padding: 24px 24px;
  background-color: rgba(244, 244, 244, 0.832);
}

.banner-box {
  width: 100%;
  background-color: #e8edf5;
  padding-top: 40px;
}

.banner-img-box {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 0 12px;
}

.banner-img-box img {
  max-width: 1200px;
  height: auto;
  display: block;
  border-radius: 12px;
  margin-bottom: 40px;
}

.text {
  font-family: 'KakaoSmallSans-Bold';
  font-size: 20px;
}

.mini-text {
  font-size: 13px;
  color: #9ca3af; 
}

.cta-container {
  margin-top: 16px;
  text-align: right;
  margin-bottom: 16px;
}

.section-title {
  font-size: 24px;
  font-weight: 700;
}

.cta-link {
  display: inline-block;
  padding: 10px 20px;
  background-color: #64748b;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.cta-link:hover {
  background-color: #475569;
}

.filter-section {
  background-color: #ffffff;
  padding: 24px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  margin-bottom: 40px;
}

.filter-section h2 {
  margin-bottom: 8px;
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 20px 32px;
  align-items: center;
  margin-bottom: 18px;
  padding: 5px 0;
}

.filter-group label {
  display: flex;
  align-items: center;
  font-size: 15px;
  gap: 8px;
  padding: 5px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.filter-group label:hover {
  background-color: #e5e7eb;
}

.filter-group input[type="radio"] {
  margin: 0;
}

.recommend-btn {
  padding: 10px 18px;
  background-color: #64748b;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-left: auto;
}

.recommend-btn:hover {
  background-color: #475569;
}

.recommend-btn:active {
  background-color: #334155;
}

.search-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  margin-bottom: 16px;
}

.filter-item {
  flex: 1 1 220px;
  min-width: 200px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.filter-item h4 {
  margin-bottom: 0;
}

.filter-item .mini-text {
  font-size: 13px;
  color: #9ca3af;
  margin-top: 4px;
}

.result-section {
  margin-top: 32px;
}

.product-top,
.product-bottom {
  margin: 32px 0 16px;
  font-size: 20px;
  font-weight: bold;
}

.result-section > .product-list:first-of-type {
  margin-top: 0;
}

.result-section > .product-list:last-of-type {
  margin-bottom: 32px;
}

.result-section > .product-list:only-of-type {
  margin: 12px 0 24px;
}

.product-list {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  margin-bottom: 16px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
  transition: box-shadow 0.2s ease, background-color 0.2s ease;
}

.product-list:hover {
  background-color: #f9fafb;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
}

.product-list:active {
  background-color: #e5e7eb;
}

.product-info {
  display: flex;
  flex-direction: column;
}

.product-info strong {
  font-size: 16px;
  color: #111827;
}

.product-info .company {
  font-size: 13px;
  color: #6b7280;
  margin-top: 4px;
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
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.heart-btn:hover {
  background-color: #fee2e2;
  transform: scale(1.05);
}

.heart-btn:active {
  background-color: #fecaca;
  transform: scale(0.95);
}


@media (max-width: 1024px) {
  .product-page {
    padding: 80px 16px;
  }

  .banner-img-box img {
    width: 100%;
    max-width: 100%;
    height: auto;
  }

  .section-title {
    font-size: 20px;
  }
}

@media (max-width: 768px) {
  .product-page {
    padding: 60px 12px;
  }

  .section-title h1 {
    font-size: 18px;
  }

  .cta-container {
    text-align: center;
  }

  .cta-link {
    width: 100%;
    text-align: center;
    font-size: 15px;
    padding: 10px;
  }

  .filter-section {
    padding: 16px;
  }

  .filter-group {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .search-filter {
    flex-direction: column;
    gap: 16px;
  }

  .filter-item {
    width: 100%;
  }

  .recommend-btn {
    width: 100%;
    padding: 12px;
    font-size: 16px;
    margin-left: 0;
    align-self: flex-end;
  }

  .product-list {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    padding: 16px;
  }

  .product-info strong {
    font-size: 15px;
  }

  .product-info .company {
    font-size: 12px;
  }

  .heart-btn {
    align-self: flex-end;
    font-size: 16px;
    width: 32px;
    height: 32px;
  }

  .product-top,
  .product-bottom {
    font-size: 18px;
  }
}
</style>

