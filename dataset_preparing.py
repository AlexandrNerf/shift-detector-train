import argparse
import hashlib
import json
import os
import shutil

import cv2
from sklearn.model_selection import train_test_split
from tqdm import tqdm


def split_data(dataset_path, split_coeff):
    """
    Разбивает данные на train и val
    """
    data_dir = os.path.join(dataset_path, "data")
    images_dir = os.path.join(dataset_path, "images")

    # Пути к папкам для train и val
    train_data_dir = os.path.join(dataset_path, "train_set/data")
    train_images_dir = os.path.join(dataset_path, "train_set/images")
    val_data_dir = os.path.join(dataset_path, "val_set/data")
    val_images_dir = os.path.join(dataset_path, "val_set/images")

    os.makedirs(train_data_dir, exist_ok=True)
    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(val_data_dir, exist_ok=True)
    os.makedirs(val_images_dir, exist_ok=True)

    txt_files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]

    train_files, val_files = train_test_split(
        txt_files, test_size=split_coeff, random_state=42
    )

    # Функция для копирования пар файлов
    def copy_files(
        file_list, src_data_dir, src_images_dir, dst_data_dir, dst_images_dir
    ):
        for txt_file in file_list:
            image_file = txt_file.replace(
                ".txt", ".png"
            )  # Замените на нужное расширение, если не png

            shutil.copy(
                os.path.join(src_data_dir, txt_file),
                os.path.join(dst_data_dir, txt_file),
            )

            if os.path.exists(os.path.join(src_images_dir, image_file)):
                shutil.copy(
                    os.path.join(src_images_dir, image_file),
                    os.path.join(dst_images_dir, image_file),
                )

    # Копируем train
    copy_files(train_files, data_dir, images_dir, train_data_dir, train_images_dir)

    # Копируем val
    copy_files(val_files, data_dir, images_dir, val_data_dir, val_images_dir)


def compute_sha256(image_path):
    """Вычисляет SHA-256 хеш файла."""
    with open(image_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def yolo_to_polygon(yolo_data, img_w, img_h):
    """Конвертирует YOLO аннотации в список полигонов."""
    polygons = []
    for line in yolo_data:
        parts = line.strip().split()
        if len(parts) < 5:
            continue
        try:
            x, y, w, h = map(float, parts[1:])
        except:
            continue
        if (
            x > 1.0
            or x < 0.0
            or y > 1.0
            or y < 0.0
            or w > 1.0
            or w < 0.0
            or h > 1.0
            or h < 0.0
        ):
            continue
        x, w = x * img_w, w * img_w
        y, h = y * img_h, h * img_h

        # Восстанавливаем координаты углов прямоугольника
        x1, y1 = x - w / 2, y - h / 2
        x2, y2 = x + w / 2, y - h / 2
        x3, y3 = x + w / 2, y + h / 2
        x4, y4 = x - w / 2, y + h / 2
        polygons.append([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

    return polygons


def find_files(root_dir, extensions):
    """Рекурсивно находит файлы с заданными расширениями."""
    files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(extensions):
                files.append(os.path.join(dirpath, filename))
    return files


def convert_dataset(dataset_path, desc="TRAIN"):
    """Обрабатывает датасет и сохраняет JSON."""
    images_dir = os.path.join(dataset_path, "images")
    annotations_dir = os.path.join(dataset_path, "data")

    if not os.path.exists(images_dir) or not os.path.exists(annotations_dir):
        print("Ошибка: Ожидается структура с папками 'images/' и 'data/'")
        return

    images = find_files(images_dir, (".png", ".jpg", ".jpeg"))
    annotations = find_files(annotations_dir, (".txt",))

    annotation_map = {os.path.splitext(os.path.basename(f))[0]: f for f in annotations}
    dataset = {}

    for image_path in tqdm(images, desc=f"Creating labels for {desc} dataset:"):
        image_name = os.path.basename(image_path)
        image_id = os.path.splitext(image_name)[0]

        img = cv2.imread(image_path)
        if img is None:
            continue
        img_h, img_w = img.shape[:2]

        img_hash = compute_sha256(image_path)
        annotation_path = annotation_map.get(image_id, None)

        polygons = []
        if annotation_path:
            with open(annotation_path, "r", encoding="utf-8") as f:
                polygons = yolo_to_polygon(f.readlines(), img_w, img_h)
        if len(polygons) > 0:
            dataset[image_name] = {
                "img_dimensions": (img_h, img_w),
                "img_hash": img_hash,
                "polygons": polygons,
            }

    with open(os.path.join(dataset_path, "labels.json"), "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    print(f"JSON сохранен в {os.path.join(dataset_path, 'labels.json')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Конвертация YOLO аннотаций в JSON")

    parser.add_argument(
        "train_val_split", type=float, default=0.2, help="Размер валидационной выборки"
    )
    parser.add_argument(
        "--dataset_path",
        type=str,
        default="dataset",
        help="Путь к директории с датасетом",
    )

    args = parser.parse_args()
    if args.train_val_split > 1.0 or args.train_val_split < 0:
        raise Exception("Coeff of splitting should be > 0.0 and < 1.0")
    split_data(args.dataset_path, args.train_val_split)

    convert_dataset(os.path.join(args.dataset_path, "train_set"))
    convert_dataset(os.path.join(args.dataset_path, "val_set"), desc="VAL")
