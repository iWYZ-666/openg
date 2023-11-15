import os


def get_rel_path(path):
    main_file_path = os.path.abspath(__file__)
    main_dir = os.path.dirname(main_file_path)
    conf_file_path = os.path.join(main_dir, path)
    return conf_file_path


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
