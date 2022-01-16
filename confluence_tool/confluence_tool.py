# -*- coding: utf-8 -*-

"""Main module."""
import csv
import json
import os
from typing import Dict, List, NamedTuple, Optional

from bs4 import BeautifulSoup
from rich import pretty

pretty.install()

from atlassian import Confluence


def get_summary(body: str) -> str:

    soup = BeautifulSoup(body, features="html.parser")
    summary = ""
    for tr in soup.find_all("tr"):
        if tr.text.startswith("Summary"):
            summary = tr.text.split("Summary")[1]
    return summary


class Page(NamedTuple):
    title: str
    id: str
    type: str
    url: str
    summary: str
    children: List["Page"]

    @classmethod
    def from_response(cls, r, children):
        return cls(
            title=r["title"],
            id=r["id"],
            type=r["type"],
            url=r["_links"]["base"] + r["_links"]["webui"],
            summary=get_summary(r["body"]["export_view"]["value"]),
            children=children,
        )


def get_config() -> Dict[str, str]:
    path_to_config = os.path.expanduser("~/.confluence-tool-config.json")
    with open(path_to_config, "r") as f:
        config = json.load(f)
    return config


def get_page(confluence: Confluence, page_id: str) -> Page:
    page = confluence.get_page_by_id(
        page_id, expand="space,children.page,descendants.page,body.export_view"
    )
    children = []
    for child_id in get_child_page_ids(confluence, page_id):
        child_page = get_page(confluence, child_id)
        children.append(child_page)

    return Page.from_response(page, children=children)


def get_child_page_ids(confluence: Confluence, parent_id: str) -> List[str]:
    result = confluence.get_page_child_by_type(parent_id, type="page")
    return [r["id"] for r in result]


def get_urls_and_titles(parent_page: Page) -> List[Dict[str, str]]:
    flattened_links = []
    this_page = {
        "url": parent_page.url,
        "title": parent_page.title,
        "subtitle": parent_page.summary[:100],
    }
    flattened_links.append(this_page)
    for child_page in parent_page.children:
        flattened_links.extend(get_urls_and_titles(child_page))
    return flattened_links


def get_links(page_id: str) -> List[Dict[str, str]]:
    config = get_config()

    confluence = Confluence(
        url=config["url"],
        username=config["username"],
        password=config["token"],
        cloud=True,
    )

    results = confluence.get_all_pages_from_space(
        config["space"],
        start=0,
        limit=100,
        status=None,
        expand=None,
        content_type="page",
    )
    results

    data_team_page = get_page(confluence, page_id)

    flattened_links = get_urls_and_titles(data_team_page)
    return flattened_links


def write_to_csv(links: List[Dict[str, str]], path_to_csv: str):
    with open(path_to_csv, "w") as f:
        writer = csv.DictWriter(f, fieldnames=("title", "subtitle", "url"))
        for link in links:
            writer.writerow(link)
