# 🚀 CLIP-based Image Clustering and Remove Similar Images

<img src="assets/figure_0.png" width="800" alt="Overall Workflow">

A tool for finding and managing similar images using CLIP (Contrastive Language-Image Pre-Training) vision encoder. This tool helps you identify and organize similar images, and can be used to remove similar images based on a configurable similarity threshold.

## Key Features

- Generate image embeddings using CLIP vision encoder
- Cluster similar images based on cosine similarity
- Visualize image clusters for easy analysis
- Remove similar images based on configurable threshold
- Configurable similarity threshold

## Example Results
Here are some example clusters from the visualization step.

<img src="results/visualization/cluster_002.jpg" width="600" alt="Cluster Example 1">

<img src="results/visualization/cluster_004.jpg" width="600" alt="Cluster Example 2">

<img src="results/visualization/cluster_006.jpg" width="600" alt="Cluster Example 3">

## Installation

```bash
git clone https://github.com/ldj7672/Similar-Image-Finder.git
cd Similar-Image-Finder
pip install -r requirements.txt
```

### CLIP Model Setup

The tool uses the CLIP model from Hugging Face. There are two ways to set up the model.

1. **Automatic Download (Default)**
   - The model will be automatically downloaded from Hugging Face on first run
   - Default model: `openai/clip-vit-base-patch32`
   - The model will be cached in your local Hugging Face cache directory

2. **Using Local Model**
   - If you already have the CLIP model downloaded, you can specify its path in the config file:
   ```yaml
   model:
     name: "path/to/your/local/clip/model"
   ```

## Quick Start

**1. Generate image embeddings**
```bash
python src/generate_embeddings.py --image_dir path/to/images --output_dir path/to/embeddings
```

**2. Cluster similar images**
```bash
python src/cluster_images.py --embedding_dir path/to/embeddings --threshold 0.95
```

The clustering results are saved in the following JSON format.
```json
{
  "metadata": {
    "threshold": 0.94,
    "total_images": 22,
    "total_clusters": 7,
    "timestamp": "20250515_151708"
  },
  "clusters": [
    ["0", "1"],
    ["10", "9"],
    ["11", "12"],
    ["15", "16", "17"],
    ["18", "19"],
    ["20", "21"],
    ["4", "5"]
  ]
}
```

**3. Visualize results**
```bash
python src/visualize_clusters.py --result_file path/to/clustering_result.json --image_dir path/to/images
```

**4. Remove similar images**
```bash
python src/remove_similar_images.py \
    --result_file path/to/clustering_result.json \
    --image_dir path/to/images \
    --keep_first
```

This will:
- Keep one representative image from each cluster (first image by default)
- Delete other similar images based on the threshold
- Log the number of deleted images

## Configuration Options

- `--threshold`: Similarity threshold (default: 0.95)
  - For removing very similar images: 0.94-0.96 recommended
  - For finding related images: 0.85-0.93 recommended
- `--batch_size`: Batch processing size (default: 1000)
- `--device`: Device to use (cuda/cpu/mps)

## Project Structure

```
similar-image-finder/
├── src/
│   ├── __init__.py
│   ├── clip_encoder.py      # CLIP model for image encoding
│   ├── image_clusterer.py   # Image clustering logic
│   ├── visualizer.py        # Result visualization
│   ├── remove_duplicates.py # Remove similar images
│   └── utils.py
├── config/
│   └── default_config.yaml  # Configuration settings
├── requirements.txt
└── README.md
```

---

## 한글 가이드

### 간단 소개
이 레포는 CLIP Vision Encoder를 활용하여 유사한 이미지를 찾고 관리하는 솔루션을 제공합니다. 주로 다음과 같은 용도로 사용할 수 있습니다.
- 유사한 이미지들을 그룹화하여 분석
- 임계값 기반으로 유사한 이미지 제거
- 대규모 이미지 데이터셋 정리

### Quick Start

**1. 이미지 임베딩 생성하기**
```bash
python src/generate_embeddings.py --image_dir path/to/images --output_dir path/to/embeddings
```

**2. 유사한 이미지 클러스터링**
```bash
python src/cluster_images.py --embedding_dir path/to/embeddings --threshold 0.95
```

클러스터링 결과는 아래와 같은 JSON 포맷으로 출력됩니다.
```json
{
  "metadata": {
    "threshold": 0.94,
    "total_images": 22,
    "total_clusters": 7,
    "timestamp": "20250515_151708"
  },
  "clusters": [
    ["0", "1"],
    ["10", "9"],
    ["11", "12"],
    ["15", "16", "17"],
    ["18", "19"],
    ["20", "21"],
    ["4", "5"]
  ]
}
```

**3. 결과 시각화**
```bash
python src/visualize_clusters.py --result_file path/to/clustering_result.json --image_dir path/to/images
```

**4. 유사 이미지 제거**
```bash
python src/remove_similar_images.py \
    --result_file path/to/clustering_result.json \
    --image_dir path/to/images \
    --keep_first
```

이 명령어는 각 클러스터에서 대표 이미지 하나만 남기고 나머지 유사한 이미지들을 삭제합니다. `--keep_first` 옵션을 사용하면 클러스터의 첫 번째 이미지를 유지하고, 이 옵션을 제거하면 마지막 이미지를 유지합니다.

### Threshold 설정 가이드
이미지 유사도 임계값은 용도에 따라 다르게 설정할 수 있습니다.

1. 유사 이미지 제거용 (0.94 ~ 0.96)
   - 매우 유사한 이미지만 제거하고 싶을 때 사용
   - 0.94: 약간 더 관대한 기준
   - 0.96: 매우 엄격한 기준

2. 관련 이미지 그룹화용 (0.85 ~ 0.93)
   - 비슷한 주제나 스타일의 이미지를 찾을 때 사용
   - 0.85: 넓은 범위의 관련 이미지 포함
   - 0.93: 더 좁은 범위의 유사 이미지 포함
