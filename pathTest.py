download_folder = os.path.expanduser("~/Downloads")
        directory = os.path.join(download_folder, "Arquivo_LGQIA+")
        if not os.path.exists(directory):
            os.makedirs(directory)
            subdirectories = [
                os.path.join(directory, "Questionários_gerados"), 
                os.path.join(directory, "Registro")
                ]