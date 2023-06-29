class User:
    def __init__(self, user_id, first_name, last_name, photos):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.profile_link = f"https://vk.com/id{user_id}"
        self.photos = photos

    def __str__(self):
        return f"User({self.id}, {self.first_name}, {self.last_name}, {self.photos})"

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "profile_link": self.profile_link,
            "photos": self.photos,
        }
