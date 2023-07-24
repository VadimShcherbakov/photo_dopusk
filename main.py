# Этот скрипт позволяет разделять фотографии с носимых видеорегистраторов и перекидывать их в папку по дате съемки
import os
import shutil
import datetime
from datetime import datetime
from tqdm import tqdm


def delete_folder(dir: str) -> None:
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)


def get_size(start_path: str) -> str:
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


def move_file(start_path: str, end_path: str) -> None:
    if get_size(start_path) == 0:
        print('Файлов - нет')
        return
    for path, dirs, files in os.walk(start_path):
        for f in tqdm(files, ncols=80, ascii=True, desc='Total'):
            fp = os.path.join(path, f)
            folder_name = datetime.utcfromtimestamp(os.path.getmtime(fp)).strftime('%d-%m-%Y')
            end_way = os.path.join(end_path, folder_name + '/')
            if not os.path.isdir(end_way):
                os.mkdir(end_way)
            shutil.move(fp, end_way)
    print('Перенос файлов выполнен')


if __name__ == '__main__':
    my_dict_way = {'video': ['Movie', 'Видео с регистраторов'], 'photo': ['Photo', 'фото_допуска']}
    for k, v in my_dict_way.items():
        start_path = f'e:/DCIM/{v[0]}/'
        end_path = f'g:/{v[1]}/'
        move_file(start_path, end_path)


