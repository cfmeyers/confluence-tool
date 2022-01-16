# -*- coding: utf-8 -*-

"""Console script for confluence_tool."""
import sys

import click

from confluence_tool.confluence_tool import get_links, write_to_csv


@click.group()
def cli():
    pass


@cli.command()
@click.argument("page_id", type=str)
@click.argument("path_to_csv", type=str)
def crawl_links_for(page_id: str, path_to_csv: str):
    links = get_links(page_id)
    write_to_csv(links, path_to_csv)

    return 0


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
