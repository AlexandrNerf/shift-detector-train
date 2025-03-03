import argparse
import json
import os

import minio

from util.downloader_utils import Progress


def main(files, destination):
    """
    Запуск клиента minIO и скачивание датасетов
    """
    client = minio.Minio(
        endpoint='shift-minio.yc.ftc.ru',
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        region='russia',
    )

    bucket_name = 'shift-recognition-symbols'

    found = client.bucket_exists(bucket_name)
    if not found:
        raise Exception('Error, no such bucket!')
    else:
        print('Successfully found. Now downloading...')
        for file in files:
            result = os.path.join(destination, file) if destination else file
            client.fget_object(bucket_name, file, result, progress=Progress())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # parser.add_argument('file', type=str, help='Название скачиваемого файла')
    parser.add_argument(
        '--destination',
        type=str,
        default='dataset',
        required=False,
        help='Куда скачать файл',
    )

    args = parser.parse_args()
    try:
        with open('credentials.json', 'r') as cred:
            info = json.load(cred)
            ACCESS_KEY = info['accessKey']
            SECRET_KEY = info['secretKey']
        print('Successfully got keys from credentials.json')
    except:
        raise Exception('Error finding your access keys!')

    main(['DDI_new.zip', 'PDFA_new.zip', 'SROIE.7z'], args.destination)
