import os

import scanpy as sc
import anndata as ad

filename='/Users/jungj2/Dropbox/Metadata/mcp/scanpy_mcp/data/filtered_gene_bc_matrices/hg19'
# var_names_make_unique: True

def read_10x_mtx(filename: str) -> ad.AnnData:

  adata = sc.read_10x_mtx(
      filename,  # the directory with the `.mtx` file
      var_names="gene_symbols",  # use gene symbols for the variable names (variables-axis index)
  )
  # 기본 정보 출력
  print("데이터 모양:", adata.shape)
  print(f"관측값 수: {adata.n_obs}, 변수 수: {adata.n_vars}")

  adata.var_names_make_unique()
  adata.var["mt"] = adata.var_names.str.startswith("MT-")
  sc.pp.calculate_qc_metrics(
      adata, qc_vars=["mt"], percent_top=None, log1p=False, inplace=True
  )
  
  return adata


def qc_violin(adata: ad.AnnData):

  print("plot vioin...")
  sc.pl.violin(
    adata,
    ["n_genes_by_counts", "total_counts", "pct_counts_mt"],
    jitter=0.4,
    multi_panel=True,
    save="_qc.png"
  )

  return None


def filtering(adata: ad.AnnData, n_genes_by_counts: int=2500, pct_counts_mt: int=5) -> ad.AnnData:

  adata = adata[adata.obs.n_genes_by_counts < n_genes_by_counts, :]
  adata = adata[adata.obs.pct_counts_mt < pct_counts_mt, :].copy()

  return adata


# def read_10x_mtx(adata) -> str:

#   filename = "/Users/jungj2/Dropbox/Metadata/mcp/scanpy_mcp/data/filtered_gene_bc_matrices/hg19"

#   if(save_fig):
#     dir_save = Path(filename).parent / "data"

#     print("데이터 모양:", ./results)

#     # 결과 디렉토리 설정
#     results_dir = "./results"
#     os.makedirs(results_dir, exist_ok=True)

#     # 플롯 설정
#     sc.settings.set_figure_params(dpi=80, facecolor='white')
#     sc.settings.verbosity = 3  # 자세한 로깅
#     sc.settings.figdir = results_dir  # 그림 저장 경로

#   # 데이터 로드
#   adata = sc.read_10x_mtx(
#       'data/filtered_gene_bc_matrices/hg19/',  # 데이터 디렉토리
#       var_names='gene_symbols',  # 유전자 심볼을 변수 이름으로 사용
#       cache=True
#   )


#   # 기본 필터링 및 정규화
#   sc.pp.filter_cells(adata, min_genes=200)
#   sc.pp.filter_genes(adata, min_cells=3)

#   # 미토콘드리아 유전자 비율 계산
#   adata.var['mt'] = adata.var_names.str.startswith('MT-')
#   sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)

#   # QC 시각화
#   sc.pl.violin(adata, ['n_genes_by_counts', 'total_counts', 'pct_counts_mt'], 
#               jitter=0.4, multi_panel=True, save='.png')

#   # 고품질 세포 필터링
#   adata = adata[adata.obs.n_genes_by_counts < 2500, :]
#   adata = adata[adata.obs.pct_counts_mt < 5, :]

#   # 정규화 및 로그 변환
#   sc.pp.normalize_total(adata, target_sum=1e4)
#   sc.pp.log1p(adata)

#   # 고변이 유전자 선택
#   sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
#   sc.pl.highly_variable_genes(adata, save='.png')

#   # 차원 축소를 위해 고변이 유전자만 사용
#   adata = adata[:, adata.var.highly_variable]

#   # 데이터 스케일링
#   sc.pp.scale(adata, max_value=10)

#   # PCA
#   sc.tl.pca(adata, svd_solver='arpack')
#   sc.pl.pca(adata, color='CST3', save='.png')
#   sc.pl.pca_variance_ratio(adata, log=True, save='.png')

#   # 이웃 그래프 구축
#   sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40)

#   # UMAP
#   sc.tl.umap(adata)
#   sc.pl.umap(adata, color=['CST3', 'NKG7', 'PPBP'], save='.png')

#   # 클러스터링
#   sc.tl.leiden(adata)
#   sc.pl.umap(adata, color='leiden', legend_loc='on data', title='Leiden clusters', save='.png')

#   # 마커 유전자
#   sc.tl.rank_genes_groups(adata, 'leiden', method='wilcoxon')
#   sc.pl.rank_genes_groups(adata, n_genes=25, sharey=False, save='.png')

#   # 클러스터별 마커 유전자 히트맵
#   sc.pl.rank_genes_groups_heatmap(adata, n_genes=10, save='.png')

#   # 결과 저장
#   adata.write(os.path.join(results_dir, 'pbmc3k_analysis.h5ad'))

#   print("분석 완료! 결과는 results 디렉토리에 저장되었습니다.")
