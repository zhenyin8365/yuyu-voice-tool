"""
玉玉的声音工坊 — AI语音合成工具
"""

import streamlit as st
import os

# ====== 润锋配置区（帮客户填好之后重新部署即可）======
DEFAULT_API_KEY = ""
DEFAULT_VOICE_ID = ""

st.set_page_config(page_title="玉玉的声音工坊", page_icon="🎤", layout="centered")

st.markdown("""
<style>
.stButton>button {
    background: linear-gradient(135deg, #7b2ff7, #9b4dff) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    padding: 12px 24px !important; font-weight: 700 !important; width: 100%;
}
.stButton>button:hover { background: linear-gradient(135deg, #9b4dff, #b76eff) !important; }
.audio-box {
    background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.1);
    border-radius: 14px; padding: 20px; text-align: center; margin: 16px 0;
}
.pill {
    display: inline-block; background: rgba(123,47,247,.2); color: #c9a0dc;
    border-radius: 20px; padding: 4px 14px; font-size: 13px; font-weight: 600; margin: 4px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:#e0b0ff;text-align:center'>🎤 玉玉的声音工坊</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#b8a9d4;margin-bottom:30px'>输入文字，用你的专属声音合成语音</p>", unsafe_allow_html=True)

# ====== 语音合成 ======
st.markdown("<h3 style='color:#c9a0dc'>📝 输入文字</h3>", unsafe_allow_html=True)

text = st.text_area("要合成的文字", key="synth_text", height=180,
    placeholder="在这里输入你想说的话，比如：大家好，我是玉玉，欢迎来到我的声音工坊...",
    max_chars=2000)
st.caption(f"{len(text)} / 2000 字")

col1, col2 = st.columns([1, 1])
with col1:
    speed = st.select_slider("语速", options=[0.8, 1.0, 1.2, 1.3, 1.5], value=1.0)
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    synth_btn = st.button("▶ 开始合成", use_container_width=True)

if synth_btn:
    if not text.strip():
        st.error("请先输入要合成的文字。")
    elif not DEFAULT_API_KEY and not st.session_state.get("api_key"):
        st.error("未配置 API-Key，请联系润锋。")
    elif not DEFAULT_VOICE_ID and not st.session_state.get("voice_id"):
        st.error("未配置音色ID，请联系润锋复刻声音。")
    else:
        with st.spinner("正在合成中，请稍候..."):
            try:
                api_key = DEFAULT_API_KEY or st.session_state.get("api_key", "")
                voice_id = DEFAULT_VOICE_ID or st.session_state.get("voice_id", "")
                os.environ["DASHSCOPE_API_KEY"] = api_key

                from dashscope.audio.tts_v2 import SpeechSynthesizer
                synthesizer = SpeechSynthesizer(
                    model="cosyvoice-v3.5-plus",
                    voice=voice_id,
                    speech_rate=speed,
                )
                audio = synthesizer.call(text)

                st.session_state["last_audio"] = audio
                st.session_state["last_text"] = text
                st.toast("合成完成！", icon="✅")
            except Exception as e:
                st.error(f"合成失败：{e}")

# ====== 合成结果 ======
if st.session_state.get("last_audio") and st.session_state.get("last_text"):
    st.markdown("---")
    st.markdown("<h3 style='color:#c9a0dc'>🔊 合成结果</h3>", unsafe_allow_html=True)

    audio_data = st.session_state["last_audio"]
    audio_text = st.session_state["last_text"]
    audio_size = len(audio_data) / 1024

    st.markdown(f"<div class='audio-box'>"
        f"<span class='pill'>语速 {speed}x</span>"
        f"<span class='pill'>{len(audio_text)} 字</span>"
        f"<span class='pill'>{audio_size:.0f} KB</span>"
        f"</div>", unsafe_allow_html=True)

    st.audio(audio_data, format="audio/mp3")
    st.download_button("📥 下载到手机", data=audio_data, file_name="玉玉的声音.mp3",
        mime="audio/mpeg", use_container_width=True)

# ====== 使用说明 ======
with st.expander("📖 使用说明"):
    st.markdown("""
    **怎么用：**
    1. 在上方输入你想说的话
    2. 选择合适的语速
    3. 点击「开始合成」
    4. 试听满意后点「下载到手机」

    **关于你的声音：**
    你的专属声音已经预先训练好了，输入任何文字都会用你的声音朗读。

    如遇到合成失败或任何问题，请联系 **润锋 13307871670**。
    """)

# ====== Footer ======
st.markdown("---")
st.markdown("<p style='text-align:center;color:#9b8ab8;font-size:12px;margin-top:30px'>Powered by <b>润锋 AI</b> · 让每个声音都被听见</p>", unsafe_allow_html=True)
