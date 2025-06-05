<template>
  <div class="container">
    <h1>게시글 작성</h1>
    <form @submit.prevent="submitArticle" class="form-wrapper">
      <div class="form-group">
        <label for="title">제목</label>
        <input type="text" id="title" v-model.trim="title" />
      </div>
      <div class="form-group">
        <label for="category">카테고리</label>
        <select id="category" v-model="category">
          <option disabled value="">-- 카테고리 선택 --</option>
          <option :value="0">공지사항</option>
          <option :value="1">정보공유</option>
          <option :value="2">자유게시판</option>
        </select>
      </div>
      <div class="form-group">
        <label for="content">내용</label>
        <textarea id="content" v-model.trim="content"></textarea>
      </div>
      <button type="submit" class="submit-button">등록</button>
    </form>
  </div>
</template>

<script setup>
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'
import { useArticleStore } from '@/stores/articles'
import { useAccountStore } from '@/stores/accounts'
import { ref, onMounted } from 'vue'

const router = useRouter()
const route = useRoute()
const articleStore = useArticleStore()
const accountStore = useAccountStore()

const title = ref('')
const content = ref('')
const category = ref('')
const badWordsList = ref([])

const filterProfanity = function(text) {
  let result = text
  badWordsList.value.forEach(function(word) {
    const regex = new RegExp(word, 'gi')
    result = result.replace(regex, '*'.repeat(word.length))
  })
  return result
}

const loadBadWordsList = function() {
  axios({
    method: 'get',
    url: '/profanity.json'
  })
  .then(function(res) {
    badWordsList.value = res.data
  })
}

const submitArticle = function() {
  if (category.value === '') {
    alert('카테고리를 선택해주세요.')
    return
  }

  if (!confirm('게시글을 작성하시겠습니까?')) {
    return
  }

  const filteredTitle = filterProfanity(title.value)
  const filteredContent = filterProfanity(content.value)

  axios({
    method: 'post',
    url: `${articleStore.API_URL}/api/v3/articles/`,
    data: {
      title: filteredTitle,
      content: filteredContent,
      category: category.value
    },
    headers: { Authorization: `Token ${accountStore.token}` }
  })
  .then(() => {
    router.push({ name: 'article' })
  })
  .catch(() => {
    alert('게시글 등록에 실패했습니다.')
  })
}

onMounted(() => {
  if (route.query.category && !isNaN(route.query.category)) {
    category.value = Number(route.query.category)
  }
  loadBadWordsList()
})
</script>

<style scoped>
.container {
  max-width: 760px;
  margin: 0 auto;
  padding: 40px 24px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}

h1 {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 32px;
  color: #212529;
  border-left: 4px solid #0a857aa1;
  padding-left: 12px;
}

.form-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 700px;
  gap: 24px;
  background-color: #fff;
  padding: 32px;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

select {
  padding: 14px 16px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  background-color: #fff;
  transition: border-color 0.2s ease;
}

select:focus {
  border-color: #2f80ed;
}

label {
  font-size: 15px;
  font-weight: 500;
  color: #495057;
}

input[type="text"],
textarea {
  padding: 14px 16px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  background-color: #fff;
  transition: border-color 0.2s ease;
}

input[type="text"]:focus,
textarea:focus {
  border-color: #2f80ed;
}

textarea {
  height: 360px;
  resize: vertical;
}

.submit-button {
  align-self: flex-end;
  padding: 10px 22px;
  font-size: 15px;
  font-weight: 500;
  background-color: #2f80ed;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.submit-button:hover {
  background-color: #1a73e8;
}
</style>
