import numpy as np
import cv2

def sort_points(points):
    """
    對點的座標進行排序，使其成為一個連續的逆時針或順時針多邊形。
    :param points
    :return: 排序後的點陣列 (逆時針順序)。
    """
    # 1. 計算幾何中心 (Centroid)
    # np.mean(axis=0) 計算每一欄 (x 和 y) 的平均值
    center = points.mean(axis=0)
    
    # 2. 計算相對於中心的角度
    # x 座標在 points[:, 0]，y 座標在 points[:, 1]
    # 角度計算公式: atan2(y 差值, x 差值)

    # 差值 (points - center)
    x_diff = points[:, 0] - center[0]
    y_diff = points[:, 1] - center[1]
    
    # 計算角度 (弧度)
    angles = np.arctan2(y_diff, x_diff)
    
    # 3. 根據角度進行排序
    # argsort() 返回排序後的索引
    sorted_indices = np.argsort(angles)
    
    # 應用排序後的索引
    sorted_points = points[sorted_indices]
    
    # 返回逆時針排序的點 (通常是從最小角度到最大角度)
    return sorted_points


# Alpha blending： img[y, x] ← α*color + (1-α)*old
def blend_pixel(img, x, y, color, alpha):
    # Keep per-pixel fallback (used by draw_line) — cast to float, blend and store.
    if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
        dst = img[y, x].astype(np.float32)
        src = np.array(color, dtype=np.float32)
        out = alpha * src + (1 - alpha) * dst
        img[y, x] = np.clip(out, 0, 255).astype(np.uint8)

# 用掃描線填滿多邊形
def fill_poly(img, points, color, alpha=1.0):
    """Efficient triangle fill and alpha blend using OpenCV.

    This replaces the old per-pixel scanline approach with a vectorized
    mask + blend. The function supports float coordinates and clamps values.
    """
    h, w = img.shape[:2]

    pos = sort_points(np.array(points))

    # Ensure coordinates are integer pixel indices
    pts = np.array([pos], dtype=np.int32)

    # clamp pts into image bounds
    pts[:, :, 0] = np.clip(pts[:, :, 0], 0, w - 1)
    pts[:, :, 1] = np.clip(pts[:, :, 1], 0, h - 1)

    # single-channel mask for coverage (0 or 255)
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask, pts, 255)

    if alpha >= 0.999:
        # solid overwrite inside the triangle
        fill_color = tuple(int(c) for c in color)
        # Use a 3-channel copy of mask to index into color channels
        for c in range(3):
            img[..., c][mask == 255] = fill_color[c]
        return

    # vectorized blend: for pixels where mask==255, blend with given alpha
    alpha_layer = (mask.astype(np.float32) / 255.0) * float(alpha)  # shape (h,w)
    alpha_layer = alpha_layer[:, :, None]  # broadcast to (h,w,1)

    img_f = img.astype(np.float32)
    src_color = np.array(color, dtype=np.float32).reshape((1, 1, 3))

    # blended = alpha_layer * src_color + (1-alpha_layer) * img_f
    img_f = alpha_layer * src_color + (1.0 - alpha_layer) * img_f

    # write back only the affected pixels
    img[...] = np.clip(img_f, 0, 255).astype(np.uint8)
