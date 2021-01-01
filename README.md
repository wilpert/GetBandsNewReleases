# GetBandsNewReleases

Search the awesome Encyclopaedia Metallum for bands' albums you do not have yet in your collection.

## Dependencies

The script has been written in the Python programming language and tested with Python 3.8, but it should work with any version of Python 3, perhaps even with Python 2 after some minor changes.

The script depends on only one external module to work: python-metalum from Lachlan Charlick (https://github.com/lcharlick/python-metallum). Thanks Lachlan for your work!

Nothing here would make sense without the work done by the Encyclopaedia Metallum (a.k.a. The Metal Archives, https://www.metal-archives.com/), an incredible amount of high-quality information on everything metal. Thank you so much! \m/ 

## Usage

Currently there is no documentation except for the comments scattered in the code and probably there is no need for much more than that, as the script is very simple.

    usage: GetBandsNewReleases.py [-h] -a ALBUMLIST -y THRESHOLD_YEAR [-s SKIP_BANDS] [-d DISAMBIGUATIONS] [-k]

    optional arguments:
      -h, --help            show this help message and exit
      -a ALBUMLIST, --albumlist ALBUMLIST
                            The File (in JSON format) with the bands to check for new releases
      -y THRESHOLD_YEAR, --threshold_year THRESHOLD_YEAR
                            Starting from which year (included) should the new releases be searched for
      -s SKIP_BANDS, --skip_bands SKIP_BANDS
                            A file (in JSON format) with the bands to be skipped from the check
      -d DISAMBIGUATIONS, --disambiguations DISAMBIGUATIONS
                            A file (in JSON format) with disambiguation information in case of bands with the same name
      -k, --skip_splitup_bands
                            Skip bands, whose status is listed as "Split-up"

Only the first two arguments are obligatory: the JSON file with the bands and albums in your "collection" and the threshold date. You will find examples for all the input files (album list, skip-bands list and disambiguations list) in the data/ directory.

Just only one comment about the bands' IDs that are kept in the list with the disambiguations: You will find this ID in the URL for the band page; for example, in case of Metallica this ID is 125 (https://www.metal-archives.com/bands/Metallica/125). There is also a way of retrieving this ID using the python API exposed by the module python-metallum, but this is another story :-)

## Disclaimer

This project is a purely personal one, which was born out of my love for metal music and searching for an automatic way of checking for new releases in an automated. I cannot promise that I will extend the functionality, it just works as it is now for my purposes. Of course, if you find any bugs that I am not aware of I would be glad, if you would take the time to report them.

I cannot guarantee that the Encyclopedia Metallum will continue supporting this type of access to their servers in the future. Also, the connection to their servers does not always work as desired: sometimes it takes a lot of time before establishing the initial connection; sometimes it gets lost while still searching for albums. There is nothing I can do here, just be patient and try later again. AFAIK the service provided by the Encyclopedia Metallum is for free and I immensely grateful for having access to such wealth of information, by whatever means.
