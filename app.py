import streamlit as st
import yfinance as yf

st.set_page_config(page_title="股票診斷儀表板", layout="centered")

st.title("📈 股票當沖與趨勢預測卡片")

stock_id = st.text_input("請輸入台股代碼（預設 2464 盟立）：", "2464")

if stock_id:
    ticker = f"{stock_id}.TW"
    data = yf.Ticker(ticker).history(period="5d")

    if len(data) >= 2:
        latest = data.iloc[-1]
        close_price = round(latest['Close'], 2)
        high_price = latest['High']
        low_price = latest['Low']
        
        # 計算 CDP / 三關價
        mid_gate = round((high_price + low_price + close_price) / 3, 2)
        up_gate = round(mid_gate + (high_price - low_price), 2)
        down_gate = round(mid_gate - (high_price - low_price), 2)
        
        # 計算建議進出場區間
        entry_low = round(mid_gate * 0.986, 2)
        entry_high = round(mid_gate * 1.013, 2)
        stop_loss = round(down_gate * 1.003, 2)
        take_profit = round(up_gate * 0.999, 2)

        st.markdown(f"## **{stock_id} 當前股價：{close_price} 元**")
        st.success("🔥 狀態評估：數據已載入")

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
        st.warning("查無此股票數據，請確認代碼是否正確！")
