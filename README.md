# Go through a bunch of awesome lists in the awesome-list Github topic, from the comfort of your terminal!

Inspired by the very nice [awesome-cli by umutphp](https://github.com/umutphp/awesome-cli).
This tool is different in that it allows you to explore almost every (read: up to 1000 Most Starred or Last Updated within those same 1000 results) repository in the "awesome-list" Github topic.

To avoid making you scrape a bunch of webpages (and to avoid bullying the Github API), the approach is the following:

- A database of repository names/links/descriptions with relevant stats is provided by me, right here in the repository, and updated once at least once a week.

- When you use the command, an interactive paged list will be presented to you.

- Select one, and only then the contents of the readme are scraped and processed a little bit for reading in your terminal with clickable links.

- If you want to refresh the database, pass the ``--refresh`` argument, which will fetch the database from this repository if it is newer.

Includes a **random option**. When you use random, a random link (with frontmatter excluded) from a random repository's readme in the topic is selected and printed to standard output for manual clicking.


## Install:

### Arch-based:
TODO
This package has a release on the [Arch User Repository](TODO).

## Manual Installation
- Download a release or clone the project.
- Move into the release/project. 
- Run this command:

```bash
    python setup.py install
```
## Usage:

### Default

```bash
discover-awesome
```
### Refresh
To fetch a new version to replace your local database of repos (no READMEs are stored):
```bash
discover-awesome --refresh
```
```bash
discover-awesome -r
```

### Limit
The default limit for repos to list is unlimited.

```bash
discover-awesome --limit <integer>
```

```bash
discover-awesome -l <integer>
```

### Sorting
Repositories are sorted by most stars by default.

```bash
discover-awesome --sort <option>
```
```bash
discover-awesome -s <option>
```

The options are:

- most: Sort by most starred.
- least: Sort by least starred. 
- recent: Sort by most recently updated.
- oldest: Sort by least recently updated items.
- mostforks: Sort by the items with the most forks.
- leastforks: Sort by the items with the least forks.

### Random

```bash
discover-awesome --random
```

```bash
discover-awesome -ra
```
When you use random mode, a random link (trying with frontmatter excluded) from a random repository's readme in the topic is selected and printed to standard output.

Will warn you about the risks of essentially opening random links on the internet (and confirm you want to do that) the first time you use it.

## Planned features

- Use random mode within a specific repository
- Search for specific topics (implemented through fuzzy search in the repo tags)
- Repository and topic blacklist
- Save option, allowing you to save a README for a repo you like to a folder of choice

## Features I will not implement myself
- Walking the markdown documents interactively or extracting just the links and descriptions. People all format their stuff a bit different. I tried, but it's too tricky.

## (maybe) FAQ

- Q: Can I build the database myself?
    A: Yes! Please put an **appropriately scope-limited** personal Github access token in the config (~.config/discover-awesome.yaml) and run the tool with the --build-database argument. 
- Q: Is Windows or MacOS supported?
    A: Not explicitly, but the manual install should still work fine. I will not handle bug reports for these platforms.
