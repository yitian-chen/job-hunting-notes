import subprocess
import sys
from pathlib import Path

VIDEOS = [
    "由里健康.mp4",
    "爱学习 一面.mp4",
]


def extract_audio(video_path: str) -> bool:
    video = Path(video_path)
    if not video.exists():
        print(f"[跳过] 文件不存在: {video_path}")
        return False

    output = video.with_suffix(".mp3")
    print(f"[提取] {video.name} -> {output.name}")

    result = subprocess.run(
        [
            "ffmpeg",
            "-i", str(video),
            "-vn",                # 不要视频流
            "-acodec", "libmp3lame",
            "-q:a", "2",          # 高质量 (~190kbps VBR)
            "-y",                 # 覆盖已存在的输出文件
            str(output),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(f"[完成] {output.name}")
        return True
    else:
        print(f"[失败] {video.name}: {result.stderr[-300:]}")
        return False


def main():
    success = 0
    for video in VIDEOS:
        if extract_audio(video):
            success += 1
    print(f"\n成功: {success}/{len(VIDEOS)}")
    sys.exit(0 if success == len(VIDEOS) else 1)


if __name__ == "__main__":
    main()
