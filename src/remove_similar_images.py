import argparse
import json
from pathlib import Path
import os
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def remove_similar_images(result_file, image_dir, keep_first=True):
    """
    클러스터링 결과를 기반으로 유사한 이미지를 제거합니다.
    
    Args:
        result_file (str): 클러스터링 결과 JSON 파일 경로
        image_dir (str): 원본 이미지가 있는 디렉토리
        keep_first (bool): True면 클러스터의 첫 번째 이미지를 유지, False면 마지막 이미지를 유지
    """
    logger = setup_logging()
    
    # 디렉토리 설정
    image_dir = Path(image_dir)
    
    # JSON 파일 읽기
    with open(result_file, 'r', encoding='utf-8') as f:
        result = json.load(f)
    
    total_removed = 0
    total_clusters = len(result['clusters'])
    
    logger.info(f"총 {total_clusters}개의 클러스터에서 유사 이미지 제거를 시작합니다.")
    
    # 각 클러스터 처리
    for cluster_idx, cluster in enumerate(result['clusters'], 1):
        if len(cluster) <= 1:
            continue
            
        # 대표 이미지 선택 (첫 번째 또는 마지막)
        representative_idx = 0 if keep_first else -1
        representative = cluster[representative_idx]
        
        # 나머지 유사 이미지들을 삭제
        for img_name in cluster:
            if img_name == representative:
                continue
                
            # 이미지 파일 찾기
            for ext in ['.jpg', '.jpeg', '.png']:
                img_path = image_dir / f"{img_name}{ext}"
                if img_path.exists():
                    # 이미지 삭제
                    os.remove(str(img_path))
                    total_removed += 1
                    logger.debug(f"유사 이미지 삭제: {img_path}")
                    break
    
    logger.info(f"유사 이미지 제거가 완료되었습니다.")
    logger.info(f"총 {total_removed}개의 유사 이미지가 삭제되었습니다.")

def main():
    parser = argparse.ArgumentParser(description='클러스터링 결과를 기반으로 유사한 이미지를 제거합니다.')
    parser.add_argument('--result_file', type=str, 
                        default = "results/outputs/clustering_result_threshold_0.94_20250515_151708.json",
                        help='클러스터링 결과 JSON 파일 경로'
                        )
    parser.add_argument('--image_dir', type=str,
                        default = "sample_data/images",
                        help='원본 이미지가 있는 디렉토리 경로'
                        )
    parser.add_argument('--keep_first', action='store_true',
                        default = True,
                        help='클러스터의 첫 번째 이미지를 유지'
                        )
    
    args = parser.parse_args()
    remove_similar_images(args.result_file, args.image_dir, args.keep_first)

if __name__ == "__main__":
    main() 