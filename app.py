"""
玉玉的声音工坊 — AI语音合成工具
客户用自己的阿里云百炼 API-Key 和复刻音色ID，输入文字即可合成语音并下载。
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
a { color: #c0a0f0 !important; }
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
st.markdown("<p style='text-align:center;color:#b8a9d4;margin-bottom:30px'>专属你的AI语音合成 · 三步搞定</p>", unsafe_allow_html=True)

# ====== Step 1: API Key ======
with st.expander("🔑 第一步：获取 API-Key", expanded=not st.session_state.get("step1_done")):
    st.markdown("""
    去阿里云百炼控制台获取 API-Key：

    1. 点下方按钮打开百炼控制台
    2. 登录阿里云账号（没有就注册一个）
    3. 右上角点击头像 → **API-KEY** → 创建新的 → 复制
    """)
    st.link_button("去百炼控制台获取 API-Key", "https://bailian.console.aliyun.com/?tab=api", use_container_width=True)

    api_key = st.text_input("粘贴 API-Key", key="api_key_input",
        value=st.session_state.get("api_key", ""),
        placeholder="sk-xxxxxxxxxxxxxxxx",
        type="password")
    if api_key.strip():
        st.session_state["api_key"] = api_key.strip()
        st.session_state["step1_done"] = True

if st.session_state.get("api_key"):
    st.success("API-Key 已设置")

# ====== Step 2: Voice Clone ======
with st.expander("🎙️ 第二步：复刻你的声音", expanded=not st.session_state.get("step2_done")):
    st.markdown("""
    **声音复刻（一次性操作，建议在电脑上完成）：**

    方式一：手机录好音，把录音发到电脑上，用下方按钮打开复刻页面上传。
    方式二：直接在电脑麦克风前录 10-20 秒讲话。

    复刻完成后，把生成的 **音色ID** 粘贴回来。之后就能随时在手机上合成了。
    """)
    st.link_button("去复刻我的声音（百炼控制台）", "https://bailian.console.aliyun.com/cn-beijing#/efm/model_experience_center/voice?currentTab=voiceTts&secondary=clone&primary=cloning", use_container_width=True)

    voice_id = st.text_input("粘贴音色ID", key="voice_id_input",
        value=st.session_state.get("voice_id", ""),
        placeholder="例如 cosyvoice-v3.5-plus-bailian-abc123def4567890")
    if voice_id.strip():
        st.session_state["voice_id"] = voice_id.strip()
        st.session_state["step2_done"] = True

if st.session_state.get("voice_id"):
    st.success(f"音色ID 已设置 · {st.session_state['voice_id'][:50]}...")

# ====== Step 3: Synthesize ======
st.markdown("---")
st.markdown("<h3 style='color:#c9a0dc'>📝 第三步：语音合成</h3>", unsafe_allow_html=True)

text = st.text_area("输入要合成的文字", key="synth_text", height=150,
    placeholder="在这里输入文字，比如：大家好，我是玉玉，欢迎来到我的声音工坊...",
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
    elif not st.session_state.get("api_key"):
        st.error("请先在第一步设置 API-Key。")
    elif not st.session_state.get("voice_id"):
        st.error("请先在第二步设置音色ID。")
    else:
        with st.spinner("正在合成中，请稍候..."):
            try:
                os.environ["DASHSCOPE_API_KEY"] = st.session_state["api_key"]
                from dashscope.audio.tts_v2 import SpeechSynthesizer

                synthesizer = SpeechSynthesizer(
                    model="cosyvoice-v3.5-plus",
                    voice=st.session_state["voice_id"],
                    speech_rate=speed,
                )
                audio = synthesizer.call(text)

                st.session_state["last_audio"] = audio
                st.session_state["last_text"] = text
                st.toast("合成完成！", icon="✅")
            except Exception as e:
                st.error(f"合成失败：{e}")

# ====== Result ======
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

    st.download_button(
        label="📥 下载到手机",
        data=audio_data,
        file_name="玉玉的声音.mp3",
        mime="audio/mpeg",
        use_container_width=True,
    )

# ====== Footer ======
st.markdown("---")
st.markdown("<p style='text-align:center;color:#9b8ab8;font-size:12px;margin-top:30px'>Powered by <b>润锋 AI</b> · 让每个声音都被听见</p>", unsafe_allow_html=True)
