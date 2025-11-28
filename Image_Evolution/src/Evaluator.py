import numpy as np
from scipy.ndimage import gaussian_filter


def mse_fitness(state, target):
    # 轉成 float
    diff = state.astype("float") - target.astype("float")
    
    # 將差值平方
    squared_diff = diff ** 2
    
    # 分別取出 R, G, B channel 
    r_diff = squared_diff[:, :, 0]
    g_diff = squared_diff[:, :, 1]
    b_diff = squared_diff[:, :, 2]
    
    # 加權總和 (權重可微調)
    # 讓演算法優先修正綠色通道 (通常包含大部分亮度細節)
    weighted_err = np.sum(0.11 * b_diff + 0.59 * g_diff + 0.30 * r_diff)
    
    mse = weighted_err / (state.shape[0] * state.shape[1])
    
    return 1.0 / (mse + 1e-10)  # 避免除以零

def mse(img1, img2):
    # 使用 MSE 計算差異
    mse = np.mean((img1.astype("float") - img2.astype("float")) ** 2)
    
    # 將 MSE 轉換為 "Fitness" (越大越好)，避免修改大量排序邏輯
    # 加上 1e-10 避免除以零
    return 1.0 / (mse + 1e-10)



# 比對圖片
def ssim(img1, img2):
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)

    # 計算均值和方差（通常用高斯濾波做局部平均）
    mu1 = gaussian_filter(img1, 1.5)
    mu2 = gaussian_filter(img2, 1.5)

    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = gaussian_filter(img1 * img1, 1.5) - mu1_sq
    sigma2_sq = gaussian_filter(img2 * img2, 1.5) - mu2_sq
    sigma12 = gaussian_filter(img1 * img2, 1.5) - mu1_mu2

    C1 = (0.01 * 255) ** 2
    C2 = (0.03 * 255) ** 2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))

    return ssim_map.mean()