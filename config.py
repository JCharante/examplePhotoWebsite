project_directories = {
    'JCharante': '/home/jcharante/Projects/ePW',
    'Nutmeag': '/home/student/examplePhotoWebsite'
}


current_developer = 'Nutmeag'


def path_to_db():
    return 'sqlite:///' + project_directories[current_developer] + '/database.db'


def image_storage_path():
    return project_directories[current_developer] + '/images'
