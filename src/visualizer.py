import json
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image
import math
import yaml
import logging

class ClusterVisualizer:
    def __init__(self, config_path="config/default_config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # 로깅 설정
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def create_collage(self, image_paths, output_path, max_width=2000):
        """이미지들을 가로로 이어붙여서 하나의 이미지로 만듭니다."""
        images = []
        for img_path in image_paths:
            try:
                if img_path.exists():
                    img = Image.open(img_path)
                    self.logger.debug(f"이미지 로드 성공: {img_path}, 크기: {img.size}")
                    images.append(img)
                else:
                    self.logger.warning(f"이미지를 찾을 수 없음: {img_path}")
            except Exception as e:
                self.logger.error(f"이미지 처리 중 오류 발생 ({img_path}): {e}")
        
        if not images:
            self.logger.warning("처리할 이미지가 없습니다.")
            return
        
        # 모든 이미지의 높이를 동일하게 맞춤
        target_height = 300  # 고정된 높이 설정
        resized_images = []
        for img in images:
            try:
                # 이미지 비율 유지하면서 크기 조정
                ratio = target_height / img.height
                new_width = int(img.width * ratio)
                resized = img.resize((new_width, target_height), Image.Resampling.LANCZOS)
                resized_images.append(resized)
                self.logger.debug(f"이미지 리사이즈 완료: {img_path}, 새 크기: {resized.size}")
            except Exception as e:
                self.logger.error(f"이미지 리사이즈 중 오류 발생: {e}")
        
        if not resized_images:
            self.logger.error("리사이즈된 이미지가 없습니다.")
            return
        
        # 이미지들을 가로로 이어붙임
        total_width = sum(img.width for img in resized_images)
        if total_width > max_width:
            # 너무 길면 여러 줄로 나눔
            images_per_row = math.ceil(math.sqrt(len(resized_images)))
            rows = math.ceil(len(resized_images) / images_per_row)
            collage = Image.new('RGB', (max_width, target_height * rows))
            
            x, y = 0, 0
            for img in resized_images:
                if x + img.width > max_width:
                    x = 0
                    y += target_height
                collage.paste(img, (x, y))
                x += img.width
                self.logger.debug(f"이미지 붙이기 완료: 위치 ({x}, {y})")
        else:
            collage = Image.new('RGB', (total_width, target_height))
            x = 0
            for img in resized_images:
                collage.paste(img, (x, 0))
                x += img.width
                self.logger.debug(f"이미지 붙이기 완료: 위치 ({x}, 0)")
        
        try:
            collage.save(output_path, quality=95)
            self.logger.info(f"콜라주 저장 완료: {output_path}")
        except Exception as e:
            self.logger.error(f"콜라주 저장 중 오류 발생: {e}")
    
    def visualize_clusters(self, result_file, image_dir, output_dir=None):
        """클러스터링 결과를 시각화합니다."""
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
            
            if output_dir is None:
                output_dir = Path(self.config['output']['visualization_dir'])
            else:
                output_dir = Path(output_dir)
                
            output_dir.mkdir(parents=True, exist_ok=True)
            
            image_dir = Path(image_dir)
            clusters = result['clusters']
            
            self.logger.info(f"\n=== 클러스터 시각화 시작 ===")
            self.logger.info(f"총 {len(clusters)}개의 클러스터를 처리합니다.")
            
            for cluster_idx, cluster in enumerate(clusters, 1):
                image_paths = []
                for img_name in cluster:
                    for ext in self.config['image']['supported_formats']:
                        img_path = image_dir / f"{img_name}{ext}"
                        if img_path.exists():
                            image_paths.append(img_path)
                            break
                
                if image_paths:
                    output_path = output_dir / f"cluster_{cluster_idx:03d}.jpg"
                    self.logger.info(f"클러스터 {cluster_idx} 처리 중: {len(image_paths)}개 이미지")
                    self.create_collage(image_paths, output_path)
                    self.logger.info(f"클러스터 {cluster_idx} 처리 완료")
                else:
                    self.logger.warning(f"클러스터 {cluster_idx}에 이미지가 없습니다.")
            
            self.logger.info(f"\n시각화가 완료되었습니다. 결과 위치: {output_dir}")
            
        except Exception as e:
            self.logger.error(f"시각화 중 오류 발생: {e}")
            raise
