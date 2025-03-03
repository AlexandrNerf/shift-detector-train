# Тренировочный скрипт для YOLO text detection

Скрипт для обучения YOLO на PyTorch. Взято из библиотеки `ultralytics`

## Структура репозитория

```
├───config
│   ├───augmentations
│   ├───functional
│   ├───hyperparams
│   └───logger
├───dataset
│   ├───images
│   │   ├───train
│   │   └───val
│   └───labels
│       ├───train
│       └───val
├───outputs
├───runs
├───utils
├───dataset_preparing.py
├───download_file.py
└───train.py
```

Настройки обучения хранятся в папке `config` (`config.yaml` и прилегающие папки со своими отдельными файлами). В `utils` располагаются дополнительные скрипты, а в `dataset` данные в классическом формате YOLO.


Папка с датасетом YOLO:

```shell
├───images
│   ├───train
│   └───val
└───labels
│   ├───train
│   └───val
└── data.yaml
```

Где `data.json` содержит пути до `train` и `val`, а также обозначения классов


## Установка + настройка среды

Склонировать репозиторий и войти в папку.

```shell
git clone -b yolo-train --single-branch https://github.com/AlexandrNerf/shift-detector-train.git
cd shift-detector-train
```

Рекомендуется использовать `Anaconda` для работы.

Создание и подготовка среды:
```shell
conda create --name <ENV_NAME> python=3.12.8
conda activate <ENV_NAME>
pip install -r requirements.txt
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
rm -rf *.zip *.7z
cd ../
```

На Windows:

```shell
cd dataset
tar -xf DDI_new.zip
tar -xf PDFA_new.zip
tar -xf SROIE.7z
cd ../
```

Должны получиться две папки - `data` и `images`

Теперь запускаем процесс форматирования данных для `YOLO`

```shell
python dataset_preparing 0.2
```

Аргумент - это размер валидационной выборки

В результате работы скрипта - разбиение на трейн и валидацию и приведение к нужному виду (нулевые классы)

## Использование

Для запуска:

```shell
python set_settings.py
python train.py
```

`set_settings.py` можно пропускать следующие разы, если не меняются параметры логирования (это нужно для обновления настроек логеров YOLO)



Настройка параметров происходит в конфигах. В `config.yaml` собраны самые главные и часто изменяемые (такие как число эпох, базовая модель для обучения или запуск с уже обученных весов). В папках отдельно лежат конфиги для параметров модели, которые можно создавать и менять в главном конфиге.