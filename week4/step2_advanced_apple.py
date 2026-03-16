# -*- coding: utf-8 -*-
"""
생물자원가공공학 및 실습 - 4주차 실습 (Advanced)
주제: 대상 품목 변경 (사과)에 따른 밀도 및 공극률 변화 분석
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import product, combinations

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# =====================================================================
# [실습 과제] 아래의 변수값을 매뉴얼의 사과(Apple) 데이터로 수정하세요.
# =====================================================================
# 단일 사과 체적 (cm^3)
volume_single_cm3 = ???  # (예: 315.0)

# 단일 사과 질량 (g)
mass_single_g = ???      # (예: 280.0)

# 플라스틱 상자 규격 (18,000 cm^3)
box_volume_cm3 = 40.0 * 30.0 * 15.0  

# 박스 적재 개수
apple_count = ???        # (예: 24)

# =====================================================================
# 밀도 및 공극률 계산식 (수정 불필요)
# =====================================================================
# 1. 파티클 밀도
density_particle = mass_single_g / volume_single_cm3

# 2. 벌크 밀도
mass_total_g = mass_single_g * apple_count
density_bulk = mass_total_g / box_volume_cm3

# 3. 공극률
porosity_density_based = (1 - (density_bulk / density_particle)) * 100

print(f"[Advanced: 사과]")
print(f" - 파티클 밀도: {density_particle:.3f} g/cm^3")
print(f" - 벌크 밀도  : {density_bulk:.3f} g/cm^3")
print(f" - 공극률     : {porosity_density_based:.2f} %")

# =====================================================================
# 시각화 (수정 불필요 - 24개 격자에 맞춰 자동 생성)
# =====================================================================
fig = plt.figure(figsize=(18, 6))

# ---- (A) 좌측: 3D 가상 패킹 (4x3x2 배열 = 24개) ----
ax1 = fig.add_subplot(131, projection='3d')
r = [0, 40]
for s, e in combinations(np.array(list(product(r, [0, 30], [0, 15]))), 2):
    if np.sum(np.abs(s-e)) in [40, 30, 15]:
        ax1.plot3D(*zip(s, e), color="black", linestyle='--', alpha=0.3)

x_centers = np.linspace(5, 35, 4)
y_centers = np.linspace(5, 25, 3)
z_centers = np.linspace(3.75, 11.25, 2)
X, Y, Z = np.meshgrid(x_centers, y_centers, z_centers)

# --- 공극(Void) 영역 시각화 추가 ---
from scipy.spatial.distance import cdist
vx, vy, vz = np.meshgrid(np.linspace(1, 39, 20), 
                         np.linspace(1, 29, 15), 
                         np.linspace(1, 14, 8))
void_pts = np.vstack((vx.flatten(), vy.flatten(), vz.flatten())).T
center_pts = np.vstack((X.flatten(), Y.flatten(), Z.flatten())).T

# 사과 체적이 더 크므로(약 315) 구 환산 시 반경 약 4.22cm로 설정
R_apple = np.cbrt(315.0 * (3/(4*np.pi))) if 'volume_single_cm3' not in locals() or volume_single_cm3 is None else np.cbrt(315.0 * (3/(4*np.pi)))
distances = cdist(void_pts, center_pts)
is_void = np.min(distances, axis=1) > 4.2 # 하드코딩된 대략적 사과 반경

# 빈 공간(공극)을 시안색(Cyan) 반투명 점으로 시각화하여 사과(Red)와 시각적 대비
ax1.scatter(void_pts[is_void, 0], void_pts[is_void, 1], void_pts[is_void, 2], 
            s=15, c='cyan', alpha=0.3, label='Void (공극)')

# 사과는 붉은색 톤으로 시각화
ax1.scatter(X, Y, Z, s=800, c='#FF5252', alpha=1.0, edgecolors='#B71C1C', label='Apple')
ax1.set_title('Advanced: 사과 3D 가상 패킹 (24개)', fontsize=14, pad=15)
ax1.set_box_aspect((40, 30, 15))
ax1.legend(loc='upper right', fontsize=10)

# ---- (B) 중앙: 밀도 갭 차트 ----
ax2 = fig.add_subplot(132)
bars = ax2.bar(['파티클 밀도\n(사과)', '벌크 밀도\n(사과산물)'], 
               [density_particle, density_bulk], color=['#FFCDD2', '#EF9A9A'], edgecolor='black', width=0.5)
ax2.set_title('밀도 갭 분석 (Apple)', fontsize=14, pad=15)
ax2.set_ylim(0, max([density_particle, density_bulk]) * 1.3)
for bar in bars:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
             f'{bar.get_height():.3f}', ha='center', va='bottom', fontweight='bold', fontsize=11)

# ---- (C) 우측: 파이 차트 ----
ax3 = fig.add_subplot(133)
ax3.pie([100 - porosity_density_based, porosity_density_based], explode=(0.05, 0),
        labels=['사과 체적\n(점유)', '빈 공기층\n(공극)'], colors=['#FFCDD2', '#e6f0ff'],
        autopct='%1.1f%%', startangle=140, textprops={'fontsize': 13, 'fontweight': 'bold'},
        wedgeprops={'edgecolor': 'black', 'linewidth': 1})
ax3.set_title(f'사과 점유율 및 공극률 ({apple_count}개)', fontsize=14, pad=15)

plt.tight_layout()
plt.show()
