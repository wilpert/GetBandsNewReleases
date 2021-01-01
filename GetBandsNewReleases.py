import argparse
import codecs
import datetime
import json
import sys

# https://github.com/lcharlick/python-metallum
import metallum


class CSVData(object):
    # define some colors
    red_ansi_code = "91"
    green_ansi_code = "92"
    yellow_ansi_code = "93"

    def __init__(self, albumlist_fname, disambiguations_fname, skip_bands_fname):

        self.bands_data = {}
        self.disambiguations = {}
        self.skip_bands = []

        # load the list of disambiguations
        if disambiguations_fname:
            with codecs.open(disambiguations_fname, 'r', encoding='utf-8') as disambiguations_f:
                for disambiguation in json.load(disambiguations_f):
                    self.disambiguations[disambiguation["band"]] = disambiguation["metallum_band_id"]

        # load the list with the bands to be skipped from the search
        if skip_bands_fname:
            with codecs.open(skip_bands_fname, 'r', encoding='utf-8') as skip_bands_f:
                self.skip_bands = json.load(skip_bands_f)

        # load the list of bands with albums owned
        with codecs.open(albumlist_fname, 'r', encoding='utf-8') as albumlist_f:
            for band_dct in json.load(albumlist_f):
                band_name = band_dct["band"]
                genre = band_dct["genre"]
                # filtering condition: include a band only if
                # - the band is not included in the list of bands to be skipped
                # - the genre of the band ist "Metal" (other bands are excluded from Encyclopaedia Metallum)
                if band_name not in self.skip_bands and genre == "Metal":
                    self.bands_data[band_name] = band_dct

    def get_albums_for_band(self, band):
        """
        return a list of all the albums owned for a given band
        :param band: name of the band
        :return: dictionary with the list of albums and corresponding release dates (only years) for the band
        """
        albums_found = {}
        if band in self.bands_data:
            for single_album in self.bands_data[band]["albums"]:
                albums_found[single_album["album"]] = single_album["year"]
        return albums_found

    def is_album_in_collection(self, band, album_title):
        """
        check if a given album of a given band is found in collection (self.bands_data)
        :param band: name of the band
        :param album_title: the title of the album
        :return: True, if the album is found in collection, False otherwise
        """
        is_in_collection = False
        if album_title in self.get_albums_for_band(band):
            is_in_collection = True
        return is_in_collection

    def band_needs_disambiguation(self, band, metallum_band):
        """
        check whether a band is found in the disambiguation list and if so whether its disambiguation id matches the id
        in Encyclopaedia Metallum; if the band is not found in disambiguation list (typically because there is only one
        band matching the band's name), continue searching for new releases for the band
        :param band: name of the band
        :param metallum_band: the band in Encyclopaedia Metallum (object with several properties, e.g. the band's id)
        :return: True, if the band is found in the disambiguation list and the band's id in Encyclopaedia Metallum
        does not match the id set in the disambiguation list, otherwise False
        """
        needs_disambiguation = False
        if band in self.disambiguations:
            if not metallum_band.id == self.disambiguations[band]:
                needs_disambiguation = True  # skip band from the search
        return needs_disambiguation

    def find_new_releases(self, args_threshold_year, args_skip_splitup_bands):
        """
        for each band in the collection list the albums not owned that have been released after a given year
        :param args_threshold_year: a release year, from which to search for new albums
        :param args_skip_splitup_bands: if True, bands, whose status is listed as "Split-up" will be skipped
        :return: nothing, this function prints only log messages and writes a json file with the new releases
        """
        new_releases = []

        for band in self.bands_data:
            bands = metallum.band_search(band)
            disambiguation_found = False

            # check whether the band is listed in Encyclopaedia Metallum
            if bands:

                sys.stdout.write("[BAND] {0}".format(band))

                # log the case that there are several bands with the same band's name, but no disambiguation was found;
                # if so, the band is skipped and a new entry with the correct band's id should be added to the list
                # with the disambiguations
                if len(bands) > 1 and band not in self.disambiguations:
                    sys.stdout.write("\x1b[{0}m [AMBIGUOUS_BAND_NAME]\x1b[0m\n".format(CSVData.red_ansi_code))
                else:

                    # the band's name can be used by several bands, process each one separately
                    for metallum_band in bands:

                        # continue (do not skip band) only if:
                        # - the band's name is not found in the disambiguation list, most likely because there is only
                        #   one band matching the band's name
                        # - the band's name is found in the disambiguation list and the band's id in Encyclopaedia
                        #   Metallum matches the id set in the disambiguation list
                        if not self.band_needs_disambiguation(band, metallum_band):

                            # remember whether a disambiguation is needed for the band and one was found; this
                            # information is used to report the rare condition checked below
                            disambiguation_found = True

                            metallum_band_page = metallum_band.get()

                            # trace down which bands have split-up; this information could be used to add this bands
                            # to the list of bands to be skipped and so decrease the searching time. We do not want
                            # to skip them by default because it could be useful to look for other band's albums than
                            # he latest ones, and who knows: perhaps the band reunite again under the same name; if
                            # you want to skip them, use the --skip_splitup_bands switch
                            if metallum_band_page.status == "Split-up":
                                sys.stdout.write(" \x1b[{0}m[SPLIT-UP]\x1b[0m".format(CSVData.yellow_ansi_code))
                                if args_skip_splitup_bands:
                                    sys.stdout.write(" \x1b[{0}m[SKIPPED]\x1b[0m\n".format(CSVData.yellow_ansi_code))
                                    continue

                            # get the list of all the albums in Encyclopaedia Metallum for the given band
                            metallum_albums = metallum_band_page.albums.search(type=metallum.AlbumTypes.FULL_LENGTH)

                            # log the number of albums listed for the band and the number of these albums owned
                            percent_owned = round((100 * len(self.get_albums_for_band(band))) / len(metallum_albums), 2)
                            sys.stdout.write(" [ALBUMS] {0}/{1} ({2}%)\n".format(
                                len(self.get_albums_for_band(band)),
                                len(metallum_albums),
                                percent_owned))

                            # finally search for new albums
                            for metallum_album in metallum_albums:
                                metallum_album_title = metallum_album.title
                                metallum_release_date = metallum_album.date.date()

                                # a new album's release is reported only if:
                                # - the album does not belong already to the collection
                                # - the release date (year) of the album is equal or greater to a given threshold
                                # - albums with release dates that are set in the future are excluded
                                if not self.is_album_in_collection(band, metallum_album_title) and \
                                        metallum_album.date.year >= args_threshold_year and not (
                                        metallum_release_date > datetime.date.today()):
                                    sys.stdout.write("[BAND] {0} \x1b[{1}m[NEW_ALBUM]\x1b[0m {2} ({3})\n".format(
                                        band, CSVData.green_ansi_code, metallum_album_title, metallum_release_date))
                                    new_releases.append([band, metallum_album_title, str(metallum_release_date)])

                    # rare condition:
                    # - there are several bands with the same name
                    # - the bands' name is found in the disambiguations list
                    # - the disambiguation id does not match any id in Encyclopaedia Metallum
                    # This can be due to a typo in the disambiguations list or to a change in Encyclopaedia Metallum
                    if len(bands) > 1 and band in self.disambiguations and not disambiguation_found:
                        sys.stdout.write("\x1b[{0}m [NO_DISAMBIGUATION_FOUND]\x1b[0m\n".format(CSVData.red_ansi_code))

            else:  # the band is not listed in Encyclopaedia Metallum
                sys.stdout.write("[BAND] {0} \x1b[{1}m[BAND_NOT_FOUND]\x1b[0m\n".format(band, CSVData.red_ansi_code))

        # write a json file with all the new releases
        if new_releases:
            with codecs.open("new_releases.json", 'w', encoding='utf-8') as new_releases_f:
                json_data = []
                for new_release in new_releases:
                    json_data.append({'band': new_release[0], 'album': new_release[1], 'release_date': new_release[2]})
                json.dump(json.loads(json.dumps(json_data)), new_releases_f, indent=2)


parser = argparse.ArgumentParser()

parser.add_argument(
    '-a',
    '--albumlist',
    help='The File (in JSON format) with the bands to check for new releases',
    required=True,
    type=str)
parser.add_argument(
    '-y',
    '--threshold_year',
    help='Starting from which year (included) should the new releases be searched for',
    required=True,
    type=int)
parser.add_argument(
    '-s',
    '--skip_bands',
    help='A file (in JSON format) with the bands to be skipped from the check',
    required=False,
    default=None,
    type=str)

parser.add_argument(
    '-d',
    '--disambiguations',
    help='A file (in JSON format) with disambiguation information in case of bands with the same name',
    required=False,
    default=None,
    type=str)

parser.add_argument(
    '-k',
    '--skip_splitup_bands',
    help='Skip bands, whose status is listed as "Split-up"',
    action='store_true',
    default=False)

args = parser.parse_args()
CSVData(args.albumlist, args.disambiguations, args.skip_bands).find_new_releases(
    args.threshold_year, args.skip_splitup_bands)
