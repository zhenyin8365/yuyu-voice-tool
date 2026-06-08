"""
玉玉的声音工坊 — AI语音合成工具（皮肤护理行业）
"""

import streamlit as st
import os

st.set_page_config(page_title="玉玉的声音工坊", page_icon="🎤", layout="centered")

AGNES_KEY = "sk-SfAuFKTIGg8WCkhwRYgVZGhSNazYLgrSbI4dYWrSBsM2RrCK"

POLISH_PROMPT = """你是一位经验丰富的皮肤护理顾问，不是销售。你只负责客观、中立地向客户介绍护理项目本身的情况，不做任何推销、说服或引导购买的行为。

核心任务：用户会给你一段文案，你需要对其进行去广润色。只去掉营销话术和硬广词汇，保留原有的项目信息和内容要点。只做减法不做加法，不要凭空添加原本没有的内容。

绝对禁止出现的词汇：爆款、热销、推荐、首选、必买、划算、便宜、性价比、最好、顶级、完美、秒杀、吊打、赶紧、错过、活动、优惠、特价、促销、打折、赠品、厂家直销、工厂价、卖得火、销量好

语气要自然、平和、亲切，就像皮肤顾问在店里随手给客户介绍一样。直接输出文案，不要任何前缀、后缀或解释。"""

# 从 URL 恢复已保存的配置（刷新不丢）
try:
    qp = st.query_params
    saved_key = qp.get("key", "")
    saved_voice = qp.get("voice", "")
except Exception:
    saved_key = ""
    saved_voice = ""

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
with st.expander("⚙️ 第一步：配置", expanded=(not saved_key)):
    col_a, col_b = st.columns(2)
    with col_a:
        api_key = st.text_input("API-Key", type="password", value=saved_key,
            placeholder="sk-xxxxxxxxxxxxxxxx")
    with col_b:
        voice_id = st.text_input("音色ID", value=saved_voice,
            placeholder="cosyvoice-v3.5-plus-bailian-xxxxxxxx")
    if st.button("💾 保存配置", use_container_width=True):
        if api_key.strip() and voice_id.strip():
            st.query_params["key"] = api_key.strip()
            st.query_params["voice"] = voice_id.strip()
            st.rerun()
        else:
            st.error("请填写完整的 API-Key 和音色ID。")

# ====== 第二步：AI文案生成 ======
st.markdown("<h3 style='color:#c9a0dc'>📝 第二步：AI文案生成</h3>", unsafe_allow_html=True)
st.caption("点击项目按钮，AI 自动生成一段皮肤护理口播文案。")

ai_products = {
    "🔴 祛痘": "帮我写一条抖音短视频口播文案，推广祛痘护理项目。突出专业、温和不刺激、从根源改善痘痘肌。字数80字左右，语气亲切自然。",
    "🟤 祛斑": "帮我写一条抖音短视频口播文案，推广祛斑美白项目。突出科技淡斑、温和不反弹、针对性解决色素沉着。字数80字左右，语气亲切自然。",
    "💧 补水": "帮我写一条抖音短视频口播文案，推广深层补水护理项目。突出水润修复、改善干燥粗糙、做完皮肤像喝饱水。字数80字左右，语气亲切自然。",
    "✨ 亮肤": "帮我写一条抖音短视频口播文案，推广肤色提亮护理项目。突出均匀肤色、去黄气、做完素颜也能打。字数80字左右，语气亲切自然。",
    "🧴 抗敏": "帮我写一条抖音短视频口播文案，推广敏感肌修复护理项目。突出温和舒敏、重建皮肤屏障、适合换季过敏。字数80字左右，语气亲切自然。",
    "⏳ 抗衰": "帮我写一条抖音短视频口播文案，推广抗衰老紧致护理项目。突出胶原再生、淡化细纹、让皮肤更紧致有弹性。字数80字左右，语气亲切自然。",
}

cols = st.columns(6)
for idx, (label, prompt) in enumerate(ai_products.items()):
    with cols[idx % 6]:
        if st.button(label, key=f"ai_{idx}", use_container_width=True):
            with st.spinner(f"AI 正在为你生成{label}口播文案..."):
                try:
                    import requests as req
                    import json as _json
                    ai_payload = {
                        "model": "agnes-2.0-flash",
                        "messages": [
                            {"role": "system", "content": "你是一个专业的抖音皮肤护理口播文案写手。回复只输出文案本身，不加任何解释、引号或前缀。语气要自然，像朋友推荐。"},
                            {"role": "user", "content": prompt},
                        ],
                        "max_tokens": 300,
                    }
                    ai_resp = req.post(
                        "https://apihub.agnes-ai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {AGNES_KEY}",
                            "Content-Type": "application/json; charset=utf-8",
                        },
                        data=_json.dumps(ai_payload, ensure_ascii=False).encode("utf-8"),
                        timeout=30,
                    )
                    if ai_resp.status_code == 200:
                        ai_text = ai_resp.json()["choices"][0]["message"]["content"].strip()
                        st.session_state["template_text"] = ai_text
                        st.rerun()
                    else:
                        st.error(f"AI 生成失败：{ai_resp.text[:150]}")
                except Exception as e:
                    st.error(f"AI 生成失败：{e}")

# ====== 第三步：语音合成 ======
st.markdown("<h3 style='color:#c9a0dc'>🎙️ 第三步：语音合成</h3>", unsafe_allow_html=True)

text = st.text_area("输入要合成的文字", height=180,
    value=st.session_state.get("template_text", ""),
    placeholder="在这里输入你想说的话，或点击上方 AI 按钮自动生成，或点击下方模板快速填充。",
    max_chars=2000)

tc1, tc2 = st.columns(2)
with tc1:
    st.caption(f"{len(text)} / 2000 字")
