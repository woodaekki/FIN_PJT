<template>
  <div class="container">
    <div class="page-background">
      <h1 class="page-title">예적금 상품 안내</h1>

      <div class="product-wrapper" v-if="product">
        <div class="product-card">
          <div class="header">
            <div class="name-box">
              <h2>{{ product.fin_prdt_nm }}</h2>
              <p class="bank-name">{{ product.kor_co_nm }}</p>
            </div>
            <div class="rate-box">
              <span class="rate-label">최고 연</span>
              <span class="rate-value">{{ product.highest_rate }}%</span>
              <div class="like-box-inline">
                <button class="like-button" @click="toggleLike">
                  {{ isLiked ? '♥ 관심 해제' : '♡ 관심 상품' }}
                </button>
              </div>
            </div>
          </div>

          <ul class="info-list">
            <li><strong>가입 방법</strong> | {{ product.join_way }}</li>
            <li><strong>우대 조건</strong> | {{ product.spcl_cnd }}</li>
            <li><strong>가입 대상</strong> | {{ product.join_member }}</li>
            <li><strong>최대 가입 한도</strong> | {{ Number(product.max_limit).toLocaleString() }}원</li>
            <li><strong>만기 후 이자율</strong> | {{ product.mtrt_int }}</li>
            <li><strong>기타</strong> {{ product.etc_note }}</li>
          </ul>

          <div v-if="options.length" class="option-section">
            <h3 class="option-title">금리 옵션 정보</h3>
            <div class="table-wrapper">
              <table class="option-table">
                <thead>
                  <tr>
                    <th>저축 기간 (개월)</th>
                    <th>금리 유형</th>
                    <th>기본 금리</th>
                    <th>최고 금리</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="opt in options" :key="opt.id">
                    <td>{{ opt.save_trm }}개월</td>
                    <td>{{ opt.intr_rate_type_nm }}</td>
                    <td>{{ opt.intr_rate }}%</td>
                    <td>{{ opt.intr_rate2 }}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="router-links">
            <RouterLink :to="{ name: 'article' }">상품 Q&A</RouterLink>
            <RouterLink :to="{ name: 'product' }">목록으로</RouterLink>
          </div>
        </div>
      </div>

      <div v-else>
        <p>불러오는 중...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const props = defineProps(['type', 'id'])

const product = ref(null)
const options = ref([])
const isLiked = ref(false)

const accountStore = useAccountStore()
const token = accountStore.token

onMounted(() => {
  const endpointType = props.type === 'deposit' ? 'deposits' : 'savings'
  const productUrl = `http://127.0.0.1:8000/api/v2/${endpointType}/${props.id}/`

  axios({
    method: 'get',
    url: productUrl
  })
    .then(res => {
      product.value = res.data

      const optionUrl =
        props.type === 'deposit'
          ? `http://127.0.0.1:8000/api/v2/deposit-options/${props.id}/`
          : `http://127.0.0.1:8000/api/v2/saving-options/${props.id}/`

      return axios({
        method: 'get',
        url: optionUrl
      })
    })
    .then(optionRes => {
      options.value = optionRes.data

      return axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/profile/my_profile/',
        headers: { Authorization: `Token ${token}` }
      })
    })
    .then(profileRes => {
      const likedList =
        props.type === 'deposit'
          ? profileRes.data.liked_deposits
          : profileRes.data.liked_savings

      isLiked.value = likedList.includes(props.id)
    })
})

