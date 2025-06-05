<template>
  <div class="wrapper">
    <h1>프로필 수정</h1>

    <label>아이디 (username)</label>
    <input type="text" v-model="username" readonly />

    <label>기존 비밀번호</label>
    <input type="password" v-model="oldPassword" placeholder="현재 비밀번호 입력 (필수)" />

    <label>변경할 비밀번호</label>
    <input type="password" v-model="password" placeholder="변경할 비밀번호 입력" />
    <p class="notice">
    </p>

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

onMounted(function () {
  username.value = accountStore.username
  userId.value = accountStore.userId

  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/api/v1/profile/my_profile/',
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  })
  .then(function (res) {
    email.value = res.data.email
  })
})

function submitProfile() {
  if (password.value && !oldPassword.value) {
    alert('비밀번호를 변경하려면 기존 비밀번호를 입력해주세요.')
    return
  }

  axios({
    method: 'put',
    url: 'http://127.0.0.1:8000/api/v1/profile/edit/',
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
  max-width: 800px;
  margin: 0 auto;
  padding: 64px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
  background-color: rgba(240, 240, 240, 0.832);
}

h1 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 40px;
  color: #1f2937;
}

label {
  display: block;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
  margin-top: 28px;
  color: #374151;
}

input {
  width: 100%;
  padding: 16px 18px;
  font-size: 18px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  box-sizing: border-box;
  transition: border-color 0.2s ease;
}

input:focus {
  outline: none;
  border-color: #2563eb;
}

.notice {
  color: #dc2626;
  font-size: 16px;
  margin-left: 6px;
  margin-top: 14px;
}

form {
  margin-top: 28px;
}

form button {
  display: block;
  margin-left: auto;
  margin-top: 20px;
  padding: 14px 28px;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

form button:hover {
  background-color: #1d4ed8;
}
</style>

