// store/articles.js

import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  const accountStore = useAccountStore()

  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v3/articles/`,
      headers: {
        Authorization: `Token ${accountStore.token}` 
      }
    })
      .then(res => {
        console.log('으아아아', res.data)
        articles.value = res.data
      })
      .catch(err => console.log(err))
  }
  return { articles, API_URL, getArticles }
}, { persist: true })
