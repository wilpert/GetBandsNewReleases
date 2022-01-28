# GetBandsNewReleases

Search the awesome Encyclopaedia Metallum for bands' albums you do not have yet in your collection.

This assumes that you store your music collection locally or at least that you have full access to the metadata stored in your collection. I know, this is nowadays not common anymore... The main challenge for you will probably be to extract the metadata from your collection in an automated way; I use for this the application TagScanner from Sergey Serkov (https://www.xdlab.ru/en/): it delivers a CSV file with all the metadata I need, which I convert then to the JSON format with a small piece of Python code.

One note about the genre classification: in the example you will find in this repository a band is classifed as *metal* only if it is listed in the Encyclopaedia Metallum, everything else is tagged as *rock*. Not everyone will agree with the criteria used by the Encyclopaedia Metallum (hey, I hear you, Slipknot ist not metal??), but they use a strict definition that is well explained (see here, if you care: https://www.metal-archives.com/content/rules) and for me, it is a reference I want to rely upon.

## Dependencies

The script has been written in the Python programming language and tested with Python 3.8, but it should work with any version of Python 3, probably also with Python 2, after some minor changes.

The script depends on only one external module to work: python-metalum from Lachlan Charlick (https://github.com/lcharlick/python-metallum). Thanks, Lachlan, for your work!

Nothing here would make sense without the work done by the Encyclopaedia Metallum (a.k.a. The Metal Archives, https://www.metal-archives.com/), an incredible amount of high-quality information on everything metal. Thank you so much! \m/ 

## Usage

Currently, there is no documentation except for the comments scattered in the code and probably there is no need for much more than that, as the script is very simple.

    usage: GetBandsNewReleases.py [-h] -a ALBUMLIST -r RELEASE_INTERVAL [-s SKIP_BANDS] [-d DISAMBIGUATIONS] [-k]

    optional arguments:
      -h, --help            show this help message and exit
      -a ALBUMLIST, --albumlist ALBUMLIST
                            The File (in JSON format) with the bands to check for new releases
      -r RELEASE_INTERVAL, --release_interval RELEASE_INTERVAL
                            Interval in years (for example 2010-2016 or 2010-2010) within (and including) it will be
                            searched for new releases
      -s SKIP_BANDS, --skip_bands SKIP_BANDS
                            A file (in JSON format) with the bands to be skipped from the check
      -d DISAMBIGUATIONS, --disambiguations DISAMBIGUATIONS
                            A file (in JSON format) with disambiguation information in case of bands with the same name
      -k, --skip_splitup_bands
                            Skip bands, whose status is listed as "Split-up"


Only the first two arguments are required: the JSON file with the bands and albums in your collection and the release interval. You will find examples for all the input files (album list, skip-bands list and disambiguations list) in the data/ directory.

Just only one comment about the bands' IDs that are kept in the list with the disambiguations: You will find this ID in the URL for the band page; for example, in case of Metallica this ID is 125 (https://www.metal-archives.com/bands/Metallica/125). There is also a way of retrieving this ID using the python API exposed by the module python-metallum, and this is indeed done in the script to compare the bands' IDs.

## Disclaimer

This project was born out of my love for metal music and for searching for an automated way of checking for new releases in my rather-bigger-than-small collection. If you find any bugs that I am not aware of I would be glad, if you would take the time to report them, but I cannot promise that I will extend the functionality.

I cannot either guarantee that the Encyclopedia Metallum site will continue supporting this type of access to their servers in the future. Also, the connection to their servers does not always work as desired: sometimes it takes a lot of time before establishing the initial connection; sometimes it gets lost while still searching for albums. There is nothing I can do here, just be patient and try later again. AFAIK the service provided by the Encyclopedia Metallum is for free and am I immensely grateful for having access to such wealth of information.
