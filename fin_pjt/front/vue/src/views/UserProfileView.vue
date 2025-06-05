<template>
  <div class="wrapper">
    <h1>프로필 작성</h1>

    <label>아이디 (username)</label>
    <input type="text" v-model="username" readonly />

    <label>기존 비밀번호</label>
    <input
      type="password"
      v-model="oldPassword"
      placeholder="현재 비밀번호 입력"
    />

    <form @submit.prevent="submitProfile">
      <label>닉네임</label>
      <input type="text" v-model="nickname" />

      <label>이메일</label>
      <input type="email" v-model="email" required />

      <label>생년월일</label>
      <input type="date" v-model="birthdate" />

      <label>자산</label>
      <input type="number" v-model="asset" />

      <label>월급 (*세전 금액)</label>
      <input type="number" v-model="salary" />
      <button type="submit">저장</button>
    </form>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()
const router = useRouter()

const username = ref('')
const userId = ref('')
const password = ref('')
const oldPassword = ref('')
const nickname = ref('')
const email = ref('')
const birthdate = ref('')
const asset = ref('')
const salary = ref('')

onMounted(() => {
  username.value = accountStore.username
  userId.value = accountStore.userId
})

function submitProfile() {
  if (password.value && !oldPassword.value) {
    alert('비밀번호를 변경하려면 기존 비밀번호를 입력해주세요.')
    return
  }

  axios({
    method: 'post',
    url: 'http://127.0.0.1:8000/api/v1/profile/',
    headers: {
      Authorization: `Token ${accountStore.token}`
    },
    data: {
      email: email.value,
      nickname: nickname.value,
      birthdate: birthdate.value,
      asset: asset.value,
      salary: salary.value
    }
  })
  .then(function () {
    if (password.value && oldPassword.value) {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/password/change/',
        headers: {
          Authorization: `Token ${accountStore.token}`
        },
        data: {
          old_password: oldPassword.value,
          new_password1: password.value
        }
      })
      .then(function () {
        alert('프로필이 저장되었고 비밀번호가 변경되었습니다.')
        router.push({ name: 'final-userprofile', params: { id: accountStore.userId } })
      })
    }
    else {
      alert('프로필이 저장되었습니다.')
      router.push({ name: 'final-userprofile', params: { id: accountStore.userId } })
    }
  })
}

</script>

<style scoped>
.wrapper {
  max-width: 700px;
  margin: 0 auto;
  padding: 48px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
  background-color: rgba(240, 240, 240, 0.832);
}

h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 32px;
  color: #1f2937;
}

label {
  display: block;
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 8px;
  margin-top: 24px;
  color: #374151;
}

input {
  width: 100%;
  padding: 14px 16px;
  font-size: 16px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  box-sizing: border-box;
  transition: border-color 0.2s ease;
}

input:focus {
  outline: none;
  border-color: #2563eb;
}

.notice {
  color: #dc2626;
  font-size: 15px;
  margin-left: 6px;
  margin-top: 12px;
}

form {
  margin-top: 20px;
}

form button {
  display: block;
  margin-left: auto; 
  margin-top: 16px;
  padding: 12px 24px;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}


button:hover {
  background-color: #1d4ed8;
}
</style>
