import torch
import numpy as np
from PIL import Image
from pathlib import Path
from tqdm import tqdm
from transformers import CLIPProcessor, CLIPModel
import yaml
import os

class CLIPEncoder:
    def __init__(self, config_path="config/default_config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.device = self._get_device()
        self.model = CLIPModel.from_pretrained(self.config['model']['name']).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(self.config['model']['name'])
        
    def _get_device(self):
        device_config = self.config['model']['device']
        if device_config == "auto":
            if torch.cuda.is_available():
                return "cuda"
            elif torch.backends.mps.is_available():
                return "mps"
            return "cpu"
        return device_config
    
    def encode_image(self, image_path):
        """단일 이미지의 임베딩을 생성합니다."""
        try:
            image = Image.open(image_path).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                image_embeds = self.model.get_image_features(**inputs)
            
            return torch.nn.functional.normalize(image_embeds, p=2, dim=-1).cpu().numpy()
        except Exception as e:
            print(f"이미지 처리 오류 ({image_path}): {e}")
            return None
    
    def encode_directory(self, image_dir, output_dir):
        """디렉토리 내의 모든 이미지에 대한 임베딩을 생성합니다."""
        image_dir = Path(image_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        image_files = []
        for ext in self.config['image']['supported_formats']:
            image_files.extend(list(image_dir.glob(f"*{ext}")))
        
        print(f"총 {len(image_files)}개의 이미지를 처리합니다.")
        
        for img_file in tqdm(image_files, desc="CLIP 임베딩 생성 중"):
            embedding = self.encode_image(img_file)
            if embedding is not None:
                output_path = output_dir / f"{img_file.stem}.npy"
                np.save(output_path, embedding)
        
        print(f"✅ 임베딩 생성이 완료되었습니다. 저장 위치: {output_dir}") 