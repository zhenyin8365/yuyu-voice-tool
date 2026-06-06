"""
玉玉的声音工坊 — AI语音合成工具
"""

import streamlit as st
import os

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

# ====== 第一步：配置 ======
with st.expander("⚙️ 第一步：配置", expanded=True):
    col_a, col_b = st.columns(2)
    with col_a:
        api_key = st.text_input("API-Key", type="password", placeholder="sk-xxxxxxxxxxxxxxxx")
    with col_b:
        voice_id = st.text_input("音色ID", placeholder="cosyvoice-v3.5-plus-bailian-xxxxxxxx")

# ====== 第二步：合成 ======
st.markdown("<h3 style='color:#c9a0dc'>📝 第二步：语音合成</h3>", unsafe_allow_html=True)

text = st.text_area("输入要合成的文字", height=180,
    placeholder="在这里输入你想说的话，或者点击下方模板快速填充...",
    max_chars=2000,
    key="synth_text_area")
st.caption(f"{len(text)} / 2000 字")

# 快捷模板
st.caption("💡 快捷模板（点击自动填入）：")
templates = {
    "📞 电话客服": "您好，感谢您的来电。我是您的专属客服，请问有什么可以帮您的？",
    "💬 陪伴闲聊": "今天天气真好，心情也跟着好了起来。有时候简单的事情，就能让人开心一整天。",
    "🛍️ 产品介绍": "欢迎了解我们的新产品，它采用最新技术，简约设计，操作简单，非常适合日常使用。",
    "💼 品牌宣传": "专注品质，用心服务。我们始终坚持以客户为中心，为您提供最优质的产品和体验。",
    "🎉 节日祝福": "祝您节日快乐，身体健康，家庭幸福！感谢您一直以来的支持与信任。",
    "📱 日常问候": "早上好！新的一天开始了，愿你今天心情美好，工作顺利，生活愉快。",
    "🎙️ 自我介绍": "大家好，我是玉玉，欢迎来到我的声音工坊。这里可以用我的专属声音朗读任何文字。",
}
cols = st.columns(4)
for i, (label, sample) in enumerate(templates.items()):
    with cols[i % 4]:
        if st.button(label, key=f"tmpl_{i}", use_container_width=True):
            st.session_state["synth_text_area"] = sample
            st.rerun()

col_s1, col_s2 = st.columns(2)
with col_s1:
    speed = st.select_slider("语速", options=[0.8, 1.0, 1.2, 1.3, 1.5], value=1.0)
with col_s2:
    volume = st.slider("音量", min_value=0, max_value=100, value=80)

if st.button("▶ 开始合成", use_container_width=True):
    if not api_key.strip():
        st.error("请先填写 API-Key。")
    elif not voice_id.strip():
        st.error("请先填写音色ID。")
    elif not text.strip():
        st.error("请先输入要合成的文字。")
    else:
        with st.spinner("正在合成中，请稍候..."):
            try:
                os.environ["DASHSCOPE_API_KEY"] = api_key.strip()
                from dashscope.audio.tts_v2 import SpeechSynthesizer
                synthesizer = SpeechSynthesizer(
                    model="cosyvoice-v3.5-plus",
                    voice=voice_id.strip(),
                    speech_rate=speed,
                    volume=volume,
                )
                audio = synthesizer.call(text)
                st.session_state["last_audio"] = audio
                st.session_state["last_text"] = text
                st.session_state["last_speed"] = speed
                st.toast("合成完成！", icon="✅")
                st.rerun()
            except Exception as e:
                st.error(f"合成失败：{e}")

# ====== 合成结果 ======
if st.session_state.get("last_audio") and st.session_state.get("last_text"):
    st.markdown("---")
    st.markdown("<h3 style='color:#c9a0dc'>🔊 合成结果</h3>", unsafe_allow_html=True)

    audio_data = st.session_state["last_audio"]
    audio_text = st.session_state["last_text"]
    audio_size = len(audio_data) / 1024
    last_speed = st.session_state.get("last_speed", 1.0)

    st.markdown(f"<div class='audio-box'>"
        f"<span class='pill'>语速 {last_speed}x</span>"
        f"<span class='pill'>{len(audio_text)} 字</span>"
        f"<span class='pill'>{audio_size:.0f} KB</span>"
        f"</div>", unsafe_allow_html=True)

    st.audio(audio_data, format="audio/mp3")
    st.download_button("📥 下载到手机", data=audio_data, file_name="玉玉的声音.mp3",
        mime="audio/mpeg", use_container_width=True)

# ====== 使用说明 ======
with st.expander("📖 使用说明"):
    st.markdown("**怎么用**")
    st.markdown("1. 填写 API-Key 和音色ID（润锋提供，填一次即可）")
    st.markdown("2. 输入你想说的话")
    st.markdown("3. 选择合适的语速，点击「开始合成」")
    st.markdown("4. 试听满意后点「下载到手机」")
    st.markdown("")
    st.markdown("**关于你的声音**")
    st.markdown("你的专属声音已经预先训练好了，输入任何文字都会用你的声音朗读出来。")
    st.markdown("")
    st.markdown("如遇到合成失败或任何问题，请联系 **润锋 13307871670**。")

st.markdown("---")
st.markdown("<p style='text-align:center;color:#9b8ab8;font-size:12px;margin-top:30px'>Powered by <b>润锋 AI</b> · 让每个声音都被听见</p>", unsafe_allow_html=True)
