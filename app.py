"""
玉玉的声音工坊 — AI语音合成工具（皮肤护理行业）
"""

import streamlit as st
import os

st.set_page_config(page_title="玉玉的声音工坊", page_icon="🎤", layout="centered")

AGNES_KEY = "sk-SfAuFKTIGg8WCkhwRYgVZGhSNazYLgrSbI4dYWrSBsM2RrCK"

POLISH_PROMPT = """你是一位经验丰富的皮肤护理顾问，不是销售。你只负责客观、中立地向客户介绍护理项目本身的情况，不做任何推销、说服或引导购买的行为。

核心任务：用户会给你一段文案，你需要对其进行去广润色。只去掉营销话术和硬广词汇，保留原有的项目信息和内容要点。只做减法不做加法，不要凭空添加原本没有的内容。

必须用安全词汇替换以下所有禁用词：

【效果承诺→安全替代】祛痘/去痘/消痘→皮肤洁净管理/清爽护理。祛斑/去斑/淡斑→肤色均匀护理/亮泽管理。祛皱/去皱/除皱→皮肤紧致护理/平滑管理。祛黄/去黄→提亮肤色/焕亮气色。祛黑/去黑→肤色提亮。美白/变白/焕白→肤色提亮/养出好气色。祛水肿/去水肿→面部线条管理。瘦脸/小脸/V脸→面部轮廓护理。提拉/提升/拉皮→皮肤紧实感。嫩肤/换肤/婴儿肌→皮肤质感变好。逆龄/冻龄→保持好状态。一次见效/当场/瞬间/立竿见影→坚持护理/慢慢调理。永久/不再→持续养护。根除/根治/彻底→持续管理。包好/保证/绝对→用心做。特效/奇效/神效→专业护理。排毒/排激素→深层清洁/让皮肤更干净。

【医疗术语→安全替代】治疗/医治→照护/打理。治愈/痊愈→皮肤状态变好。疗程/治疗周期→护理周期。疗效/药效→护理效果。处方/秘方→护理方案。消炎/杀菌/抗菌→洁净清爽。抗敏/脱敏→皮肤更舒服。抗痘/抗斑/抗皱/抗衰老→日常照护。消肿/镇痛/止痒→舒缓。激素/无激素→温和配方。药用/药妆/械字号→专业护理产品。

【皮肤问题→安全替代】痘痘/青春痘→皮肤偶尔的状况。痘印/痘疤/痘坑→皮肤表面不够平滑。粉刺/痤疮/闭口→皮肤不够清爽。黑头/白头/脂肪粒→皮肤不够干净。毛孔粗大/草莓鼻→皮肤不够细腻。色斑/雀斑/黄褐斑→肤色不均匀。暗沉/发黄/发灰→气色不够好。粗糙/起皮→皮肤不够细腻。油腻/大油田→皮肤偏油。干燥/缺水/脱皮→皮肤偏干。敏感/过敏/刺痛/红肿→皮肤容易不舒服。红血丝/毛细血管扩张→脸上容易泛红。激素脸→皮肤需要养护。烂脸→皮肤状态不太好。松弛/下垂/法令纹→皮肤不够紧实。眼袋/泪沟/黑眼圈→眼部状态不太好。老/显老/年龄感→状态不够好。

【医美擦边→安全替代】水光针/水光→水润护理。玻尿酸注射→皮肤充盈护理。肉毒素/瘦脸针→面部肌肉放松护理。线雕/埋线→皮肤提拉护理。激光/点阵激光→科技照护。皮秒/超皮秒→色素管理。光子/IPL→光线照护。微针/黄金微针→细微护理。刷酸/果酸/水杨酸→角质管理。填充/注射/打针→让皮肤更饱满。热玛吉/超声刀→皮肤紧实护理。整形/医美/微整→日常皮肤管理。美白针/美白丸→肤色提亮护理。

【科学背书→安全替代】医学研究/临床验证→经验积累。医生推荐/皮肤科医生→客户选择/同行认可。专利/独家技术→自有方法。纳米/量子/分子/细胞→细微周到。诺贝尔/国际大奖→用心做的方案。

【促销诱导→安全替代】免费/0元→欢迎来了解。限时/限量/抢/秒杀→最近。名额/仅剩→可以安排时间。扫码/加微信/私信→可以来找我。下单/购买/付款→确定来。便宜/特价/白菜价→了解一下。划算/太值了→用心做。好评/零差评→客户挺喜欢的。爆款/热销/卖爆→很多客户选这个。

【对比拉踩→安全替代】对比图/前后对比→看看变化。秒杀/吊打/碾压→有自己的特色。别家/其他店→不同方式。最好/第一/排名→用心做。

【焦虑制造→安全替代】丑/难看/吓人→状态可以更好。自卑/不敢见人→状态好人也精神。老了十岁/大妈感→状态保持得更好。不保养就完了→日常照护很重要。

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
    "🧹 洁净管理": "帮我写一条抖音短视频口播文案，推广皮肤洁净管理项目。突出专业、清爽、让皮肤状态更稳定。字数80字左右，语气亲切自然。严格遵守抖音规范：不说效果承诺、不说医疗术语、不制造容貌焦虑。",
    "✨ 肤色调理": "帮我写一条抖音短视频口播文案，推广肤色调理项目。突出肤色均匀、气色提亮、用心照护让皮肤看起来更干净。字数80字左右，语气亲切自然。严格遵守抖音规范。",
    "💧 水润管理": "帮我写一条抖音短视频口播文案，推广皮肤水润管理项目。突出充分滋润、皮肤水润饱满、做完感觉很舒服。字数80字左右，语气亲切自然。严格遵守抖音规范。",
    "🌟 气色焕新": "帮我写一条抖音短视频口播文案，推广气色焕新护理项目。突出肤色均匀、让皮肤看起来更有光泽、素颜也有好状态。字数80字左右，语气亲切自然。严格遵守抖音规范。",
    "🤲 舒缓照护": "帮我写一条抖音短视频口播文案，推广皮肤舒缓照护项目。突出皮肤更舒服、细心打理、适合换季。字数80字左右，语气亲切自然。严格遵守抖音规范。",
    "🧘 紧致护理": "帮我写一条抖音短视频口播文案，推广皮肤紧致护理项目。突出皮肤饱满感、照护细纹、让轮廓更清晰。字数80字左右，语气亲切自然。严格遵守抖音规范。",
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

st.caption("⏱️ AI智能调整字数（根据已有文案扩写或精简）：")
dur_cols = st.columns(4)
durations = {"30秒 ≈ 80字": 80, "60秒 ≈ 160字": 160, "120秒 ≈ 320字": 320, "180秒 ≈ 500字": 500}
for i, (label, target_chars) in enumerate(durations.items()):
    with dur_cols[i]:
        if st.button(label, key=f"dur_{i}", use_container_width=True):
            current_text = st.session_state.get("template_text", "")
            if not current_text.strip():
                st.error("请先生成或输入文案。")
            else:
                if len(current_text) > target_chars:
                    action = f"精简到{target_chars}字"
                    prompt = f"请将以下文案精简到{target_chars}字左右，保留核心信息和卖点，去掉重复和啰嗦的内容。直接输出精简后的文案，不要任何解释：\n\n{current_text}"
                else:
                    action = f"扩写到{target_chars}字"
                    prompt = f"请将以下文案扩写到{target_chars}字左右，补充细节、场景描述和自然过渡，保持原有风格和核心信息不变。直接输出扩写后的文案，不要任何解释：\n\n{current_text}"
                with st.spinner(f"AI 正在{action}..."):
                    try:
                        import requests as req3
                        import json as _json5
                        ai_payload = {
                            "model": "agnes-2.0-flash",
                            "messages": [
                                {"role": "system", "content": "你是一个专业的短视频口播文案写手。根据用户要求精简或扩写文案，保持原有风格和信息。严格遵守抖音内容规范，不使用任何营销话术、医疗术语和效果承诺。直接输出文案，不要任何解释。"},
                                {"role": "user", "content": prompt},
                            ],
                            "max_tokens": 800,
                        }
                        ai_resp = req3.post(
                            "https://apihub.agnes-ai.com/v1/chat/completions",
                            headers={
                                "Authorization": f"Bearer {AGNES_KEY}",
                                "Content-Type": "application/json; charset=utf-8",
                            },
                            data=_json5.dumps(ai_payload, ensure_ascii=False).encode("utf-8"),
                            timeout=45,
                        )
                        if ai_resp.status_code == 200:
                            result_text = ai_resp.json()["choices"][0]["message"]["content"].strip()
                            st.session_state["template_text"] = result_text
                            st.rerun()
                        else:
                            st.error(f"AI 调整失败：{ai_resp.text[:150]}")
                    except Exception as e:
                        st.error(f"AI 调整失败：{e}")

tc1, tc2 = st.columns([1.5, 1])
with tc1:
    st.caption(f"当前 {len(text)} / 2000 字")
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
    "📞 到店了解": "您好，欢迎来到玉玉皮肤管理。我是玉玉，今天可以帮您看看皮肤状态，根据您的情况搭配适合的护理方式。",
    "💬 日常问候": "早上好呀，新的一天开始了。灵山天气热记得给皮肤多滋润一下，有空来店里坐坐聊天。",
    "🛍️ 护理介绍": "这是我们店里很受欢迎的一个项目，做完脸上干净透亮，摸起来滑滑的，很多客户做完都说感觉很舒服。",
    "💼 护理后提醒": "刚做完护理的姐妹注意了，今天回去多喝水、早点休息，明天睡醒状态会更好哦。",
    "🎉 老友福利": "姐妹们这个月过来有惊喜，带闺蜜一起来有双人福利，具体可以来找我了解。",
    "🎙️ 自我介绍": "大家好，我是玉玉，做皮肤管理好多年了，最开心的就是看到客户的状态一天比一天好。有什么想了解的都可以来找我聊聊。",
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
                        st.warning("⚠️ 音频不会自动保存！刷新页面、切走页面或关闭浏览器后音频就会消失，请马上点上方按钮下载到手机。")
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
