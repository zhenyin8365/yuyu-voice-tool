# 玉玉的声音工坊

基于阿里云百炼 CosyVoice v3.5-plus 的 AI 语音合成工具。客户填写 API-Key 和复刻音色 ID 即可用专属声音朗读任何文字，支持试听和下载。

## 技术栈

- **前端**：Streamlit（Python）
- **部署**：Streamlit Cloud（免费）
- **语音合成**：阿里云百炼 CosyVoice v3.5-plus REST API
- **声音复刻**：阿里云百炼控制台（一次性操作，免费）

## 页面功能

1. **配置**（填一次，保存到 URL 参数，刷新不丢）
   - 阿里云百炼 API-Key
   - 声音复刻音色 ID
2. **语音合成**
   - 自由输入文字（≤2000字）
   - 7 个快捷模板：电话客服、陪伴闲聊、产品介绍、品牌宣传、节日祝福、日常问候、自我介绍
   - 语速调节（0.8x - 1.5x）
   - 音量调节（0 - 100）
3. **合成结果**
   - 在线播放
   - 一键下载 MP3 到手机
4. **使用说明**
   - 操作指引 + 客服联系方式

## 部署地址

- **线上**：https://zhenyin8365-yuyu-voice-tool-app-3o4pcz.streamlit.app
- **代码**：https://github.com/zhenyin8365/yuyu-voice-tool
- **本地**：~/voice-tool/

## 给新客户部署

1. 在百炼控制台帮客户复刻声音 → 拿到音色 ID
2. 打开部署页面，填好 API-Key 和音色 ID，点「保存配置」
3. 把带参数的链接发给客户（如 `...?key=sk-xxx&voice=cosyvoice-xxx`）
4. 客户打开即用，无需登录、无需安装

## API 调用方式

REST API，非 WebSocket：

```
POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer
Authorization: Bearer {api_key}
Body: {"model":"cosyvoice-v3.5-plus","input":{"text":"...","voice":"xxx","format":"mp3"},"parameters":{"speech_rate":1.0,"volume":80}}

→ 返回音频 URL → GET 下载 → MP3
```

## 费用

- 声音复刻：免费
- 语音合成：1.5 元/万字符（客户的 API-Key 扣费）
