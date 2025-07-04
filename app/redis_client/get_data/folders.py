from models.Folders import Folders

def redis_folders(user):
    folders = Folders.select().where(Folders.user == user.id)
    folders_list = list(folders)

    folders_data = []

    for folder in folders_list:
        folders_data.append({
            "id": folder.id,
            "name": folder.name,
            "user_id": folder.user_id,
        })
    
    return folders_data