# Music Harvester (音乐收割者)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
</p>

专为 NAS / 个人私有云及音乐爱好者打造的**全网高品质音乐抓取与自动化刮削归档工具**。

支持搜索歌曲、歌单链接一键解析，自动下载最高音质音源（FLAC / 320kbps MP3），自动内嵌高清专辑封面、LRC 歌词及 ID3 标签元数据，完美适配 Navidrome / Plex / Jellyfin / 车机播放器。

---

## ✨ 核心特性

- 🎵 **高音质音源解析**：优先匹配 FLAC 无损 / 320kbps 极高音质。
- 🖼️ **全套元数据内嵌**：自动内嵌 ID3v2 标签（歌手、专辑、年份、音轨号）与高清封面。
- 📜 **LRC 同步歌词**：自动生成同名 `.lrc` 动态滚动歌词文件。
- 📁 **规范化结构归档**：支持按 `[音乐库]/[歌手]/[专辑]/[歌名].[ext]` 规范自动分门别类。
- 🌐 **双运行模式**：
  - **CLI 命令行**：支持歌曲名搜索下载、歌单链接批量下载。
  - **RESTful API**：基于 FastAPI，方便接入微信/飞书/TG Bot、快捷指令或网页前端。
- 🐳 **Docker 开箱即用**：提供 Dockerfile、Compose 及全平台多架构预构建镜像。

---

## 📂 归档目录结构

```text
/music/
└── 周杰伦/
    └── 范特西/
        ├── 01. 晴天.flac
        ├── 01. 晴天.lrc
        ├── cover.jpg
        └── album.nfo
```

---

## 🚀 快速上手

### 方式一：Docker Compose 一键运行（推荐）

```yaml
version: '3.8'

services:
  music-harvester:
    image: ghcr.io/foundcodep/music-harvester:latest
    container_name: music-harvester
    restart: unless-stopped
    ports:
      - "8081:8081"
    volumes:
      - /path/to/your/nas/music:/music
    environment:
      - MUSIC_DIR=/music
      - TZ=Asia/Shanghai
```

```bash
docker compose up -d
```

---

### 方式二：本地运行

#### 1. 安装依赖

```bash
git clone https://github.com/Foundcodep/music-harvester.git
cd music-harvester
pip install -r requirements.txt
```

#### 2. 命令行使用

```bash
# 搜索并下载歌曲
python main.py "周杰伦 晴天"

# 指定输出目录
python main.py "陈奕迅 富士山下" -o /path/to/music
```

#### 3. 启动 API 服务

```bash
python server.py
```

API 服务启动在 `http://localhost:8081`，访问 `http://localhost:8081/docs` 查看交互式接口文档。

---

## 📡 API 接口说明

### 1. 搜索歌曲
- **Endpoint**: `GET /api/search`
- **Query**: `keyword`
- **Response**:
```json
{
  "code": 0,
  "data": [
    {
      "id": "123456",
      "title": "晴天",
      "artist": "周杰伦",
      "album": "叶惠美",
      "quality": "FLAC"
    }
  ]
}
```

### 2. 下载并归档歌曲
- **Endpoint**: `POST /api/download`
- **Body**:
```json
{
  "keyword": "周杰伦 晴天",
  "quality": "lossless"
}
```

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。
