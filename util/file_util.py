import os
from os.path import isfile, join


class FileUtil:
    """Classe utilitária com operações de arquivos."""

    @staticmethod
    def check_json_file(fileName):
        """Checa se o arquivo json foi criado."""
        onlyfiles = [f for f in os.listdir('files/') if isfile(join('files/', f))]
        return fileName in onlyfiles