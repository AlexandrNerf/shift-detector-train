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

Для скачивания датасетов потребуется доступ к хранилищу `minIo`. Закинуть в папку репозитория файл `credentials.json`

### 1. Cкачать уже готовый датасет с minIo

Необходимые данные уже разбиты на трейн и валидацию под каждый конкретный датасет (Соотношение 8:2)

Запускаем:

```shell
python download_prepared_dataset.py yolo_dataset.zip
```

Если вы уже сохраняли свой датасет с другим разбиением, указывайте своё название для него, например `yolo_dataset_0_3.zip`

После распаковываем:

```shell
unzip *.zip
rm -rf *.zip
```

### 2. Собственное разделение данных (если нужен кастомный размер валидации или нужно заново создать датасет) 


Запускаем:

```shell
python download_file.py
```

В папке dataset появятся 3 архива. Распаковываем их туда же

Выполняем:

```shell
cd dataset
unzip *.zip
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

### Опционально после скачивания

Если хочется сохранить текущий датасет в minIo, запускаем:

```shell
rm -rf dataset/data
rm -rf dataset/images/*.png
python save_dataset.py yolo_dataset_YOUR_SPLIT.zip
```

Здесь указывать необходимое разделение, чтобы обозначить датасет. Рекомендуется формат `*_0_2.zip`, указывая размер валидационной выборки.

## Использование

Для запуска:

```shell
python set_settings.py
python train.py
```

`set_settings.py` можно пропускать следующие разы, если не меняются параметры логирования (это нужно для обновления настроек логеров YOLO)



Настройка параметров происходит в конфигах. В `config.yaml` собраны самые главные и часто изменяемые (такие как число эпох, базовая модель для обучения или запуск с уже обученных весов). В папках отдельно лежат конфиги для параметров модели, которые можно создавать и менять в главном конфиге.