"""Numpy-only replacements for the cv2 functions used in metadrive map rasterization."""

import numpy as np


def fill_poly(img, pts_list, color):
    """Fill polygon(s) in *img* (H x W x C or H x W) with *color*.

    Mimics ``cv2.fillPoly(img, pts_list, color=color)`` for integer-coordinate
    polygons using a scanline approach.  *pts_list* is an array of shape
    (1, N, 2) or (N, 2) — matching the cv2 calling convention.
    """
    pts = np.asarray(pts_list).reshape(-1, 2)
    if len(pts) < 3:
        return img

    h, w = img.shape[:2]
    y_min = max(int(pts[:, 1].min()), 0)
    y_max = min(int(pts[:, 1].max()), h - 1)

    n = len(pts)
    for y in range(y_min, y_max + 1):
        intersections = []
        for i in range(n):
            p1 = pts[i]
            p2 = pts[(i + 1) % n]
            y1, y2 = p1[1], p2[1]
            if y1 == y2:
                continue
            if y1 > y2:
                y1, y2 = y2, y1
                p1, p2 = p2, p1
            if y1 <= y < y2:
                x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                intersections.append(x)
        intersections.sort()
        for j in range(0, len(intersections) - 1, 2):
            x_start = max(int(np.ceil(intersections[j])), 0)
            x_end = min(int(np.floor(intersections[j + 1])), w - 1)
            if x_start <= x_end:
                img[y, x_start:x_end + 1] = color
    return img


def _draw_line(img, x0, y0, x1, y1, color, thickness):
    """Bresenham line with thickness via perpendicular expansion."""
    h, w = img.shape[:2]
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    half = thickness // 2

    while True:
        for tx in range(-half, half + 1):
            for ty in range(-half, half + 1):
                px, py = x0 + tx, y0 + ty
                if 0 <= px < w and 0 <= py < h:
                    img[py, px] = color
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def draw_polylines(img, pts_list, is_closed, color, thickness):
    """Draw polyline(s) on *img*.

    Mimics ``cv2.polylines(img, pts_list, is_closed, color, thickness)``.
    """
    pts = np.asarray(pts_list).reshape(-1, 2).astype(np.int32)
    if len(pts) < 2:
        return img
    for i in range(len(pts) - 1):
        _draw_line(img, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], color, thickness)
    if is_closed and len(pts) > 2:
        _draw_line(img, pts[-1][0], pts[-1][1], pts[0][0], pts[0][1], color, thickness)
    return img


def dilate(img, kernel, iterations=1):
    """Binary/grayscale dilation via sliding-window max.

    Mimics ``cv2.dilate(img, kernel, iterations=N)``.
    *kernel* shape determines the structuring element.
    cv2.dilate squeezes single-channel (H,W,1) to (H,W).
    """
    squeezed = False
    if img.ndim == 3 and img.shape[2] == 1:
        img = img[:, :, 0]
        squeezed = True
    for _ in range(iterations):
        kh, kw = kernel.shape[:2]
        ph, pw = kh // 2, kw // 2
        padded = np.pad(img, ((ph, ph), (pw, pw)), mode='constant', constant_values=0)
        out = np.zeros_like(img)
        for dy in range(kh):
            for dx in range(kw):
                if kernel[dy, dx]:
                    out = np.maximum(out, padded[dy:dy + img.shape[0], dx:dx + img.shape[1]])
        img = out
    return img
