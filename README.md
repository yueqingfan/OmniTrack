# 🎥 OmniTrack安全监控与异常行为检测系统

## 🌟 项目简介

本项目是一个结合目标检测与异常行为识别的智能监控系统，可以实时分析视频流，识别 打架、盗窃、爆炸、火灾 等异常行为，并触发告警。
支持摄像头监控及本地视频上传，实时检测视频中的异常行为

## 🔧 功能特点

✅ 实时摄像头监控
✅ 本地视频上传
✅ 异常行为检测（如打架、盗窃、枪击、火灾、爆炸等）
✅ 实时告警（声音、截图保存、报警日志记录）
✅ 多视频源切换，状态重置重新分析
✅ WebSocket 实时通信

## 🚀 快速启动

1️⃣ 克隆项目
git clone https://github.com/yueqingfan/OmniTrack
cd OmniTrack

2️⃣ 安装依赖

cd frontend(前端)

npm install

3️⃣ 启动前端

npm run serve

4️⃣ 启动后端

mvn spring-boot:run

5️⃣ 访问页面
浏览器打开：
http://localhost:8080

## 🛠️ 技术栈

前端
🎯 Vue 3
后端

🔥 Spring Boot 3.4.3 (Java 21)
🔥 MySQL 数据库 (数据库名: omnitrackdb)

视频分析与检测

🔍 OpenCV（视频帧处理）
🔍 YOLOv8 （目标检测）
🔍 LSTM(行为识别)

## 📌 配置说明

🎥 切换视频源
支持以下视频源：

camera（摄像头实时监控）
local（本地视频上传）

## 🔥 异常行为识别分类

系统内置了以下行为分类逻辑，支持后续扩展：
打架、
盗窃、
枪击、
火灾、
爆炸、
虐待

## 🛠️ 未来计划

多摄像头支持

多路视频流同时分析

云端异常事件存储与回溯

移动端适配

## 💪 贡献指南

欢迎提出 Issue 或 PR 来一起改进项目 🎉

Fork 项目
创建新分支 (git checkout -b feature/your-feature)
提交修改 (git commit -m 'Add your feature')
推送分支 (git push origin feature/your-feature)
创建 Pull Request 🚀
🎉 鸣谢
感谢所有开源项目提供的灵感与支持 🙌

如果你喜欢这个项目，别忘了点个 ⭐️ Star 支持一下！**