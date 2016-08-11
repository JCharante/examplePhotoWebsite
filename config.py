db_paths = {
    'JCharante': 'sqlite:////home/jcharante/Projects/ePW/database.db',
    'Nutmeag': 'sqlite:////home/student/examplePhotoWebsite/database.db'
}

current_developer = 'JCharante'


def path_to_db():
    return db_paths[current_developer]
