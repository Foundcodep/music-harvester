import os
import re
import requests
import json
from typing import Optional, Dict, Any
from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC, USLT

class MusicDownloader:
    def __init__(self, base_dir: str = "/vol2/1000/openclaw/music"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def clean_name(self, name: str) -> str:
        return re.sub(r'[\\/:*?"<>|]', '_', name).strip()

    def search_and_download(self, keyword: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        根据关键词搜索并下载无损/高品质音乐，自动刮削元数据与歌词
        """
        target_dir = output_dir or self.base_dir
        print(f"[*] 正在搜索音乐: {keyword}")

        # 使用网易云公开检索接口获取音源信息
        search_url = f"https://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={requests.utils.quote(keyword)}&type=1&offset=0&total=true&limit=1"
        try:
            resp = requests.get(search_url, headers=self.headers, timeout=10)
            data = resp.json()
            songs = data.get("result", {}).get("songs", [])
            if not songs:
                return {"success": False, "error": f"未找到与 '{keyword}' 相关的歌曲"}

            song = songs[0]
            song_id = song["id"]
            title = self.clean_name(song.get("name", "Unknown Title"))
            artist = self.clean_name(song.get("artists", [{}])[0].get("name", "Unknown Artist"))
            album = self.clean_name(song.get("album", {}).get("name", "Unknown Album"))
            cover_url = song.get("album", {}).get("picUrl", "")

            # 目录组织：[输出目录]/[歌手]/[专辑]/
            album_dir = os.path.join(target_dir, artist, album)
            os.makedirs(album_dir, exist_ok=True)

            audio_file = os.path.join(album_dir, f"{title}.mp3")
            lrc_file = os.path.join(album_dir, f"{title}.lrc")
            cover_file = os.path.join(album_dir, "cover.jpg")

            # 1. 获取音源并下载
            stream_url = f"https://music.163.com/song/media/outer/url?id={song_id}.mp3"
            r = requests.get(stream_url, headers=self.headers, stream=True, timeout=15)
            if r.status_code == 200:
                with open(audio_file, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            else:
                return {"success": False, "error": "音源下载失败"}

            # 2. 下载歌词
            lrc_url = f"https://music.163.com/api/song/lyric?os=pc&id={song_id}&lv=-1&kv=-1&tv=-1"
            lrc_text = ""
            try:
                lrc_resp = requests.get(lrc_url, headers=self.headers, timeout=5).json()
                lrc_text = lrc_resp.get("lrc", {}).get("lyric", "")
                if lrc_text:
                    with open(lrc_file, "w", encoding="utf-8") as f:
                        f.write(lrc_text)
            except Exception as e:
                print(f"[!] 歌词获取跳过: {e}")

            # 3. 下载封面
            cover_data = None
            if cover_url:
                try:
                    c_resp = requests.get(cover_url, headers=self.headers, timeout=10)
                    if c_resp.status_code == 200:
                        cover_data = c_resp.content
                        with open(cover_file, "wb") as f:
                            f.write(cover_data)
                except Exception as e:
                    print(f"[!] 封面下载跳过: {e}")

            # 4. 写入 ID3 标签
            try:
                audio = ID3(audio_file)
            except Exception:
                audio = ID3()

            audio.add(TIT2(encoding=3, text=title))
            audio.add(TPE1(encoding=3, text=artist))
            audio.add(TALB(encoding=3, text=album))
            if lrc_text:
                audio.add(USLT(encoding=3, lang="chi", desc="Lyric", text=lrc_text))
            if cover_data:
                audio.add(APIC(
                    encoding=3,
                    mime="image/jpeg",
                    type=3,
                    desc="Cover",
                    data=cover_data
                ))
            audio.save(audio_file)

            return {
                "success": True,
                "title": title,
                "artist": artist,
                "album": album,
                "file_path": audio_file,
                "lrc_path": lrc_file if os.path.exists(lrc_file) else None,
                "cover_path": cover_file if os.path.exists(cover_file) else None
            }

        except Exception as e:
            return {"success": False, "error": str(e)}
