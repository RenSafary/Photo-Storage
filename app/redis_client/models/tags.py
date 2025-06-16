from models.Tags import Tags

def redis_tags(user):
    tags = Tags.select().where(Tags.user_id == user.id)
    tags_list = list(tags)

    tags_data = []

    for tag in tags_list:
        tags_data.append({
            "id": tag.id,
            "name": tag.name,
            "user_id": tag.user_id,
        })

    return tags_data