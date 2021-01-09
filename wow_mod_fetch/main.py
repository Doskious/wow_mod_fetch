""" Browser and Filesystem Automation for WoW AddOn Updates """
import argparse
import datetime
import pathlib
import time
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from chrome_bookmarks import instance as chrome_bookmarks


WINDOW_SIZE = "1920,1080"
ADDON_BASE_DIR = (
    '~/Games/world-of-warcraft/drive_c'
    '/Program Files (x86)/World of Warcraft/_retail_/Interface/AddOns')
ADDON_BASE_PATH = pathlib.Path(ADDON_BASE_DIR).expanduser()
USER_DL_DIR = "~/Downloads/pywowmods/"
WOW_DL_DIR = pathlib.Path(USER_DL_DIR).expanduser()


def check_for_updates(path):
    """ See if the downloaded Zip has an update! """
    do_updates = []
    with zipfile.ZipFile(path) as mod_zip:
        for new_file in mod_zip.infolist():
            # check if same file exists in AddOn Dir
            existing_file = pathlib.Path(pathlib.os.path.join(
                ADDON_BASE_DIR, new_file.filename))
            if not existing_file.exists():
                do_updates.append(True)
                continue
            existing_ctime = datetime.datetime.fromtimestamp(
                existing_file.stat().st_ctime)
            new_ctime = datetime.datetime(*new_file.date_time)
            # print(existing_ctime, new_ctime, existing_ctime < new_ctime)
            do_updates.append(existing_ctime < new_ctime)
        if any(do_updates):
            print(f"Updating {mod_zip}")
            mod_zip.extractall(ADDON_BASE_PATH)
    path.unlink()


class ModZipFileHandler(PatternMatchingEventHandler):
    """ Handling WoW AddOn Zip Files! """
    patterns = ("*.zip", "*.crdownload")
    created_count = 0
    completed_count = 0

    @property
    def count_match(self):
        """truth check controlling exit, based on target/successful fetches"""
        return self.created_count == self.completed_count

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.downloads_started = []

    def on_any_event(self, event):
        # print(event)
        pass

    def on_created(self, event):
        if event.src_path.endswith(".crdownload"):
            if event.src_path not in self.downloads_started:
                self.created_count += 1
                self.downloads_started.append(event.src_path)

    def on_moved(self, event):
        if event.src_path.endswith(".crdownload"):
            if event.dest_path.endswith(".zip"):
                self.wait_for_completion(event.dest_path)

    def wait_for_completion(self, path):
        """ensure that files are only processed after download completion"""
        file_size = -1
        while file_size != pathlib.os.path.getsize(path):
            file_size = pathlib.os.path.getsize(path)
            time.sleep(1)

        self.completed_count += 1
        check_for_updates(pathlib.Path(path))


def fetch():
    """Start the Watchdog and pull the downloads!"""
    wow_bookmarks = chrome_bookmarks.folders.iter_named_items(
        'WoW Addon Downloads')
    addon_urls = []
    target_count = 0
    for bookmark_folder in wow_bookmarks:
        for bookmark in bookmark_folder.urls:
            target_count += 1
            addon_urls.append(f'window.open("{bookmark.url}","_blank");')
    event_handler = ModZipFileHandler()
    observer = Observer()
    prefs = {"download.default_directory" : f"{WOW_DL_DIR.absolute()}"}
    chrome_options = Options()
    chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")
    chrome_options.add_experimental_option("prefs", prefs)
    observer.schedule(event_handler, WOW_DL_DIR)
    observer.start()
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get("https://allegiance.bastion-rising.net/")
        for spawn_download_tab in addon_urls:
            driver.execute_script(spawn_download_tab)
            time.sleep(4)
        count_pairity_count = 0
        while count_pairity_count < 10 and\
              (not event_handler.count_match or
               event_handler.created_count < target_count):
            if event_handler.count_match:
                count_pairity_count += 1
                # print(event_handler.created_count,
                #       target_count, count_pairity_count)
            time.sleep(2)
    observer.stop()
    observer.join()


def resume():
    """ Iterate over any zip files in the target directory for new mods """
    for mod_file in WOW_DL_DIR.iterdir():
        if mod_file.suffix != ".zip":
            continue
        check_for_updates(mod_file)


def main(parsed_args):
    """argument-based execution logic"""
    if not WOW_DL_DIR.exists():
        WOW_DL_DIR.mkdir()
    if parsed_args.resume:
        resume()
    else:
        fetch()


class ParseArgs(argparse.ArgumentParser):
    """Class-based ArgParse for cleaner invocation block"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        group = self.add_mutually_exclusive_group()
        group.add_argument(
            "-r", "--resume", help="process existing archived addons",
            action="store_true")
        group.add_argument(
            "-g", "--get", help="download addons, install updates (default)",
            action="store_true", default=True)


if __name__ == '__main__':
    parser = ParseArgs()
    main(parser.parse_args())
