"""
Step 1: Power Law Model Curve Fitting
이 스크립트는 가상의 전단 속도(Shear Rate)와 전단 응력(Shear Stress) 데이터를 통해
비뉴턴 유체의 Power Law 모델 (Tau = K * Gamma^n) 계수인
농도 계수(Consistency Index, K)와 유동 지수(Flow Behavior Index, n)를
scipy.optimize.curve_fit을 이용해 산출하는 기본 알고리즘입니다.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import linregress

# 1. 가상의 실험 데이터 보간 (전분 풀 - Pseudoplastic 유체 가정)
# 전단 속도 (Shear Rate, 1/s): 10 ~ 100
shear_rate_data = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
# 전단 응력 (Shear Stress, Pa) (측정 결과 가정)
shear_stress_data = np.array([18.5, 29.3, 38.5, 46.8, 54.3, 61.2, 67.8, 74.0, 80.0, 85.8])

# 2. 파워 로우(Power Law) 모델 함수 정의
# 식: \tau = K * \dot{\gamma}^n
def power_law(gamma, K, n):
    return K * (gamma ** n)

# 3. 최적 계수 찾기 (log Fitting)
log_shear_rate = np.log(shear_rate_data)
log_shear_stress = np.log(shear_stress_data)

slope, intercept, r_value, p_value, std_err = linregress(log_shear_rate, log_shear_stress)

n_est_log = slope
K_est = np.exp(intercept)

print(f"--- Power Law 피팅 결과 ---")
print(f"농도 계수 (K): {K_est:.4f} Pa·s^n")
print(f"유동 지수 (n): {n_est_log:.4f}")

plt.figure(figsize=(8, 6))

plt.scatter(log_shear_rate, log_shear_stress, color='blue', label='Log Data')

# 직선
log_fit = intercept + slope * log_shear_rate
plt.plot(log_shear_rate, log_fit, color='red',
         label=f'Linear Fit (n={n_est_log:.2f})')

plt.title('Log-Log Linearization of Power Law')
plt.xlabel('log(Shear Rate)')
plt.ylabel('log(Shear Stress)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.show()