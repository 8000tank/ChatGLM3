import os
import requests
import tarfile
from pathlib import Path
from tqdm import tqdm


def download_file(url: str, save_path: str):
    """下载文件并显示进度条"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(save_path, 'wb') as file, tqdm(
        desc=f"下载 {Path(save_path).name}",
        total=total_size,
        unit='iB',
        unit_scale=True
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            pbar.update(size)


def extract_tar(tar_path: str, extract_path: str):
    """解压tar.gz文件并显示进度"""
    with tarfile.open(tar_path, 'r:gz') as tar:
        members = tar.getmembers()
        with tqdm(desc=f"解压 {Path(tar_path).name}", total=len(members)) as pbar:
            for member in members:
                tar.extract(member, extract_path)
                pbar.update(1)


def main():
    # 创建必要的目录
    current_dir = Path(__file__).parent
    data_dir = current_dir / 'data'
    data_dir.mkdir(exist_ok=True)

    # 下载文件
    url = "https://cloud.tsinghua.edu.cn/f/b3f119a008264b1cabd1/?dl=1"
    tar_path = data_dir / "AdvertiseGen.tar.gz"

    if not tar_path.exists():
        print("开始下载数据集...")
        download_file(url, str(tar_path))

    # 解压文件
    extract_path = data_dir
    if not (extract_path / "AdvertiseGen").exists():
        print("开始解压数据集...")
        extract_tar(str(tar_path), str(extract_path))

    # 清理tar.gz文件
    tar_path.unlink()
    print("数据集准备完成!")


if __name__ == "__main__":
    main()
