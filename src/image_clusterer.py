import numpy as np
from pathlib import Path
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import json
from datetime import datetime
import yaml

class ImageClusterer:
    def __init__(self, config_path="config/default_config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.threshold = self.config['clustering']['threshold']
        self.batch_size = self.config['clustering']['batch_size']
    
    def process_batch(self, embeddings_batch, filenames_batch):
        """배치 단위로 유사 이미지 클러스터링을 수행합니다."""
        similarity_matrix = cosine_similarity(embeddings_batch)
        num_images = len(embeddings_batch)
        
        edges = []
        for i in range(num_images):
            for j in range(i + 1, num_images):
                if similarity_matrix[i, j] > self.threshold:
                    edges.append((i, j))
        
        G = nx.Graph()
        G.add_nodes_from(range(num_images))
        G.add_edges_from(edges)
        components = list(nx.connected_components(G))
        
        clusters = []
        for group in components:
            group = sorted(list(group))
            if len(group) > 1:  # 유사 이미지가 2개 이상인 경우만 클러스터로 저장
                clusters.append([filenames_batch[idx] for idx in group])
        
        return clusters
    
    def cluster_images(self, embedding_dir, output_dir=None):
        """디렉토리 내의 모든 이미지 임베딩에 대해 클러스터링을 수행합니다."""
        embedding_dir = Path(embedding_dir)
        embedding_files = sorted(list(embedding_dir.glob("*.npy")))
        
        if output_dir is None:
            output_dir = Path(self.config['output']['result_dir'])
        else:
            output_dir = Path(output_dir)  # 문자열을 Path 객체로 변환
            
        output_dir.mkdir(parents=True, exist_ok=True)
        
        all_clusters = []
        total_images = len(embedding_files)
        
        for i in tqdm(range(0, total_images, self.batch_size), desc="배치 처리 중"):
            batch_files = embedding_files[i:i + self.batch_size]
            batch_embeddings = []
            batch_filenames = []
            
            for file in batch_files:
                emb = np.load(file)
                batch_embeddings.append(emb)
                batch_filenames.append(file.stem)
            
            batch_embeddings = np.vstack(batch_embeddings)
            batch_clusters = self.process_batch(batch_embeddings, batch_filenames)
            all_clusters.extend(batch_clusters)
        
        # 결과 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            "metadata": {
                "threshold": self.threshold,
                "total_images": total_images,
                "total_clusters": len(all_clusters),
                "timestamp": timestamp
            },
            "clusters": all_clusters
        }
        
        output_file = output_dir / f"clustering_result_threshold_{self.threshold}_{timestamp}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n=== 클러스터링 결과 ===")
        print(f"임계값: {self.threshold}")
        print(f"전체 이미지 수: {total_images}개")
        print(f"발견된 클러스터 수: {len(all_clusters)}개")
        print(f"\n결과가 저장되었습니다: {output_file}")
        
        return result 