with tc2:
    polish_clicked = st.button("✨ 去广润色", key="polish", use_container_width=True,
        help="把营销文案转为纯讲解风格，去掉硬广和推销话术")

if polish_clicked:
    if not text.strip():
        st.error("请先输入要润色的文案。")
    else:
        with st.spinner("AI 正在润色文案..."):
            try:
                import requests as req2
                import json as _json3
                polish_payload = {
                    "model": "agnes-2.0-flash",
                    "messages": [
                        {"role": "system", "content": POLISH_PROMPT},
                        {"role": "user", "content": f"请对以下文案进行去广润色，去掉营销话术和硬广词汇，保留原有的护理项目信息和内容要点，只做减法不做加法，不要添加原本没有的内容：\n\n{text.strip()}"},
                    ],
                    "max_tokens": 600,
                }
                polish_resp = req2.post(
                    "https://apihub.agnes-ai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {AGNES_KEY}",
                        "Content-Type": "application/json; charset=utf-8",
                    },
                    data=_json3.dumps(polish_payload, ensure_ascii=False).encode("utf-8"),
                    timeout=30,
                )
                if polish_resp.status_code == 200:
                    polished = polish_resp.json()["choices"][0]["message"]["content"].strip()
                    st.session_state["template_text"] = polished
                    st.rerun()
                else:
                    st.error(f"润色失败：{polish_resp.text[:150]}")
            except Exception as e:
                st.error(f"润色失败：{e}")

# 快捷模板
st.caption("💡 快捷模板（点击自动填入）：")
templates = {
    "📞 到店咨询": "您好，欢迎来到玉玉皮肤护理。我是玉玉，今天可以帮您看看皮肤状况，根据您的情况推荐合适的护理方案。",
    "💬 日常问候": "早上好呀，新的一天开始了。记得给皮肤补补水哦，灵山天气热皮肤更需要护理，有空来店里坐坐。",
    "🛍️ 项目介绍": "这是我们店里最受欢迎的深层清洁项目，先检测皮肤再针对护理，做完脸上干净透亮，很多客户做完都说舒服。",
    "💼 术后提醒": "刚做完护理的姐妹注意了，今天回去多敷面膜多喝水，不要吃辣，明天睡醒皮肤状态会更好哦。",
    "🎉 活动通知": "姐妹们这个月我们店搞活动，老客户带新朋友来可以享受两人同行一人免单，具体项目可以微信问我。",
    "🎙️ 自我介绍": "大家好，我是玉玉，做皮肤护理这么多年，最开心的就是看到客户皮肤一步步改善。有什么皮肤问题都可以来找我聊聊。",
}
cols = st.columns(3)
for i, (label, sample) in enumerate(templates.items()):
    with cols[i % 3]:
        if st.button(label, key=f"tmpl_{i}", use_container_width=True):
            st.session_state["template_text"] = sample
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
                import requests
                import json as _json4

                payload = {
                    "model": "cosyvoice-v3.5-plus",
                    "input": {
                        "text": text,
                        "voice": voice_id.strip(),
                        "format": "mp3",
                    },
                    "parameters": {
                        "rate": speed,
                        "volume": volume,
                    },
                }
                resp = requests.post(
                    "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer",
                    headers={
                        "Authorization": f"Bearer {api_key.strip()}",
                        "Content-Type": "application/json; charset=utf-8",
                    },
                    data=_json4.dumps(payload, ensure_ascii=False).encode("utf-8"),
                    timeout=60,
                )

                if resp.status_code != 200:
                    st.error(f"合成失败：HTTP {resp.status_code} - {resp.text[:200]}")
                else:
                    result = resp.json()
                    audio_url = result.get("output", {}).get("audio", {}).get("url", "")
                    if not audio_url:
                        st.error(f"未获取到音频链接：{resp.text[:200]}")
                    else:
                        audio_resp = requests.get(audio_url, timeout=30)
                        audio = audio_resp.content
                        audio_size = len(audio) / 1024
                        st.markdown("---")
                        st.markdown("<h3 style='color:#c9a0dc'>🔊 合成结果</h3>", unsafe_allow_html=True)
                        st.markdown(f"<div class='audio-box'>"
                            f"<span class='pill'>语速 {speed}x</span>"
                            f"<span class='pill'>{len(text)} 字</span>"
                            f"<span class='pill'>{audio_size:.0f} KB</span>"
                            f"</div>", unsafe_allow_html=True)
                        st.audio(audio, format="audio/mp3")
                        st.download_button("📥 下载到手机", data=audio, file_name="玉玉的声音.mp3",
                            mime="audio/mpeg", use_container_width=True)
                        st.toast("合成完成！", icon="✅")
            except Exception as e:
                st.error(f"合成失败：{e}")

# ====== 使用说明 ======
with st.expander("📖 使用说明"):
    st.markdown("**怎么用**")
    st.markdown("1. 填写 API-Key 和音色ID（润锋提供，填一次即可）")
    st.markdown("2. 点击项目按钮 AI 自动生成文案，或直接输入文字")
    st.markdown("3. 文案太硬的话点「去广润色」去掉推销话术")
    st.markdown("4. 选择语速，点击「开始合成」")
    st.markdown("5. 试听满意后点「下载到手机」")
    st.markdown("")
    st.markdown("**关于你的声音**")
    st.markdown("你的专属声音已经预先训练好了，输入任何文字都会用你的声音朗读出来。")
    st.markdown("")
    st.markdown("如遇到合成失败或任何问题，请联系 **润锋 13307871670**。")

st.markdown("---")
st.markdown("<p style='text-align:center;color:#9b8ab8;font-size:12px;margin-top:30px'>Powered by <b>润锋 AI</b> · 让每个声音都被听见</p>", unsafe_allow_html=True)
