import argparse
import sys
from core.downloader import MusicDownloader

def main():
    parser = argparse.ArgumentParser(description="全网高品质音乐抓取与自动化刮削归档工具")
    parser.add_argument("keyword", help="歌曲名称 / 歌手 + 歌曲名 (例如: '周杰伦 晴天')")
    parser.add_argument("-o", "--output", default=None, help="自定义输出目录路径")
    
    args = parser.parse_args()
    downloader = MusicDownloader()
    
    res = downloader.search_and_download(args.keyword, args.output)
    if res.get("success"):
        print("\n✅ 下载与刮削完成！")
        print(f"🎵 歌曲：{res.get('title')}")
        print(f"👤 歌手：{res.get('artist')}")
        print(f"💿 专辑：{res.get('album')}")
        print(f"📁 音频路径：{res.get('file_path')}")
        if res.get('lrc_path'):
            print(f"📜 歌词路径：{res.get('lrc_path')}")
        if res.get('cover_path'):
            print(f"🖼️ 封面路径：{res.get('cover_path')}")
    else:
        print(f"\n❌ 下载失败: {res.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
