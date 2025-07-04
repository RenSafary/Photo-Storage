from models.Files import Files

def redis_files(user):
    files = Files.select().where(Files.user == user.id)
    files_list = list(files)
                    
    files_data = []
    for file in files_list:
        files_data.append({
            "id": file.id,
            "user_id": file.user_id,
            "folder_id": file.folder_id,
            "link": file.link,
            "date_uploaded": str(file.date_uploaded),
            "size": file.size_of_file_bytes,
            "tag_id": file.tag_id,
        })

    return files_data