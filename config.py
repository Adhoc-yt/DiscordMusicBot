"""
This script will load the configuration of the bot
"""
import json

# load the configuration
CONFIG: dict = json.load(open("config.json"))
# load banned ids
BANNED_ID: dict = json.load(open("banned_id.json"))


# create the data class
class config:
    """
    Create a class for the full configuration

    - authorized link: source fore music authorized
    - music_folder: The folder where music will be stored
    - encoder: the encoder that will be used
    """

    authorized_link: [str] = CONFIG["CONFIG"]["authorized link"]
    music_folder: str = CONFIG["CONFIG"]["music folder"]
    encoder: str = CONFIG["CONFIG"]["encoder"]

    class play:
        """
        configuration for the play command
        This command start playing a song
        - Activate: if this function can be used
        - role: role that can use this command
        """
        ACTIVATE: bool = CONFIG["play"]["ACTIVATE"]
        role: [str] = CONFIG["play"]["role"]

    class stop:
        """
        configuration for the stop command
        This function stop the music that is playing
        - Activate: if this function can be used
        - role: role that can use this command
        - Self: if the person who start the music can stop it
        """
        ACTIVATE: bool = CONFIG["stop"]["ACTIVATE"]
        role: [str] = CONFIG["stop"]["role"]
        Self: bool = CONFIG["stop"]["self"]

    class pause:
        """
        configuration for the pause command
        This function pause the music that is playing
        - Activate: if this function can be used
        - role: role that can use this command
        - Self: if the person who start the music can pause the music
        """
        ACTIVATE: bool = CONFIG["pause"]["ACTIVATE"]
        role: [str] = CONFIG["pause"]["role"]
        Self: bool = CONFIG["pause"]["self"]

    class resume:
        """
        configuration for the resume command
        This function restart the music after a pause
        - Activate: if this function can be used
        - role: role that can use this command
        - Self: if the person who start or pause the music can resume the music
        """
        ACTIVATE: bool = CONFIG["resume"]["ACTIVATE"]
        role: [str] = CONFIG["resume"]["role"]
        Self: bool = CONFIG["resume"]["self"]

    class skip:
        """
        configuration for the skip function
        This function stop the music that is playing and play the new in queue
        (or stop the music if there is nothing in queue)
        - Activate: if this function can be used
        - role: role that can use this command
        - Self: if the person who start the music can skip it
        """
        ACTIVATE: bool = CONFIG["skip"]["ACTIVATE"]
        role: [str] = CONFIG["skip"]["role"]
        Self: bool = CONFIG["skip"]["self"]

    class leave:
        """
        configuration for the leave function
        This function disconnect the bot from the channel
        - Activate: if this function can be used
        - role: role that can use this command
        """
        ACTIVATE: bool = CONFIG["leave"]["ACTIVATE"]
        role: [str] = CONFIG["leave"]["role"]

    class skip_vote:
        """
        configuration for the skip vote functionality
        This functionality allow users to vote to skip a music
        if this functionality is enable, the normal skip function can only be used by the user who start the music
        - ACTIVATE: if this functionality is enable
        - rate: the rate of person in channel who want skip
        """
        ACTIVATE: bool = CONFIG["skip vote"]["ACTIVATE"]
        rate: float = CONFIG["skip vote"]["rate"]

    # contain every user ids that can't used the bot
    banned_ids: [int] = BANNED_ID["banned ids"]
