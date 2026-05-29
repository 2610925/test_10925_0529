import streamlit as st

# 1. 앱 페이지 설정
st.set_page_config(page_title="방구석 자판기", page_icon="🥤", layout="centered")
st.title("🥤 방구석 스마트 자판기")
st.markdown("돈을 넣고 원하는 음료수를 골라보세요!")

# 2. 자판기 데이터 초기화 (세션 상태 유지)
if "balance" not in st.session_state:
    st.session_state.balance = 0  # 투입된 금액

if "inventory" not in st.session_state:
    # 음료수 이름: [가격, 재고, 아이콘]
    st.session_state.inventory = {
        "콜라": [1500, 5, "🥤"],
        "사이다": [1400, 3, "🥛"],
        "캔커피": [1000, 10, "☕"],
        "이온음료": [1200, 2, "⚡"]
    }

if "history" not in st.session_state:
    st.session_state.history = []  # 구매 내역 로그

# --- 레이아웃 나누기 (왼쪽: 자판기 화면 / 오른쪽: 정산 및 로그) ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🛒 음료수 메뉴")
    
    # 음료수 목록을 가로로 배치하기 위해 컬럼 나누기
    menu_cols = st.columns(2)
    
    for i, (name, info) in enumerate(st.session_state.inventory.items()):
        price, stock, icon = info
        # 0, 1번은 첫 번째 열, 2, 3번은 두 번째 열에 배치
        with menu_cols[i % 2]:
            st.info(f"### {icon} {name}\n* **가격**: {price}원\n* **재고**: {stock}개 남음")
            
            # 구매 버튼 활성화 조건 제어
            button_disabled = False
            if stock <= 0:
                button_disabled = True
                button_text = "품절 ❌"
            elif st.session_state.balance < price:
                button_disabled = True
                button_text = "잔액 부족"
            else:
                button_text = f"{name} 구매하기"
            
            # 구매 버튼 클릭 시 로직
            if st.button(button_text, key=name, disabled=button_disabled):
                st.session_state.balance -= price  # 잔액 차감
                st.session_state.inventory[name][1] -= 1  # 재고 차감
                st.session_state.history.append(f"🎉 {name} 구매 완료! (-{price}원)")
                st.rerun()  # 화면 즉시 갱신

with col2:
    st.subheader("💰 금액 투입구")
    
    # 현재 잔액 표시
    st.metric(label="현재 투입된 금액", value=f"{st.session_state.balance} 원")
    
    # 돈 넣기 버튼들
    money_cols = st.columns(2)
    with money_cols[0]:
        if st.button("🪙 +500원"):
            st.session_state.balance += 500
            st.rerun()
    with money_cols[1]:
        if st.button("💵 +1,000원"):
            st.session_state.balance += 1000
            st.rerun()
            
    if st.button("💳 +5,000원", use_container_width=True):
        st.session_state.balance += 5000
        st.rerun()
        
    st.write("---")
    
    # 잔돈 반환 버튼
    if st.button("⚠️ 잔돈 반환 받기", use_container_width=True, type="secondary"):
        if st.session_state.balance > 0:
            st.success(f"거스름돈 {st.session_state.balance}원이 반환되었습니다. 💸")
            st.session_state.balance = 0
        else:
            st.warning("반환할 돈이 없습니다.")

# --- 하단 구매 로그 표시 ---
st.write("---")
st.subheader("📜 실시간 이용 내역")
if st.session_state.history:
    for log in reversed(st.session_state.history):  # 최신 로그가 위로 오도록
        st.write(log)
else:
    st.caption("아직 구매한 내역이 없습니다.")