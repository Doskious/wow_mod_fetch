from datetime import datetime, timezone, timedelta
import json


def dateFromWebkit(timestamp):
    epochStart = datetime(1601, 1, 1)
    delta = timedelta(microseconds=int(timestamp))
    return (epochStart + delta).replace(tzinfo=timezone.utc).astimezone()


class NamedItemList(list):
    """Named Item List, list based"""

    def iter_named_items(self, name):
        for item in self:
            if item.name == name:
                yield item


class Item(dict):
    """Item class, dict based. properties:
        `id`, `name`, `type`, `url`, `folders`, `urls`"""

    @property
    def id(self):
        return self["id"]

    @property
    def name(self):
        return self["name"]

    @property
    def type(self):
        return self["type"]

    @property
    def url(self):
        if "url" in self:
            return self["url"]
        return ""

    @property
    def added(self):
        return dateFromWebkit(self["date_added"])

    @property
    def modified(self):
        if "date_modified" in self:
            return dateFromWebkit(self["date_modified"])

    @property
    def folders(self):
        items = NamedItemList()
        for children in self["children"]:
            if children["type"] == "folder":
                items.append(Item(children))
        return items

    @property
    def urls(self):
        items = NamedItemList()
        for children in self["children"]:
            if children["type"] == "url":
                items.append(Item(children))
        return items


class Bookmarks:
    """Bookmarks class. attrs: `path`. properties: `folders`, `urls`"""
    path = None

    def __init__(self, path):
        self.path = path
        with open(path, encoding="utf-8") as f:
            self.data = json.load(f)
        self.attr_list = {"urls": NamedItemList(), "folders": NamedItemList()}
        self.processRoots()

    @property
    def urls(self):
        return self.attr_list["urls"]

    @property
    def folders(self):
        return self.attr_list["folders"]

    def processRoots(self):
        with open(self.path, encoding="utf-8") as f:
            roots_data = json.load(f)
        for value in roots_data["roots"].values():
            if "children" in value:
                self.processTree(value["children"])

    def processTree(self, childrenList):
        for item in childrenList:
            self.processUrls(item)
            self.processFolders(item)

    def processUrls(self, item):
        if "type" in item and item["type"] == "url":
            self.attr_list["urls"].append(Item(item))

    def processFolders(self, item):
        if "type" in item and item["type"] == "folder":
            self.attr_list["folders"].append(Item(item))
            if "children" in item:
                self.processTree(item["children"])
