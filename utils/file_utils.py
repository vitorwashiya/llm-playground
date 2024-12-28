import os


def create_directories(directories, models):
    for dir in directories:
        if not os.path.exists(dir):
            os.makedirs(dir)
    for model in models:
        model_name = model.replace(":", "_").replace(".", "_")
        model_dir = os.path.join('faiss', model_name)
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)


def list_folder(directory):
    return [
        f for f in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, f))
    ]


def list_pdf_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.pdf')]
