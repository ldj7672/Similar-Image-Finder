import argparse
from pathlib import Path
from image_clusterer import ImageClusterer

def main():
    parser = argparse.ArgumentParser(description='이미지 임베딩을 기반으로 유사 이미지를 클러스터링합니다.')
    parser.add_argument('--embedding_dir', type=str,
                        default = "results/embeddings",
                        help='임베딩이 저장된 디렉토리 경로'
                        )
    parser.add_argument('--output_dir', type=str,
                        default = "results/outputs",
                        help='클러스터링 결과를 저장할 디렉토리 경로'
                        )
    parser.add_argument('--threshold', type=float,
                        default = 0.94,
                        help='유사도 임계값'
                        )
    parser.add_argument('--config', type=str, default='config/default_config.yaml',
                      help='설정 파일 경로')
    
    args = parser.parse_args()
    
    clusterer = ImageClusterer(config_path=args.config)
    if args.threshold is not None:
        clusterer.threshold = args.threshold
    
    clusterer.cluster_images(args.embedding_dir, args.output_dir)

if __name__ == "__main__":
    main() 