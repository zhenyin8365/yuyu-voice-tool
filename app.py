"""
玉玉的声音工坊 — AI语音合成工具
客户用自己的阿里云百炼 API-Key 和复刻音色ID，输入文字即可合成语音并下载。
"""

import streamlit as st
import os, base64, json, urllib.request

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
    tab1, tab2 = st.tabs(["📱 手机上传录音", "💻 电脑端复刻"])

    with tab1:
        st.markdown("""
        **用手机录音直接复刻（推荐）：**
        1. 打开手机自带的「语音备忘录」，录一段 **10-20 秒** 的讲话
        2. 保存后点下方按钮上传录音文件
        3. 系统自动完成复刻，返回音色ID
        """)
        audio_file = st.file_uploader("上传录音", type=["mp3", "wav", "m4a", "m4a"], key="voice_sample",
            help="支持 MP3 / WAV / M4A，建议 10-20 秒清晰人声")

        preferred_name = st.text_input("给音色起个名字（可选）", key="voice_name",
            placeholder="例如：yuyu", max_chars=10)

        if audio_file and st.button("开始复刻", key="clone_btn", use_container_width=True):
            if not st.session_state.get("api_key"):
                st.error("请先在第一步设置 API-Key。")
            else:
                with st.spinner("正在复刻你的声音，大约需要 30 秒..."):
                    try:
                        audio_bytes = audio_file.read()
                        b64_str = base64.b64encode(audio_bytes).decode()
                        ext = audio_file.name.rsplit(".", 1)[-1] if "." in audio_file.name else "mp3"
                        mime = {"mp3": "audio/mpeg", "wav": "audio/wav", "m4a": "audio/mp4", "m4a": "audio/mp4"}.get(ext, "audio/mpeg")
                        data_uri = f"data:{mime};base64,{b64_str}"

                        name = preferred_name.strip() or "myvoice"

                        payload = json.dumps({
                            "model": "qwen-voice-enrollment",
                            "input": {
                                "action": "create",
                                "target_model": "cosyvoice-v3.5-plus",
                                "preferred_name": name,
                                "audio": {"data": data_uri}
                            }
                        }).encode("utf-8")

                        req = urllib.request.Request(
                            "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization",
                            data=payload,
                            headers={
                                "Authorization": f"Bearer {st.session_state['api_key']}",
                                "Content-Type": "application/json",
                            },
                            method="POST",
                        )
                        with urllib.request.urlopen(req, timeout=60) as resp:
                            result = json.loads(resp.read().decode("utf-8"))

                        voice_id = result.get("output", {}).get("voice", "")
                        if voice_id:
                            st.session_state["voice_id"] = voice_id
                            st.session_state["step2_done"] = True
                            st.success(f"复刻成功！音色ID：{voice_id}")
                            st.rerun()
                        else:
                            st.error(f"复刻失败：{result.get('message', str(result)[:200])}")
                    except Exception as e:
                        st.error(f"复刻出错：{e}")

    with tab2:
        st.markdown("""
        **在电脑上复刻（一次性操作）：**
        1. 点下方按钮打开声音复刻页面
        2. 点击 **「上传音频」**，上传一段 10-20 秒的讲话录音
        3. 等待 1-2 分钟，复制生成的 **音色ID**
        4. 粘贴到下方输入框
        """)
        st.link_button("去百炼控制台复刻声音", "https://bailian.console.aliyun.com/cn-beijing#/efm/model_experience_center/voice?currentTab=voiceTts&secondary=clone&primary=cloning", use_container_width=True)

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
