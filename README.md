# Go through a bunch of awesome lists in the awesome-list Github topic, from the comfort of your terminal!

Inspired by the very nice [awesome-cli by umutphp](https://github.com/umutphp/awesome-cli).
This tool is different in that it allows you to explore almost every (read: up to 1000 retrieved by stat such as stars or creation time) repository in the "awesome-list" Github topic.

To avoid making you scrape a bunch of webpages (and to avoid bullying the Github API), the approach is the following:

- A database of repository names/links/descriptions with relevant stats is provided by me, right here in the repository, and updated once at least once a week.

- When you use the command, an interactive paged list will be presented to you.

- Select one, and only then the contents of the readme are scraped and processed a little bit for reading in your terminal with clickable links.

- If you want to refresh the database, pass the `--refresh` argument, which will fetch the database from this repository.

P.S. Want to build the database yourself? Please see [this section](#build-the-database-yourself).

Includes a **random mode**. When you use random, a random link (with frontmatter excluded) from a random repository's readme in the topic is selected and printed to standard output for manual clicking.

## Install

### Arch-based

TODO
This package has a release on the [Arch User Repository](TODO).

# Makefile for Linux, FreeBSD, MacOS, and Linux subsystem for Windows (See FAQ for non-Linux!)

- Download tarball from releases
- Extract tarball
- Move into extracted folder
- Run:

```bash
make install
```

### PyPI for all platforms (requires pip) (See FAQ for non-Linux!)

```bash
pipx install discover-awesome
```

You can also use pip instead of pipx if you're comfortable with possible conflicts with your system packages.

### Manual for all platforms (requires pip) (See FAQ for non-Linux!)

- Download tarball from releases
- Extract tarball
- Move into extracted folder
- Run:

```bash
pipx install setup.py
```

You can also use pip instead of pipx if you're comfortable with possible conflicts with your system packages.

## Usage

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

### Build the database yourself

If you want to use the Github API to build the databases directly rather than relying on my updates, please pass one of the following arguments, replacing GITHUB_PERSONAL_ACCESS_TOKEN with a personal access token associated with your Github account (just setting it up for reading public repositories will do fine):

```bash
discover-awesome --buildDatabase GITHUB_PERSONAL_ACCESS_TOKEN
```

```bash
discover-awesome -b GITHUB_PERSONAL_ACCESS_TOKEN
```

## Planned features

- Use random mode within a specific repository
- Search for specific topics (implemented through fuzzy search in the repo tags)
- Repository and topic blacklist
- Save option, allowing you to save a README for a repo you like to a folder of choice
- Fetch database from repo only works if the repo's copies are newer than your local copies

## Features I will not implement myself

- Walking the markdown documents interactively or extracting just the links and descriptions. People all format their stuff a bit different. I tried, but it's too tricky.

## (maybe) FAQ

- Q: Is FreeBSD, Windows or MacOS supported?
  A: Not explicitly because I don't use these platforms, but it should still work totally fine. Please mention it in your bug reports if using one of these platforms.
