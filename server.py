import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from core.downloader import MusicDownloader

app = FastAPI(
    title="Music Harvester API",
    description="专为 NAS / 个人云打造的高品质音乐抓取与自动化刮削归档服务",
    version="1.0.0"
)

downloader = MusicDownloader(base_dir=os.environ.get("MUSIC_DIR", "/vol2/1000/openclaw/music"))

class DownloadRequest(BaseModel):
    keyword: str
    output_dir: Optional[str] = None

@app.get("/")
def root():
    return {
        "service": "Music Harvester",
        "status": "running",
        "docs_url": "/docs"
    }

@app.post("/api/download")
def download_music(req: DownloadRequest):
    if not req.keyword:
        raise HTTPException(status_code=400, detail="keyword 不能为空")
    
    res = downloader.search_and_download(req.keyword, req.output_dir)
    if not res.get("success"):
        raise HTTPException(status_code=500, detail=res.get("error", "下载失败"))
    
    return {
        "code": 0,
        "message": "success",
        "data": res
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
