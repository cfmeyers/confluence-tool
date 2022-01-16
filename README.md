# confluence-tool

A tool for dealing with Confluence on the command line

Requires a config json file at `~/.confluence-tool-config.json` with the following keys:
```
{
  "url": "<YOUR CONFLUENCE URL HERE>",
  "token": "<YOUR TOKEN HERE>",
  "username": "<YOUR USERNAME HERE (likely email)>",
  "space": "<SPACE YOU'RE OPERATING IN>"
}
```
An example URL might be `https://<YOUR COMPANY NAME>.atlassian.net`

Currently just crawls Confluence starting from a given parent page id, writes that page and all child pages to a csv file.
```sh
confluence-tool crawl-links-for <PAGE ID> <PATH TO CSV FILE>
```

Example:
```sh
confluence-tool crawl-links-for 75825157 ~/confluence-links.csv
```
