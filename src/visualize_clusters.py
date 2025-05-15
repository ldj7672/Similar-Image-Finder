import argparse
from pathlib import Path
from visualizer import ClusterVisualizer

def main():
    parser = argparse.ArgumentParser(description='클러스터링 결과를 시각화합니다.')
    parser.add_argument('--result_file', type=str,
                        default = "results/outputs/clustering_result_threshold_0.94_20250515_212721.json",
                        help='클러스터링 결과 JSON 파일 경로'
                        )
    parser.add_argument('--image_dir', type=str,
                        default = "sample_data/images",
                        help='원본 이미지가 있는 디렉토리 경로'
                        )
    parser.add_argument('--output_dir', type=str,
                        default = "results/visualization",
                        help='시각화 결과를 저장할 디렉토리 경로'
                        )
    parser.add_argument('--config', type=str, default='config/default_config.yaml',
                      help='설정 파일 경로')
    
    args = parser.parse_args()
    
    visualizer = ClusterVisualizer(config_path=args.config)
    
    # 클러스터 이미지 생성
    visualizer.visualize_clusters(args.result_file, args.image_dir, args.output_dir)
    
if __name__ == "__main__":
    main() 