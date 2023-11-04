# Region Coord
통계청의 데이터 API를 이용하여 대한민국 전국의 좌표 정보를 가져옵니다.

## 📁 데이터 형식
```bash
├── 시/도
│   └── 시/군/구
│       └── 읍/면/동
└── JSON 형식
```
## 📚 사용 기술
<div>
  <div>
    <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white">
    <img src="https://img.shields.io/badge/통계청 데이터API-7EBC6F?style=flat-square&logo=openstreetmap&logoColor=white">
    <img src="https://img.shields.io/badge/JSON-000000?style=flat-square&logo=json&logoColor=white">
    
  </div>
</div>

# 🌀 좌표 수집 사용방식
##통계청 Data API
### 메인 주소 : **`https://sgisapi.kostat.go.kr/OpenAPI3`**

### 인증 API
```
GET /auth/authentication.json

Body {
  consumer_key: 서비스 ID
  consumer_secret: 서비스 Secret
}
```

### 좌표 수집 API
```
GET /auth/authentication.json

Body {
  accessToken: 토큰,
  cd: 코드
}
```

### 좌표 변환 API
```
GET /transformation/transcoord.json

Body {
  accessToken: 토큰,
  src: 요청 좌표형식,
  dst: 반환 좌표형식,
  posX: X좌표
  posY: Y좌표
}
```

