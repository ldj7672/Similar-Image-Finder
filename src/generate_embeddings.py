import argparse
from pathlib import Path
from clip_encoder import CLIPEncoder

def main():
    parser = argparse.ArgumentParser(description='CLIP 모델을 사용하여 이미지 임베딩을 생성합니다.')
    parser.add_argument('--image_dir', type=str, 
                        default = "sample_data/images",
                        help='이미지가 있는 디렉토리 경로'
                        )
    parser.add_argument('--output_dir', type=str,
                        default = "results/embeddings",
                        help='임베딩을 저장할 디렉토리 경로'
                        )
    parser.add_argument('--config', type=str, default='config/default_config.yaml',
                      help='설정 파일 경로')
    
    args = parser.parse_args()
    
    encoder = CLIPEncoder(config_path=args.config)
    encoder.encode_directory(args.image_dir, args.output_dir)

if __name__ == "__main__":
    main() 