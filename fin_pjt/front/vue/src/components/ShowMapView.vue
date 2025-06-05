<template>
  <div class="map-page">
    <aside class="sidebar">
      <h1>내 주변 은행 찾기</h1>
      <MapSearchView
        @update-sido="selectedSido = $event"
        @update-gungu="selectedGungu = $event"
        @update-bank="selectedBank = $event"
        @update-search-type="searchType = $event"
        @trigger-search="triggerSearch"
      />
    </aside>
    <section class="map-area">
      <div id="map"></div>
    </section>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import MapSearchView from '../components/MapSearchView.vue'

const selectedSido = ref('')
const selectedGungu = ref('')
const selectedBank = ref('')
const searchType = ref('bank')
const shouldSearch = ref(false)

let map = null
let places = null
let markers = []
let infoWindows = []

function triggerSearch() {
  shouldSearch.value = true
}

onMounted(function () {
  nextTick()
  .then(()=> {
    if (!window.kakao || !window.kakao.maps) {
      const script = document.createElement('script')
      script.src = '//dapi.kakao.com/v2/maps/sdk.js?appkey=e258d582e93aafacb6174dcf18c5388c&libraries=services&autoload=false'
      script.onload = function () {
        kakao.maps.load(initMap)
      }
      document.head.appendChild(script)
    } else {
      kakao.maps.load(initMap)
    }
  })
})

function initMap() {
  const container = document.getElementById('map')
  const options = {
    center: new kakao.maps.LatLng(37.5665, 126.978),
    level: 3
  }
  map = new kakao.maps.Map(container, options)
  places = new kakao.maps.services.Places()
}

// 검색 결과 변화에 따른 마커 표시
watch(shouldSearch, function (search) {
  if (!search) return
  if (!selectedSido.value || !selectedGungu.value) return
  if (!map || !places) return

  const type = searchType.value === 'bank' ? selectedBank.value : 'ATM'
  const keyword = selectedSido.value + ' ' + selectedGungu.value + ' ' + type

  markers.forEach(function (m) { m.setMap(null) })
  infoWindows.forEach(function (iw) { iw.close() })
  markers = []
  infoWindows = []

  places.keywordSearch(keyword, function (data, status) {
    if (status !== kakao.maps.services.Status.OK) return

    const bounds = new kakao.maps.LatLngBounds()

    data.forEach(function (place) {
      const position = new kakao.maps.LatLng(place.y, place.x)

      const marker = new kakao.maps.Marker({ map: map, position: position })
      markers.push(marker)

      let content = '<div style="padding:10px; font-size:14px; max-width:200px; word-break:break-word">'
      content += '<strong>' + place.place_name + '</strong><br>'
      content += place.address_name + '<br>'
      if (place.phone) content += '전화: ' + place.phone + '<br>'
      content += '<a href="' + place.place_url + '" target="_blank">카카오맵에서 보기</a>'
      content += '</div>'

      const iw = new kakao.maps.InfoWindow({ content: content })
      infoWindows.push(iw)

      kakao.maps.event.addListener(marker, 'mouseover', function () { iw.open(map, marker) })
      kakao.maps.event.addListener(marker, 'mouseout', function () { iw.close() })

      bounds.extend(position)
    })

    map.setBounds(bounds)
  })

  shouldSearch.value = false
})
</script>


<style scoped>
.map-page {
  display: flex;
  height: 100vh;
  background-color: #f4f6f8;
}

.sidebar {
  flex: 0 0 420px;
  background-color: #fff;
  padding: 32px 24px;
  border-right: 1px solid #e0e0e0;
  overflow-y: auto;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.05);
}

.map-area {
  flex: 1;
  display: flex;
  align-items: stretch;
}

#map {
  width: 100%;
  height: 100%;
  border: none;
}
</style>
