<template>
  <div class="wrapper">
    <div v-if="article" class="article-info">
      <div class="title-row">
        <span class="article-title-text">{{ article.title }}</span>
        <span class="article-category">[{{ getCategoryName(article.category) }}]</span>
        <span class="article-time"> | </span>
        <span class="article-time">{{ formatDate(article.created_at) }}</span>
        <button
          v-if="article.user === accountStore.username"
          class="change-btn"
          @click="goToEditPage"
        >
          수정
        </button>
        <button
          v-if="article.user === accountStore.username"
          class="delete-btn"
          @click="deleteArticle"
        >
          삭제
        </button>
      </div>
      <div class="article-content">{{ article.content }}</div>
    </div>

    <div class="review-section">
      <form @submit.prevent="submitComment" class="comment-form">
        <div class="comment-flex">
          <div class="comment-box">
            <textarea
              v-model="newComment"
              placeholder="댓글을 입력하세요"
              class="comment-textarea"
            ></textarea>
            <div class="comment-actions">
              <button type="submit" :disabled="!newComment.trim()">등록</button>
            </div>
          </div>
        </div>
      </form>

      <ReviewItem :reviews="commentList" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/articles'
import { useAccountStore } from '@/stores/accounts'
import ReviewItem from '@/components/ReviewItem.vue'
import axios from 'axios'

const accountStore = useAccountStore()
const articleStore = useArticleStore()
const route = useRoute()
const router = useRouter()

const article = ref(null)
const newComment = ref('')
const commentList = ref([])
const profanityList = ref([])

const getCategoryName = (num) => {
  if (num === 0) return '공지사항'
  if (num === 1) return '정보공유'
  if (num === 2) return '자유게시판'
  return '기타'
}

function filterProfanity(text) {
  let cleanText = text
  profanityList.value.forEach((word) => {
    const regex = new RegExp(word, 'gi')
    cleanText = cleanText.replace(regex, '*'.repeat(word.length))
  })
  return cleanText
}

function loadProfanityList() {
  axios({
    method: 'get',
    url: '/profanity.json'
  }).then((res) => {
    profanityList.value = res.data
  })
}

function loadArticle() {
  axios({
    method: 'get',
    url: `${articleStore.API_URL}/api/v3/articles/${route.params.id}/`,
    headers: { Authorization: `Token ${accountStore.token}` }
  }).then((res) => {
    article.value = res.data
    commentList.value = res.data.reviews
  })
}

function submitComment() {
  const filteredComment = filterProfanity(newComment.value)

  axios({
    method: 'post',
    url: `${articleStore.API_URL}/api/v3/articles/${route.params.id}/reviews/`,
    headers: { Authorization: `Token ${accountStore.token}` },
    data: { content: filteredComment }
  }).then(() => {
    newComment.value = ''
    loadArticle()
  })
}

function deleteArticle() {
  if (!confirm('정말 삭제하시겠습니까?')) return

  axios({
    method: 'delete',
    url: `${articleStore.API_URL}/api/v3/articles/${route.params.id}/`,
    headers: { Authorization: `Token ${accountStore.token}` }
  }).then(() => {
    articleStore.articles = articleStore.articles.filter(
      (item) => item.id !== Number(route.params.id)
    )
    router.push({ name: 'article' })
  })
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  })
}

function goToEditPage() {
  router.push({
    name: 'edit',
    params: { id: route.params.id },
    query: {
      title: article.value.title,
      content: article.value.content,
      category: article.value.category
    }
  })
}

onMounted(() => {
  if (!accountStore.token) {
    router.push({ name: 'login' })
    return
  }
  loadProfanityList()
  loadArticle()
})
</script>

<style scoped>
.wrapper {
  max-width: 1080px;
  margin: 0 auto;
  padding: 60px 32px;
  font-family: 'Noto Sans KR', sans-serif;
  color: #222;
  box-sizing: border-box;
}

.article-info {
  padding-top: 48px;
}

.title-row {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 12px;
  margin-bottom: 24px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
}

.article-title-text {
  font-size: 28px;
  font-weight: 700;
  word-break: break-word;
}

.article-category {
  font-size: 16px;
  color: #666;
}

.article-time {
  margin-left: 3px;
  font-size: 15px;
  color: #888;
}

.article-content {
  font-size: 20px;
  line-height: 2.2;
  padding: 40px 0;
  white-space: pre-wrap;
  border-bottom: 1px solid #e0e0e0;
  min-height: 520px;
  margin-bottom: 48px;
}

.review-section {
  margin-top: 0;
}

form {
  width: 100%;
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-textarea {
  width: 100%;
  min-height: 140px;
  padding: 16px 20px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 10px;
  resize: vertical;
  line-height: 1.8;
  outline: none;
}

.comment-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
}

button[type='submit'] {
  padding: 12px 20px;
  font-size: 14px;
  background-color: #2f80ed;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button[type='submit']:hover {
  background-color: #1a73e8;
}

.change-btn,
.delete-btn {
  background: none;
  border: none;
  color: #888;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

@media (max-width: 768px) {
  .wrapper {
    padding: 40px 20px;
  }

  .title-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .article-title-text {
    font-size: 22px;
  }

  .article-category,
  .article-time {
    font-size: 14px;
    margin-left: 0;
  }

  .article-content {
    font-size: 16px;
    line-height: 1.8;
    padding: 30px 0;
    min-height: 320px;
  }

  .comment-textarea {
    font-size: 14px;
    min-height: 100px;
  }

  button[type='submit'] {
    font-size: 13px;
    padding: 10px 16px;
  }

  .change-btn,
  .delete-btn {
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .wrapper {
    padding: 30px 16px;
  }

  .article-title-text {
    font-size: 20px;
  }

  .article-content {
    padding: 20px 0;
  }
}
</style>

