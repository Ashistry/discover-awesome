# Go through a bunch of awesome lists in the awesome-list Github topic, from the comfort of your terminal!

Inspired by the very nice [awesome-cli by umutphp](https://github.com/umutphp/awesome-cli).
This tool is different in that it allows you to explore almost every (read: up to 1000 retrieved by stat such as stars or creation time) repository in the "awesome-list" Github topic.

To avoid making you scrape a bunch of webpages (and to avoid bullying the Github API), the approach is the following:

- Databases of repository names/links/descriptions with relevant stats are provided by me, right here in the repository, and updated once at least once a week.

- On first run, you will be sent to GitHub to install discover-awesome-bot on your account to make authenticated API requests with.

- Then, when you use the tool, an interactive paged list will be presented to you.

- Select one, and only then the contents of the readme are requested and processed a little bit for reading in your terminal with clickable links.

- If you want to refresh the databases, pass the `--refresh` argument, which will fetch them from this repository. (P.S.: Want to build the database yourself? Please see [this section](#build-the-database-yourself).)

- Want an offline mode or don't want to authenticate with GitHub? Willing to reserve about 150MB for discover-awesome? Check out [discover-awesome-offline](TODO)




Includes a **random mode**. When you use random, a random link (with frontmatter excluded) from a random repository's readme in the topic is selected and printed to standard output for manual clicking.
 
# IMPORTANT
 When I or you build the databases, we request the data from Github by a stat, such as most stars or oldest created. I have chosen this because of the API hard limiting you up to 1000 repositories for a tag/topic, but you can get different data if you request by stat in the first place. 

This means there are multiple databases which were requested by stat. When using the tool, you choose a database to determine the repos available, which you can then sort by a different stat if you so desire.


## Install

### Arch-based

TODO
This package has a release on the [Arch User Repository](TODO).

### Makefile for Linux, FreeBSD, MacOS, and Linux subsystem for Windows (See FAQ for non-Linux!)

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
Will use the most stars database by default.

```bash
discover-awesome
```

### Refresh

To fetch databases from this repo to replace your local databases of repos (no READMEs are stored):

```bash
discover-awesome --refresh
```

```bash
discover-awesome -r
```

### Limit

The default limit for total repos to list in your terminal is the maximum 1000.

```bash
discover-awesome --limit <integer>
```

```bash
discover-awesome -l <integer>
```
### Choose a database

IMPORTANT: Please read the IMPORTANT section at the beginning.

```bash
discover-awesome --database <option>
```
```bash
discover-awesome -d <option>
```

The options are:
- Most stars (most_stars)
- Least stars (least_stars)
- Most recently created (newest_created)
- Least recently created (oldest_created)
- Recently updated (recently_updated)
- Least recently updated (least_recently_updated)


### Sorting

 IMPORTANT: Please read the IMPORTANT section at the beginning.

```bash
discover-awesome --sort <option>
```

```bash
discover-awesome -s <option>
```

The options are:
- Most stars (most_stars)
- Least stars (least_stars)
- Most recently created (newest_created)
- Least recently created (oldest_created)
- Recently updated (recently_updated)
- Least recently updated (least_recently_updated)

### Random

```bash
discover-awesome --random
```

```bash
discover-awesome -ra
```

When you use random mode, a random link (trying with frontmatter excluded) from a random repository in a random database's readme in the topic is selected and printed to standard output.

Will warn you about the risks of essentially opening random links on the internet (and confirm you want to do that) the first time you use it.

### Build the database yourself

If you want to use the Github API to build the databases directly rather than relying on my updates, please pass one of the following arguments, replacing GITHUB_PERSONAL_ACCESS_TOKEN with a personal access token (just setting it up for reading public repositories will do fine):

```bash
discover-awesome --buildDatabase GITHUB_PERSONAL_ACCESS_TOKEN
```

```bash
discover-awesome -b GITHUB_PERSONAL_ACCESS_TOKEN
```

## Planned features

- Use random mode within a specific repository or database
- Search for specific topics (implemented through fuzzy search in the repo tags)
- Repository and topic blacklist
- Save option, allowing you to save a README for a repo you like to a folder of choice
- Fetch database from repo only works if the repo's copies are newer than your local copies

## Features I will not implement myself

- Walking the markdown documents interactively or extracting just the links and descriptions. People all format their stuff a bit different. I tried, but it's too tricky.

## (maybe) FAQ

- Q: Is FreeBSD, Windows or MacOS supported?
  - A: Not explicitly because I don't use these platforms, but it should still work totally fine. Please mention it in your bug reports if using one of these platforms.
- Q: Can I get more than 1000 repos per database?
  - A: No. This is a hard limit in the Github API unfortunately.