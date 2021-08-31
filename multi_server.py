"""
All functions and class for multi server management
"""


class ServerMusic:
    """
    This class contain every functions for music settings for each servers
    """

    def __init__(self):
        """
        Init the main data for a all servers

        BASE_DATA :
         - actual: the actual path of the music
         - user actual: the id of the user who choose the music
         - queue: every future music as link (not path)
         - user queue: list of all user id who choose music in queue
         - joined: if the bot is actually in a channel
         - pause: if the bot is actually paused
        """

        self.BASE_DATA: dict = {"actual": "",
                                "title actual": "",
                                "user actual": 0,
                                "queue": [],
                                "user queue": [],
                                "title queue": [],
                                "joined": False,
                                "pause": False
                                }

        self.SERVER_DATA: dict = {}

    def check_guild_exist(self, guild_id: int):
        """
        This function retur if the guild in parameter is already in memory
        if the guild is not in memory it create the guild in memory
        :param guild_id:
        :return: None
        """
        if str(guild_id) not in self.SERVER_DATA:
            self.add_guild(guild_id)

    def add_guild(self, guild_id: int) -> None:
        """
        This function add guild in memory and every information about it
        :param guild_id: None
        :return:
        """
        self.SERVER_DATA[str(guild_id)] = self.BASE_DATA

    def add_music(self, guild_id: int, music_path: str, user_id: int, title: str) -> None:
        """
        This function will add a music as actual music if it is free or will put this new music in queue
        :param guild_id: the id of the guild where the bot play music
        :param music_path: the paths of the music file
        :param user_id: the id of the user who send the link
        :param title: the title of the music
        :return: None
        """
        self.check_guild_exist(guild_id)

        # if there is no music playing
        if self.SERVER_DATA[str(guild_id)]["actual"] == "":
            self.SERVER_DATA[str(guild_id)]["actual"] = music_path
            self.SERVER_DATA[str(guild_id)]["user actual"] = user_id
            self.SERVER_DATA[str(guild_id)]["title actual"] = title

        # if there is already a music playing
        else:
            self.SERVER_DATA[str(guild_id)]["queue"].append(music_path)
            self.SERVER_DATA[str(guild_id)]["user queue"].append(user_id)
            self.SERVER_DATA[str(guild_id)]["title queue"].append(title)

    def next_music(self, guild_id: int) -> None:
        """
        This function will change the actual music with the first music in the queue
        :param guild_id: the id of the guild where the sound will be changed
        :return: None
        """
        self.check_guild_exist(guild_id)

        # check if there is something in the queue
        if len(self.SERVER_DATA[str(guild_id)]["queue"]) > 0:
            # set the new music
            self.SERVER_DATA[str(guild_id)]["actual"] = self.SERVER_DATA[str(guild_id)]["queue"][0]
            self.SERVER_DATA[str(guild_id)]["user actual"] = self.SERVER_DATA[str(guild_id)]["user queue"][0]
            self.SERVER_DATA[str(guild_id)]["title actual"] = self.SERVER_DATA[str(guild_id)]["title queue"][0]
            # remove the actual music of the queue
            del self.SERVER_DATA[str(guild_id)]["queue"][0]
            del self.SERVER_DATA[str(guild_id)]["user queue"][0]
            del self.SERVER_DATA[str(guild_id)]["title queue"][0]

        else:
            self.SERVER_DATA[str(guild_id)]["actual"] = ""
            self.SERVER_DATA[str(guild_id)]["user actual"] = ""
            self.SERVER_DATA[str(guild_id)]["title actual"] = ""

    def clear_queue(self, guild_id: int) -> None:
        """
        This function will clear the queue
        :param guild_id: the id of the guild where the queue will be cleared
        :return: None
        """
        self.check_guild_exist(guild_id)

        self.SERVER_DATA[str(guild_id)]["queue"] = []
        self.SERVER_DATA[str(guild_id)]["user queue"] = []
        self.SERVER_DATA[str(guild_id)]["title queue"] = []

    # set methode

    def set_pause(self, guild_id: int) -> None:
        """
        This function set pause as True for the specified guild
        :param guild_id: the id of the guild
        :return: None
        """
        self.check_guild_exist(guild_id)

        self.SERVER_DATA[str(guild_id)]["pause"] = True

    def set_resume(self, guild_id: int) -> None:
        """
        This function set pause as False for the specified guild
        :param guild_id: the id of the guild
        :return: None
        """
        self.check_guild_exist(guild_id)

        self.SERVER_DATA[str(guild_id)]["pause"] = False

    def set_join(self, guild_id: int) -> None:
        """
        This function set joined as True for the specified guild
        :param guild_id: the id of the guild
        :return: None
        """
        self.check_guild_exist(guild_id)

        self.SERVER_DATA[str(guild_id)]["joined"] = True

    def set_leave(self, guild_id: int) -> None:
        """
        This function set joined as False for the specified guild
        :param guild_id: the id of the guild
        :return: None
        """
        self.check_guild_exist(guild_id)

        self.SERVER_DATA[str(guild_id)]["joined"] = False
