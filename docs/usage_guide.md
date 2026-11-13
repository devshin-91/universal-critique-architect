# Universal Critique Architect 사용 가이드

본 문서는 `universal-critique`를 실무에서 가장 효과적으로 활용하기 위한 실전 사용법을 안내합니다.

---

## 1. Antigravity IDE에서 스킬로 사용하기 (추천)

### 1) 설치 방법
본 저장소의 `skills/universal-critique` 디렉터리를 사용자의 전역 스킬 폴더에 복사합니다:

```powershell
# Windows PowerShell
Copy-Item -Recurse -Force "skills/universal-critique" "$HOME/.gemini/antigravity/skills/"
```

### 2) 실행 방법
Antigravity 채팅창에서 검토할 작업물과 함께 자연스럽게 호출합니다:

```
이 분산 시스템 설계서 비평해줘: C:\Users\user\projects\core\architecture.md
사용할 도구는 Antigravity랑 Claude Pro야.
```

스킬은 다음과 같이 자동으로 작동합니다:
1. **1단계 (자동 감지):** 파일 경로와 도구 2개가 파악되었으므로 불필요한 질문 없이 즉시 2단계로 직행합니다.
2. **2단계 (루브릭 및 분할 배정):** 분산 시스템 아키텍처에 맞춰 '동시성/Dirty State', '단일 장애점(SPOF)', '네트워크 파티션' 루브릭을 선정하고, Antigravity에는 SRE 감사관, Claude에는 데이터 정합성 수석 감사관을 1:1로 분할 배정합니다.
3. **3단계 (프롬프트 투하):**
   - Antigravity용: 로컬 파일을 직접 읽도록 `read_file` 전제 조건이 포함된 하든드 프롬프트 제공
   - Claude용: 3,000자 초과 여부를 감지하여 토큰 보호 슬롯 및 `> [!WARNING]` 보안 경고가 분리된 복사 전용 프롬프트 투하

---

## 2. 웹 UI (ChatGPT / Claude / Gemini)에서 단독 프롬프트로 사용하기

1. `prompts/universal_critique_v2.4.md`의 전체 내용을 복사합니다.
2. 즐겨 쓰는 웹 AI 인터페이스(ChatGPT, Claude.ai, Gemini 웹)의 첫 메시지로 붙여넣습니다.
3. 이어서 비평받고자 하는 작업물 본문이나 코드 조각을 입력합니다.
4. 출력된 도구별 맞춤 프롬프트를 복사하여 다른 AI 창에 붙여넣고 상호 교차 검증을 수행합니다.

---

## 3. 결과 해석 및 액션 아이템 도출 팁

- **[정상(Pass): 결함 없음] 확인:**
  정상 판정된 부분은 구조적으로 탄탄한 부분이므로 억지로 뜯어고칠 필요가 없습니다. 안심하고 유지하세요.
- **[심각도: 치명적(Critical)] 즉시 격리:**
  Critical 판정을 받은 항목은 서비스 다운, 데이터 유실, 법령 위반(과징금)으로 직결되는 결함입니다. 모든 추가 개발을 중단하고 최우선으로 리팩토링하세요.
- **점수 비교:**
  동일한 작업물에 대해 두 AI가 매긴 점수가 크게 벌어진 경우(예: 한 쪽은 100점, 다른 쪽은 74점), 점수가 낮은 쪽이 발견한 '숨은 엣지 케이스'에 주목하세요.
