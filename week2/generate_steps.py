import cv2
import numpy as np
import os

def process_image(img_path, prefix, output_dir=""):
    # 저장 경로 설정
    if output_dir:
        output_prefix = os.path.join(output_dir, prefix)
    else:
        output_prefix = prefix

    # 1. 원본 로드
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error loading {img_path}")
        return

    # 2. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f"{output_prefix}_step1_gray.png", gray)

    # 3. Blur & Threshold (오츠 이진화)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imwrite(f"{output_prefix}_step2_thresh.png", thresh)

    # 4. 윤곽선 검출
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    main_contour = max(contours, key=cv2.contourArea)

    # 두꺼운 선으로 윤곽선 그리기 (원본 복사본에)
    img_contours = img.copy()
    cv2.drawContours(img_contours, [main_contour], -1, (0, 255, 0), 3)
    cv2.imwrite(f"{output_prefix}_step3_contour.png", img_contours)

    # 5. 회전된 바운딩 박스
    rect = cv2.minAreaRect(main_contour)
    box = cv2.boxPoints(rect)
    box = np.int32(box)  # 정수형 변환

    img_box = img.copy()
    cv2.drawContours(img_box, [box], 0, (255, 0, 0), 3)

    # 텍스트로 치수 표시 추가
    dim1, dim2 = rect[1]
    L = max(dim1, dim2)
    W = min(dim1, dim2)
    cv2.putText(img_box, f"L:{L:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(img_box, f"W/T:{W:.1f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imwrite(f"{output_prefix}_step4_boundingbox.png", img_box)
    print(f"[{prefix}] L:{L:.1f}, W:{W:.1f}")



if __name__ == "__main__":
    # 현재 스크립트 위치를 기준으로 데이터 폴더 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_images_dir = os.path.join(base_dir, "Raw images")
    processed_images_dir = os.path.join(base_dir, "Processed images")

    # Processed images 폴더가 없으면 생성
    if not os.path.exists(processed_images_dir):
        os.makedirs(processed_images_dir)

    print("정상 사과 측면 처리중 (A군)...")
    process_image(os.path.join(raw_images_dir, "apple_side_A.png"), "apple_side_A", output_dir=processed_images_dir)

    print("정상 사과 상면 처리중 (A군)...")
    process_image(os.path.join(raw_images_dir, "apple_top_A.png"), "apple_top_A", output_dir=processed_images_dir)

    print("10% 대조군 사과 측면 처리중 (B군)...")
    process_image(os.path.join(raw_images_dir, "apple_side_B.png"), "apple_side_B", output_dir=processed_images_dir)
