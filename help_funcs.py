# Changing format to integer
def change_likes(likes):
    likes = likes.replace('.', '').replace(',', '.')
    if 'M' in likes:
        likes = likes.replace('M', '')
        likes = float(likes) * 100000
    elif 'K' in likes:
        likes = likes.replace('K', '')
        likes = float(likes) * 100
    return int(likes)


# Deleting hashtag from string
def del_hash(hashtag):
    return hashtag.replace('#', '')
