# Scanpy QC 분석 도구

이 프로젝트는 Scanpy를 사용한 단일 세포 RNA-seq 데이터의 품질 관리(QC) 분석을 위한 도구를 제공합니다.

## 기능

- 단일 세포 데이터 로드 (H5AD 또는 10X 형식)
- 기본 QC 메트릭 계산 (유전자 수, UMI 수, 미토콘드리아/리보솜 비율 등)
- QC 메트릭의 시각화
- 사용자 정의 임계값에 따른 저품질 세포 및 유전자 필터링
- 데이터 정규화 및 로그 변환
- 고변동 유전자 식별
- PCA, UMAP 및 클러스터링을 통한 기본 분석

## 요구 사항

```
scanpy==1.10.3
anndata==0.10.9
numpy==2.0.2
scipy==1.14.1
pandas==2.2.3
scikit-learn==1.5.2
matplotlib
```

## 사용법

### 1. 기본 QC 분석 실행

예제 데이터(PBMC3K)를 사용하여 QC 분석을 실행하려면:

```bash
python run_qc_example.py
```

이 스크립트는 자동으로 예제 데이터를 다운로드하고 QC 분석을 수행한 후 결과를 `figures/qc_results` 디렉토리에 저장합니다.

### 2. 사용자 데이터로 QC 분석 실행

자신의 데이터를 분석하려면 `qc_analysis.py` 파일의 `run_qc_analysis` 함수를 사용합니다:

```python
import scanpy as sc
from qc_analysis import run_qc_analysis

# 데이터 경로 (H5AD 또는 10X 포맷)
data_path = 'path/to/your/data'

# QC 분석 실행
adata = run_qc_analysis(
    data_path,
    min_genes=200,     # 세포당 최소 유전자 수
    min_cells=3,       # 유전자당 최소 세포 수
    max_genes=5000,    # 세포당 최대 유전자 수
    max_pct_mito=20,   # 미토콘드리아 유전자 최대 비율(%)
    max_pct_ribo=50,   # 리보솜 유전자 최대 비율(%)
    n_hvgs=2000        # 고변동 유전자 수
)

# 추가 분석 (선택사항)
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color='leiden')
```

## 매개변수 조정

데이터 유형에 따라 QC 매개변수를 조정해야 할 수 있습니다:

- 면역 세포(PBMC): `max_genes=3000, max_pct_mito=5`
- 뇌 세포: `max_genes=5000, max_pct_mito=15`
- 발생 세포: `max_genes=7000, max_pct_mito=10`

항상 데이터의 QC 분포를 시각화하고 그에 따라 매개변수를 조정하는 것이 좋습니다.

## 결과 해석

QC 분석 결과는 다음 파일로 저장됩니다:

- `adata_qc_filtered.h5ad`: 필터링된 AnnData 객체
- `qc_metrics_before_filtering.png`: 필터링 전 QC 메트릭 시각화
- `qc_metrics_after_filtering.png`: 필터링 후 QC 메트릭 시각화
- `highly_variable_genes.png`: 고변동 유전자 시각화
- `umap_qc_metrics.png`: QC 메트릭으로 컬러링된 UMAP
- `umap_clusters.png`: 클러스터링 결과 UMAP

## 참고 자료

- [Scanpy 튜토리얼](https://scanpy-tutorials.readthedocs.io/en/latest/pbmc3k.html)
- [Scanpy 문서](https://scanpy.readthedocs.io/)
- [AnnData 문서](https://anndata.readthedocs.io/) 