import datetime
import requests
import streamlit as st

st.set_page_config(page_title="股票診斷儀表板", layout="centered")
st.title("📈 股票當沖與趨勢預測卡片 (FinMind 即時版)")

# 請把引號內的文字換成你從 FinMind 複製的長字串 Token
FINMIND_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoib2xkZ29vc2UyNzQwMDVAZ21haWwuY29tIiwiZW1haWwiOiJvbGRnb29zZTI3NDAwNUBnbWFpbC5jb20iLCJ0b2tlbl92ZXJzaW9uIjowfQ.NXR_FwKcCTc0bN44eftx_rv37NOoBCkfHaC-ZQnQpVM"

stock_id = st.text_input("請輸入台股代碼（預設 2464 盟立）：", "2464")

if stock_id:
    end_date = datetime.date.today().strftime("%Y-%m-%d")
    start_date = (datetime.date.today() - datetime.timedelta(days=10)).strftime(
        "%Y-%m-%d"
    )

    url = "https://api.finmindtrade.com/api/v4/data"
    params = {
        "dataset": "TaiwanStockPrice",
        "data_id": stock_id,
        "start_date": start_date,
        "end_date": end_date,
        "token": FINMIND_TOKEN,
    }

    res = requests.get(url, params=params)
    data = res.json().get("data", [])

    if len(data) >= 2:
        latest = data[-1]

        close_price = round(float(latest["close"]), 2)
        high_price = float(latest["max"])
        low_price = float(latest["min"])

        mid_gate = round((high_price + low_price + close_price) / 3, 2)
        up_gate = round(mid_gate + (high_price - low_price), 2)
        down_gate = round(mid_gate - (high_price - low_price), 2)

        entry_low = round(mid_gate * 0.986, 2)
        entry_high = round(mid_gate * 1.013, 2)
        stop_loss = round(down_gate * 1.003, 2)
        take_profit = round(up_gate * 0.999, 2)

        st.markdown(
            f"## **{stock_id} 最新收盤/盤中價：{close_price} 元** ({latest['date']})"
        )
        st.success("🔥 狀態評估：FinMind 台股數據載入成功！")

        st.markdown("---")
        st.subheader("🔥 日內當沖進出場參考")

        col1, col2, col3 = st.columns(3)
        col1.metric("上關 (壓力)", f"{up_gate}")
        col2.metric("中關 (核心)", f"{mid_gate}")
        col3.metric("下關 (支撐)", f"{down_gate}")

        st.markdown("---")

        col_a, col_b, col_c = st.columns(3)
        col_a.info(f"💵 **進場區間**\n\n{entry_low} ~ {entry_high}")
        col_b.error(f"🛑 **停損建議**\n\n{stop_loss}\n(跌破出場)")
        col_c.success(f"🎯 **停利目標**\n\n{take_profit}\n(上關獲利)")
    else:
        st.warning("查無此股票數據，請確認代碼是否正確或 Token 設定是否有誤！")
