# Imports =====================================================================
from chardet.universaldetector import UniversalDetector
# =============================================================================


def guess_codec(filepath):

    detector = UniversalDetector()

    with open(filepath, 'rb') as f:

        for line in f:

            detector.feed(line)

        detector.close()

        codec = detector.result['encoding']

    return codec
