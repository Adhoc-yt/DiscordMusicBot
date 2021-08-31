"""
This module contain every independent function
"""
from datetime import datetime
import requests
import os
import shutil

from bs4 import BeautifulSoup


def console_log(log: str) -> None:
    """
    This function log in the console with the date a log
    :param log: a text to log
    :return: None
    """
    print(f"{datetime.now()}: {log}")


def has_role(user_roles: list, roles: list) -> bool:
    """
    This function return True is the user has any role in role
    :param user_roles: roles owned by the user
    :param roles: list of roles to have
    :return: True if the user has any roles in common with the role list else return false
    """
    # for each role owned by the user
    for u_role in user_roles:
        # for each role in list of roles
        for g_role in roles:

            if u_role == g_role:
                return True

    return False


def check_link(link: str, list_link: [str]) -> bool:
    """
    This function will check if the domaine in link is in list_link and return true if the link have the good domains
    :param link: the link to check
    :param list_link: a list of domain to check
    :return:
    """
    # for each domain
    for domain in list_link:
        # check if the link is long enough
        if len(link) > len(domain):
            # check the domain
            if link[:len(domain)] == domain or link[1:len(domain) + 1] == domain:
                return True
    return False


def delete_music_folder() -> None:
    """
    This function will delete the entire content of the music folder
    :return: None
    """
    folder = '/music/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))