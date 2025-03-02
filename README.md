# Тренировочный скрипт для FAST text detection

Скрипт для обучения FAST на PyTorch. Взято из библиотеки `doctr`

## Структура репозитория

```
├───dataset
│   ├───train_set
│   └───val_set
├───config
│   ├───hyperparams
│   └───logging
├───util
├───dataset_preparing.py
├───download_file.py
└───train.py
```

Настройки обучения хранятся в папке `config` (`config.yaml` и прилегающие папки `hyperparams` и `logging` со своими отдельными файлами). В `utils` располагаются дополнительные скрипты, а в `dataset` данные.


Папка с датасетом после преобразований будет иметь следующий вид:

```shell
├── images
│   ├── sample_img_01.png
│   ├── sample_img_02.png
│   ├── sample_img_03.png
│   └── ...
└── labels.json
```

Где `labels.json` содержит:

```shell
{
    "sample_img_01.png" = {
        'img_dimensions': (900, 600),
        'img_hash': "theimagedumpmyhash",
        'polygons': [[[x1, y1], [x2, y2], [x3, y3], [x4, y4]], ...]
     },
     "sample_img_02.png" = {
        'img_dimensions': (900, 600),
        'img_hash': "thisisahash",
        'polygons': [[[x1, y1], [x2, y2], [x3, y3], [x4, y4]], ...]
     }
     ...
}
```

Словарь, на каждое изображение (название png файла) - `img_dimensions` (Ширина и высота файла), `img_hash` (SHA256 изображения), `polygons` (Набор абсолютных координат бокса или полигона). 

Для преобразования датасета из формата YOLO (`data/img.txt` и `images/img.png`)


## Установка + настройка среды

Склонировать репозиторий и войти в папку.

```shell
git clone -b fast-train --single-branch https://github.com/AlexandrNerf/shift-detector-train.git
cd shift-detector-train
```

Рекомендуется использовать `Anaconda` для работы.

Создание и подготовка среды:
```shell
conda create --name <ENV_NAME> python=3.12.8
conda activate <ENV_NAME>
pip install -f requirements.txt
```

## Скачивание и подготовка данных

Для скачивания датасетов потребуется доступ к хранилищу `minIo` закинуть в папку репозитория файл `credentials.json`

Теперь запускаем:

```shell
python download_file.py
```

В папке dataset появятся 3 архива. Распаковываем их туда же

Выполняем:

```shell
cd dataset
unzip DDI_new.zip
unzip PDFA_new.zip
7z x SROIE.7z
cd ../
```

Для Windows:

```shell
cd dataset
tar -xf DDI_new.zip
tar -xf PDFA_new.zip
tar -xf SROIE.7z
cd ../
```

Должны получиться две папки - `data` и `images`

Теперь запускаем процесс форматирования данных для `FAST`

```shell
python dataset_preparing 0.2
```

Аргумент - это размер валидационной выборки

В результате работы скрипта - разбиение на трейн и валидацию + создание файлов labels.json

## Использование

Для запуска:

```shell
python train.py
```

Настройка параметров происходит в конфигах. В `config.yaml` собраны самые главные и часто изменяемые (такие как число эпох, базовая модель для обучения или запуск с уже обученных весов). В папках (hyperparams и logging) отдельно лежат конфиги для параметров модели, которые можно создавать и менять в главном конфиге.