const toggleLike = () => {
  const method = isLiked.value ? 'delete' : 'post'

  axios({
    method: method,
    url: `http://127.0.0.1:8000/api/v1/profile/like-${props.type}/${props.id}/`,
    headers: { Authorization: `Token ${token}` }
  })
    .then(() => {
      isLiked.value = !isLiked.value
    })
    .catch(() => {
      alert('관심상품 처리 중 오류가 발생했습니다.')
    })
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

.page-background {
  width: 100%;
  max-width: 960px;
}

.page-title {
  max-width: 960px;
  margin: 0 auto 24px;
  padding-left: 16px;
  font-size: 24px;
  font-weight: 700;
  color: black;
  border-left: 6px solid #38b2ac;
}

.product-wrapper {
  max-width: 960px;
  margin: 0 auto;
  padding: 32px 24px;
  background-color: #fff;
  font-family: 'Noto Sans KR', sans-serif;
  color: #1f2937;
  border-radius: 14px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.product-card {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  flex-wrap: wrap;
}

.name-box h2 {
  font-size: 22px;
  font-weight: 700;
  color: #1e3a8a;
  margin-bottom: 6px;
}

.bank-name {
  font-size: 14px;
  color: #6b7280;
}

.rate-box {
  text-align: right;
  min-width: 110px;
}

.rate-label {
  font-size: 12px;
  color: #6b7280;
  display: block;
  margin-bottom: 3px;
}

.rate-value {
  font-size: 28px;
  font-weight: 700;
  color: #dc2626;
}

.like-box-inline {
  margin-top: 8px;
  text-align: right;
}

.like-button {
  background-color: #2563eb;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  transition: background-color 0.25s;
  white-space: nowrap;
}

.like-button:hover {
  background-color: #1e40af;
}

.info-list {
  list-style: none;
  padding: 0;
  font-size: 14px;
  line-height: 1.6;
  color: #374151;
  border-top: 1px solid #e5e7eb;
  padding-top: 20px;
  margin: 0;
}

.info-list li {
  margin-bottom: 10px;
}

.option-section {
  margin-top: 20px;
}

.option-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 12px;
}

.table-wrapper {
  overflow-x: auto;
}

.option-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  font-size: 13px;
  min-width: 100%;
}

.option-table th,
.option-table td {
  border: 1px solid #d6d7d8;
  padding: 10px 12px;
  white-space: nowrap;
}

.option-table th {
  background-color: #f9fafb;
  color: #1f2937;
  font-weight: 600;
}

.router-links {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 24px;
}

.router-links a {
  flex: 1;
  text-align: center;
  background-color: #e0e7ff;
  color: #1e3a8a;
  padding: 12px 16px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  border: 1px solid #c7d2fe;
  transition: background-color 0.25s;
  white-space: nowrap;
}

.router-links a:hover {
  background-color: #c7d2fe;
}

@media (max-width: 768px) {
  .product-wrapper {
    padding: 24px 20px;
  }
  .product-card {
    gap: 20px;
  }
  .header {
    flex-direction: column;
    align-items: flex-start;
  }
  .rate-box {
    min-width: auto;
    text-align: left;
    margin-top: 8px;
  }
  .like-box-inline {
    text-align: left;
    margin-top: 6px;
  }
  .option-table {
    font-size: 11px;
    min-width: 320px;
  }
  .info-list {
    font-size: 12px;
    line-height: 1.4;
  }
  .router-links a {
    padding: 10px 14px;
    font-size: 12px;
  }
  .page-title {
    font-size: 22px;
  }
  .name-box h2 {
    font-size: 20px;
  }
  .bank-name {
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 18px;
    padding-left: 8px;
  }
  .product-wrapper {
    padding: 20px 12px;
  }
  .option-table th,
  .option-table td {
    padding: 6px 8px;
  }
  .rate-value {
    font-size: 20px;
  }
  .like-button {
    padding: 8px 10px;
    font-size: 13px;
  }
  .router-links {
    flex-direction: column;
    gap: 10px;
  }
  .router-links a {
    flex: none;
    width: 100%;
    padding: 8px 0;
    font-size: 13px;
  }
  .name-box h2 {
    font-size: 18px;
  }
  .bank-name {
    font-size: 12px;
  }
}

@media (max-width: 360px) {
  .option-table th,
  .option-table td {
    padding: 5px 6px;
  }
  .rate-value {
    font-size: 18px;
  }
  .name-box h2 {
    font-size: 16px;
  }
  .bank-name {
    font-size: 11px;
  }
}

@media (min-width: 1440px) {
  .wrapper {
    padding-left: 40px;
    padding-right: 40px;
  }
  .page-title {
    font-size: 24px;
  }
  .product-wrapper {
    padding: 48px 40px;
  }
  .name-box h2 {
    font-size: 20px;
  }
  .rate-value {
    font-size: 28px;
  }
  .option-table {
    font-size: 15px;
  }
}

</style>
