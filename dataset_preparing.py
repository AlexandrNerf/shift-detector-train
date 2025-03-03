import argparse
import os
import shutil

from sklearn.model_selection import train_test_split
from tqdm import tqdm


def split_data(dataset_path, split_coeff):
    """
    Разбивает данные на train и val
    """
    data_dir = os.path.join(dataset_path, 'data')
    images_dir = os.path.join(dataset_path, 'images')

    # Пути к папкам для train и val
    train_data_dir = os.path.join(dataset_path, 'labels/train')
    train_images_dir = os.path.join(dataset_path, 'images/train')
    val_data_dir = os.path.join(dataset_path, 'labels/val')
    val_images_dir = os.path.join(dataset_path, 'images/val')

    os.makedirs(train_data_dir, exist_ok=True)
    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(val_data_dir, exist_ok=True)
    os.makedirs(val_images_dir, exist_ok=True)

    txt_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]

    train_files, val_files = train_test_split(
        txt_files, test_size=split_coeff, random_state=42
    )

    # Функция для копирования пар файлов
    def copy_files(
        file_list, src_data_dir, src_images_dir, dst_data_dir, dst_images_dir
    ):
        for txt_file in tqdm(file_list, desc='Copying files:'):
            image_file = txt_file.replace(
                '.txt', '.png'
            )  # Замените на нужное расширение, если не png
            with open(os.path.join(src_data_dir, txt_file), 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Переписываем строки, меняя формат
            updated_lines = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 5:
                    parts[0] = '0'
                    updated_lines.append(' '.join(parts) + '\n')

            # Перезаписываем файл
            with open(os.path.join(dst_data_dir, txt_file), 'w') as f:
                f.writelines(updated_lines)
            # shutil.copy(os.path.join(src_data_dir, txt_file), os.path.join(dst_data_dir, txt_file))

            if os.path.exists(os.path.join(src_images_dir, image_file)):
                shutil.copy(
                    os.path.join(src_images_dir, image_file),
                    os.path.join(dst_images_dir, image_file),
                )

    # Копируем train
    copy_files(train_files, data_dir, images_dir, train_data_dir, train_images_dir)

    # Копируем val
    copy_files(val_files, data_dir, images_dir, val_data_dir, val_images_dir)


def find_files(root_dir, extensions):
    """Рекурсивно находит файлы с заданными расширениями."""
    files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(extensions):
                files.append(os.path.join(dirpath, filename))
    return files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Конвертация YOLO аннотаций в JSON")

    parser.add_argument(
        'train_val_split', type=float, default=0.2, help='Размер валидационной выборки'
    )
    parser.add_argument(
        '--dataset_path',
        type=str,
        default='dataset',
        help='Путь к директории с датасетом',
    )

    args = parser.parse_args()
    if args.train_val_split > 1.0 or args.train_val_split < 0:
        raise Exception("Coeff of splitting should be > 0.0 and < 1.0")
    split_data(args.dataset_path, args.train_val_split)
