# Go through a bunch of awesome lists in the awesome-list Github topic, from the comfort of your terminal!

Inspired by the very nice [awesome-cli by umutphp](https://github.com/umutphp/awesome-cli).

discover-awesome allows you to explore almost every (up to 1000 retrieved by stat such as stars or creation time) repository in the "awesome-list" Github topic.

To avoid making you scrape a bunch of webpages (and to avoid bullying the Github API), the approach is the following:

- Databases of repository names/links/descriptions with relevant stats are provided by me, right here in the repository, and updated at least once a week.

- Before your first run, you must provide a personal access token with --token. The token will be saved in your local config in your user dir. It doesn't need any special permissions, it's simply your ticket for the Github API.

- On your first run, the database files downloaded with your release/package are copied to your user dir.

- Now you can use the tool for real, and an interactive paged list will be presented to you.

- Select one, and only then the contents of the readme are requested and processed a little bit for reading in your terminal with clickable links.

- If you want to get potentially new databases from this repo, pass the `--fetchDatabase` argument, which will fetch them from this repository. 

Want to build the database yourself? Please see [this section](#build-the-database-yourself)




# IMPORTANT
 - When I or you build the databases, we request the data from Github by a stat, such as most stars or oldest created. I have chosen this because of the API hard limiting you up to 1000 repositories for a tag/topic, but you can get different data if you request by stat in the first place. 
This means there are multiple databases which were requested by stat. Choose the one you want with the --database argument.
- The menu and readme output is made using the rich library. As far as I can tell, you do not ctrl+click the links in the outputs/menus rich creates as you normally would in a terminal. You must click them as you would a link on the web!

## Install 

*(Every method requires pip, which often comes with python depending on your platform.)*

### Makefile for Most Unix-like (Linux, *BSD, MacOS, etc.) + Linux subsystem for Windows (See FAQ for non-Linux!)

- Download tarball from releases
- Extract tarball
- Move into extracted folder
- Run:

```bash
make install
```

To uninstall move to the directory again and run:
```bash
make uninstall
```

And then delete your downloaded source files.

Please note the **install** part of this method used in the makefile is being deprecated soon by Python. I will replace it in the near future with a non-deprecated one. The uninstall is not being deprecated.

### Manual for all platforms (See FAQ for non-Linux!)

- Download tarball from releases
- Extract tarball
- Move into extracted folder
- Run:

```bash
python setup.py sdist bdist_wheel
pipx install dist/discover_awesome-0.1.0-py3-none-any.whl 
```

To uninstall, simply run this anywhere:
```bash
pipx uninstall discover-awesome
```

And then delete your downloaded source files.

Please note the **install** part of this method used in the makefile is being deprecated soon by Python. I will replace it in the near future with a non-deprecated one. The uninstall is not being deprecated.
## Usage

### Default
Will use the most stars database by default.

```bash
discover-awesome
```

### Fetch database from this repo

To fetch databases from this repo to replace your local databases of repos (no READMEs are stored in the databases so your space is respected):

```bash
discover-awesome --fetchDatabase
```

```bash
discover-awesome -f
```

### Choose a database

**IMPORTANT: Please read the IMPORTANT section at the beginning.**

```bash
discover-awesome --database <option>
```
```bash
discover-awesome -d <option>
```

The options are:
- Most stars (most)
- Least stars (least)
- Most recently created (newest)
- Least recently created (oldest)
- Recently updated (recently-updated)
- Least recently updated (least-recently-updated)

### Build the database yourself

If you want to use the Github API to build the databases directly rather than relying on my updates, please pass one of the following arguments:

```bash
discover-awesome --buildDatabase 
```

```bash
discover-awesome -b
```

This will take a minute.


## Bugs to fix:
  I want to clear the terminal when you request a readme so the table doesnt stay there. But when I do, you egt both your current readme AND previous readme?? I cannot for the life of me figure it out so the table stays beacause that's by far the better option readability wise.

## Planned features

- Random mode
- Search for specific topics
- Repository and topic blacklist
- Save option, allowing you to save a README for a repo you like to a folder of choice
- Fetch database from repo only works if the repo's copies are newer than your local copies

## Features I will not implement myself

- Walking the markdown documents interactively or extracting just the links and descriptions. People all format their stuff a bit different. I tried, but it's too tricky.

## (maybe) FAQ

- Q: Is *BSD, Windows or MacOS supported?
  - A: Not explicitly because I don't use these platforms, but it should still work totally fine. Please mention it in your bug reports if using one of these platforms.
- Q: Can I get more than 1000 repos per database?
  - A: No. This is a hard limit in the Github API unfortunately.
