"""
玉玉的声音工坊 — AI语音合成工具
"""

import streamlit as st
import os

st.set_page_config(page_title="玉玉的声音工坊", page_icon="🎤", layout="centered")

# ====== 从 URL 读取已保存的配置 ======
try:
    params = st.query_params
except Exception:
    params = {}
saved_key = params.get("key", "") if isinstance(params.get("key"), str) else ""
saved_voice = params.get("voice", "") if isinstance(params.get("voice"), str) else ""

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

# ====== 配置区（折叠，填一次即可）======
with st.expander("⚙️ 配置（仅需填写一次）", expanded=not saved_key):
    st.caption("填好后点「保存配置」，会把信息存到链接里。下次打开自动生效，无需重复填写。")
    col_a, col_b = st.columns(2)
    with col_a:
        api_key = st.text_input("API-Key", key="cfg_key", value=saved_key,
            type="password", placeholder="sk-xxxxxxxxxxxxxxxx")
    with col_b:
        voice_id = st.text_input("音色ID", key="cfg_voice", value=saved_voice,
            placeholder="cosyvoice-v3.5-plus-bailian-xxxxxxxx")

    if st.button("💾 保存配置", use_container_width=True):
        if api_key.strip() and voice_id.strip():
            st.query_params["key"] = api_key.strip()
            st.query_params["voice"] = voice_id.strip()
            st.rerun()
        else:
            st.error("请填写完整的 API-Key 和音色ID。")

if not saved_key or not saved_voice:
    st.info("请先在上方填写 API-Key 和音色ID，点「保存配置」。填一次即可，之后不用再填。")
    st.stop()

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
    else:
        with st.spinner("正在合成中，请稍候..."):
            try:
                os.environ["DASHSCOPE_API_KEY"] = saved_key
                from dashscope.audio.tts_v2 import SpeechSynthesizer
                synthesizer = SpeechSynthesizer(
                    model="cosyvoice-v3.5-plus",
                    voice=saved_voice,
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
    st.markdown("**怎么用**")
    st.markdown("1. 在上方输入你想说的话")
    st.markdown("2. 选择合适的语速")
    st.markdown("3. 点击「开始合成」")
    st.markdown("4. 试听满意后点「下载到手机」")
    st.markdown("")
    st.markdown("**关于你的声音**")
    st.markdown("你的专属声音已经预先训练好了，输入任何文字都会用你的声音朗读出来。")
    st.markdown("")
    st.markdown("如遇到合成失败或任何问题，请联系 **润锋 13307871670**。")

# ====== Footer ======
st.markdown("---")
st.markdown("<p style='text-align:center;color:#9b8ab8;font-size:12px;margin-top:30px'>Powered by <b>润锋 AI</b> · 让每个声音都被听见</p>", unsafe_allow_html=True)
