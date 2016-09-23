#!coding:utf-8
import codecs
import errno
import functools
import glob
import inspect
import os
import re
import sys
import warnings
import time
from collections import namedtuple
import ConfigParser

import cv2
import numpy

_debug_level = 2
_frame_number = 0
_config = None

cur_dir = os.getcwd()
main_dir = cur_dir[:cur_dir.find('CASE_LOG')-1]

class UITestError(Exception):
    """The test script had an unrecoverable error."""
    pass

class ConfigurationError(UITestError):
    pass

def _xdg_config_dir():
#     return os.environ.get('XDG_CONFIG_HOME', '%s/.config' % os.environ['HOME'])
    return os.path.dirname(main_dir)


def _config_init(force=False):
    global _config
    if force or not _config:
        config = ConfigParser.SafeConfigParser()
        config.readfp(
            open(os.path.join(main_dir, 'appConfig.cfg')))
        config.read([
            '%s/appConfig.cfg' % _xdg_config_dir(),
            # Config files specific to the test suite / test run:
            os.environ.get('STBT_CONFIG_FILE', ''),
        ])
        _config = config
    return _config

def get_config(section, key, default=None, type_=str):
    """Read the value of `key` from `section` of the IM config file.

    Raises `ConfigurationError` if the specified `section` or `key` is not
    found, unless `default` is specified (in which case `default` is returned).
    """

    config = _config_init()

    try:
        return type_(config.get(section, key))
    except ConfigParser.Error as e:
        if default is None:
            raise ConfigurationError(e.message)
        else:
            return default
    except ValueError:
        raise ConfigurationError("'%s.%s' invalid type (must be %s)" % (
            section, key, type_.__name__))

class MatchParameters(object):
    '''
    parse image match configure
    '''
    def __init__(self, match_method=None, match_threshold=None,
                 confirm_method=None, confirm_threshold=None,
                 erode_passes=None):
        if match_method is None:
            match_method = get_config('match', 'match_method')
        if match_threshold is None:
            match_threshold = get_config(
                'match', 'match_threshold', type_=float)
        if confirm_method is None:
            confirm_method = get_config('match', 'confirm_method')
        if confirm_threshold is None:
            confirm_threshold = get_config(
                'match', 'confirm_threshold', type_=float)
        if erode_passes is None:
            erode_passes = get_config('match', 'erode_passes', type_=int)

        if match_method not in (
                "sqdiff-normed", "ccorr-normed", "ccoeff-normed"):
            raise ValueError("Invalid match_method '%s'" % match_method)
        if confirm_method not in ("none", "absdiff", "normed-absdiff"):
            raise ValueError("Invalid confirm_method '%s'" % confirm_method)

        self.match_method = match_method
        self.match_threshold = match_threshold
        self.confirm_method = confirm_method
        self.confirm_threshold = confirm_threshold
        self.erode_passes = erode_passes

def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print 'Time consumed: %.3fs' % (end - start)
    return wrapper


def detect_match(src_image, image, noise_threshold=None, match_parameters=None):
    """Generator that yields a sequence of one `MatchResult` for each frame
    processed from the source video stream.

    `image` is the image used as the template during matching.  It can either
    be the filename of a png file on disk or a numpy array containing the
    actual template image pixel data in 8-bit BGR format.  8-bit BGR numpy
    arrays are the same format that OpenCV uses for images.  This allows
    generating templates on the fly (possibly using OpenCV) or searching for
    images captured from the system under test earlier in the test script.

    The templatematch parameter `noise_threshold` is marked for deprecation
    but appears in the args for backward compatibility with positional
    argument syntax. It will be removed in a future release; please use
    `match_parameters.confirm_threshold` intead.

    Specify `match_parameters` to customise the image matching algorithm. See
    the documentation for `MatchParameters` for details.
    """

    if match_parameters is None:
        match_parameters = MatchParameters()

    if noise_threshold is not None:
        warnings.warn(
            "noise_threshold is deprecated and will be removed in a future "
            "release of stb-tester. Please use "
            "match_parameters.confirm_threshold instead.",
            DeprecationWarning, stacklevel=2)
        match_parameters.confirm_threshold = noise_threshold

    if isinstance(image, numpy.ndarray):
        template = image
        template_name = _template_name(image)
    else:
        template_name = _find_path(image)
        if not os.path.isfile(template_name):
            raise UITestError("No such template file: %s" % image)
        template = cv2.imread(template_name, cv2.CV_LOAD_IMAGE_COLOR)
        if template is None:
            raise UITestError("Failed to load template file: %s" %
                              template_name)
    src = _find_path(src_image)
    if not os.path.isfile(src):
        raise UITestError("No such source image file: %s" % src_image)
    frame = cv2.imread(src, cv2.CV_LOAD_IMAGE_COLOR)
    if frame is None:
        raise UITestError("Failed to load template file: %s" %
                          template_name)
    
    matched, position, first_pass_certainty = _match(
        frame, template, match_parameters, template_name)

    result = MatchResult(
        time.time(), matched, position,
        first_pass_certainty, numpy.copy(frame),
        (image if isinstance(image, numpy.ndarray) else template_name))

    cv2.rectangle(
        frame,
        (position.x, position.y),
        (position.x + template.shape[1],
         position.y + template.shape[0]),
        (32, 0 if matched else 255, 255),  # bgr
        thickness=3)

    if matched:
        print "Match found: %s" % str(result)
        return True
    else:
        print "No match found. Closest match: %s" % str(result)
        return False
#     yield result

def _match(image, template, match_parameters, template_name):
    if any(image.shape[x] < template.shape[x] for x in (0, 1)):
        raise ValueError("Source image must be larger than template image")
    if any(template.shape[x] < 1 for x in (0, 1)):
        raise ValueError("Template image must contain some data")
    if template.shape[2] != 3:
        raise ValueError("Template image must be 3 channel BGR")
    if template.dtype != numpy.uint8:
        raise ValueError("Template image must be 8-bits per channel")

    first_pass_matched, position, first_pass_certainty = _find_match(
        image, template, match_parameters)
    matched = (
        first_pass_matched and
        _confirm_match(image, position, template, match_parameters))

    if _debug_level > 1:
        source_with_roi = image.copy()
        cv2.rectangle(
            source_with_roi,
            (position.x, position.y),
            (position.x + template.shape[1], position.y + template.shape[0]),
            (32, 0 if first_pass_matched else 255, 255),  # bgr
            thickness=1)
        _log_image(
            source_with_roi, "source_with_roi", "match-debug")
        _log_image_descriptions(
            template_name, matched, position,
            first_pass_matched, first_pass_certainty, match_parameters)

    return matched, position, first_pass_certainty

def _find_match(image, template, match_parameters):
    """Search for `template` in the entire `image`.

    This searches the entire image, so speed is more important than accuracy.
    False positives are ok; we apply a second pass (`_confirm_match`) to weed
    out false positives.

    http://docs.opencv.org/modules/imgproc/doc/object_detection.html
    http://opencv-code.com/tutorials/fast-template-matching-with-image-pyramid
    """

    log = functools.partial(_log_image, directory="match-debug")
    log(image, "source")
    log(template, "template")
    ddebug("Original image %s, template %s" % (image.shape, template.shape))

    levels = get_config("match", "pyramid_levels", type_=int)
    if levels <= 0:
        raise ConfigurationError("'match.pyramid_levels' must be > 0")
    template_pyramid = _build_pyramid(template, levels)
    image_pyramid = _build_pyramid(image, len(template_pyramid))
    roi_mask = None  # Initial region of interest: The whole image.

    for level in reversed(range(len(template_pyramid))):

        matched, best_match_position, certainty, roi_mask = _match_template(
            image_pyramid[level], template_pyramid[level], match_parameters,
            roi_mask, level)

        if level == 0 or not matched:
            return matched, _upsample(best_match_position, level), certainty

def _upsample(position, levels):
    """Convert position coordinates by the given number of pyramid levels.

    There is a loss of precision (unless ``levels`` is 0, in which case this
    function is a no-op).
    """
    return Position(position.x * 2 ** levels, position.y * 2 ** levels)

class Position(namedtuple('Position', 'x y')):
    """A point within the video frame.

    `x` and `y` are integer coordinates (measured in number of pixels) from the
    top left corner of the video frame.
    """
    pass

def _match_template(image, template, match_parameters, roi_mask, level):

    log = functools.partial(_log_image, directory="match-debug")
    log_prefix = "level%d-" % level
    ddebug("Level %d: image %s, template %s" % (
        level, image.shape, template.shape))

    method = {
        'sqdiff-normed': cv2.TM_SQDIFF_NORMED,
        'ccorr-normed': cv2.TM_CCORR_NORMED,
        'ccoeff-normed': cv2.TM_CCOEFF_NORMED,
    }[match_parameters.match_method]
    threshold = max(
        0,
        match_parameters.match_threshold - (0.2 if level > 0 else 0))

    matches_heatmap = (
        (numpy.ones if method == cv2.TM_SQDIFF_NORMED else numpy.zeros)(
            (image.shape[0] - template.shape[0] + 1,
             image.shape[1] - template.shape[1] + 1),
            dtype=numpy.float32))

    if roi_mask is None or any(x < 3 for x in roi_mask.shape):
        rois = [  # Initial region of interest: The whole image.
            _Rect(0, 0, matches_heatmap.shape[1], matches_heatmap.shape[0])]
    else:
        roi_mask = cv2.pyrUp(roi_mask)
        log(roi_mask, log_prefix + "roi_mask")
        contours, _ = cv2.findContours(
            roi_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        rois = [
            _Rect(*cv2.boundingRect(x))
            # findContours ignores 1-pixel border of the image
            .shift(Position(-1, -1)).expand(_Size(2, 2))
            for x in contours]

    if _debug_level > 1:
        source_with_rois = image.copy()
        for roi in rois:
            r = roi
            t = _Size(*template.shape[:2])
            s = _Size(*source_with_rois.shape[:2])
            cv2.rectangle(
                source_with_rois,
                (max(0, r.x), max(0, r.y)),
                (min(s.w - 1, r.x + r.w + t.w - 1),
                 min(s.h - 1, r.y + r.h + t.h - 1)),
                (0, 255, 255),
                thickness=1)
        log(source_with_rois, log_prefix + "source_with_rois")

    for roi in rois:
        r = roi.expand(_Size(*template.shape[:2])).shrink(_Size(1, 1))
        ddebug("Level %d: Searching in %s" % (level, roi))
        cv2.matchTemplate(
            image[r.to_slice()],
            template,
            method,
            matches_heatmap[roi.to_slice()])

    log(image, log_prefix + "source")
    log(template, log_prefix + "template")
    log(matches_heatmap, log_prefix + "source_matchtemplate")

    min_value, max_value, min_location, max_location = cv2.minMaxLoc(
        matches_heatmap)
    if method == cv2.TM_SQDIFF_NORMED:
        certainty = (1 - min_value)
        best_match_position = Position(*min_location)
    elif method in (cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED):
        certainty = max_value
        best_match_position = Position(*max_location)
    else:
        assert False, (
            "Invalid matchTemplate method '%s'" % method)

    _, new_roi_mask = cv2.threshold(
        matches_heatmap,
        ((1 - threshold) if method == cv2.TM_SQDIFF_NORMED else threshold),
        255,
        (cv2.THRESH_BINARY_INV if method == cv2.TM_SQDIFF_NORMED
         else cv2.THRESH_BINARY))
    new_roi_mask = new_roi_mask.astype(numpy.uint8)
    log(new_roi_mask, log_prefix + "source_matchtemplate_threshold")

    matched = certainty >= threshold
    ddebug("Level %d: %s at %s with certainty %s" % (
        level, "Matched" if matched else "Didn't match",
        best_match_position, certainty))
    return (matched, best_match_position, certainty, new_roi_mask)

class _Size(namedtuple("_Size", "h w")):
    pass

class _Rect(namedtuple("_Rect", "x y w h")):
    def expand(self, size):
        return _Rect(self.x, self.y, self.w + size.w, self.h + size.h)

    def shrink(self, size):
        return _Rect(self.x, self.y, self.w - size.w, self.h - size.h)

    def shift(self, position):
        return _Rect(self.x + position.x, self.y + position.y, self.w, self.h)

    def to_slice(self):
        """Return a 2-dimensional slice suitable for indexing a numpy array."""
        return (slice(self.y, self.y + self.h), slice(self.x, self.x + self.w))
       
def _build_pyramid(image, levels):
    """A "pyramid" is [an image, the same image at 1/2 the size, at 1/4, ...]

    As a performance optimisation, image processing algorithms work on a
    "pyramid" by first identifying regions of interest (ROIs) in the smallest
    image; if results are positive, they proceed to the next larger image, etc.
    See http://docs.opencv.org/doc/tutorials/imgproc/pyramids/pyramids.html

    The original-sized image is called "level 0", the next smaller image "level
    1", and so on. This numbering corresponds to the array index of the
    "pyramid" array.
    """
    pyramid = [image]
    for _ in range(levels - 1):
        if any(x < 20 for x in pyramid[-1].shape[:2]):
            break
        pyramid.append(cv2.pyrDown(pyramid[-1]))
    return pyramid
       
def _confirm_match(image, position, template, match_parameters):
    """Confirm that `template` matches `image` at `position`.

    This only checks `template` at a single position within `image`, so we can
    afford to do more computationally-intensive checks than `_find_match`.
    """

    if match_parameters.confirm_method == "none":
        return True

    log = functools.partial(_log_image, directory="match-debug")

    # Set Region Of Interest to the "best match" location
    roi = image[
        position.y:(position.y + template.shape[0]),
        position.x:(position.x + template.shape[1])]
    image_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    log(roi, "confirm-source_roi")
    log(image_gray, "confirm-source_roi_gray")
    log(template_gray, "confirm-template_gray")

    if match_parameters.confirm_method == "normed-absdiff":
        cv2.normalize(image_gray, image_gray, 0, 255, cv2.NORM_MINMAX)
        cv2.normalize(template_gray, template_gray, 0, 255, cv2.NORM_MINMAX)
        log(image_gray, "confirm-source_roi_gray_normalized")
        log(template_gray, "confirm-template_gray_normalized")

    absdiff = cv2.absdiff(image_gray, template_gray)
    _, thresholded = cv2.threshold(
        absdiff, int(match_parameters.confirm_threshold * 255),
        255, cv2.THRESH_BINARY)
    eroded = cv2.erode(
        thresholded,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
        iterations=match_parameters.erode_passes)
    log(absdiff, "confirm-absdiff")
    log(thresholded, "confirm-absdiff_threshold")
    log(eroded, "confirm-absdiff_threshold_erode")

    return cv2.countNonZero(eroded) == 0


def _log_image(image, name, directory):
    if _debug_level <= 1:
        return
    global _frame_number
    d = directory
    if name == "source":
        _frame_number += 1
#     d = os.path.join(directory, "%05d" % _frame_number)
#         d = directory
    if not _mkdir(d):
        warn("Failed to create directory '%s'; won't save debug images." % d)
        return
    if image.dtype == numpy.float32:
        image = cv2.convertScaleAbs(image, alpha=255)
    cv2.imwrite(os.path.join(d, name) + ".png", image)

def _mkdir(d):
    try:
        os.makedirs(d)
    except OSError, e:
        if e.errno != errno.EEXIST:
            return False
    return os.path.isdir(d) and os.access(d, os.R_OK | os.W_OK)
   
def _template_name(template):
    if isinstance(template, numpy.ndarray):
        return "<Custom Image>"
    elif isinstance(template, str) or isinstance(template, unicode):
        return template
    else:
        assert False, ("template is of unexpected type '%s'" %
                       type(template).__name__)
        
        
def _find_path(image):
    """Searches for the given filename and returns the full path.

    Searches in the directory of the script that called (for example)
    detect_match, then in the directory of that script's caller, etc.
    """

    if os.path.isabs(image):
        return image

    # stack()[0] is _find_path;
    # stack()[1] is _find_path's caller, e.g. detect_match;
    # stack()[2] is detect_match's caller (the user script).
    for caller in inspect.stack()[2:]:
        caller_image = os.path.join(
            os.path.dirname(inspect.getframeinfo(caller[0]).filename),
            image)
        if os.path.isfile(caller_image):
            return os.path.abspath(caller_image)

    # Fall back to image from cwd, for convenience of the selftests
    return os.path.abspath(image)


class MatchResult(object):
    """
    * `timestamp`: Video stream timestamp.
    * `match`: Boolean result.
    * `position`: `Position` of the match.
    * `first_pass_result`: Value between 0 (poor) and 1.0 (excellent match)
      from the first pass of the two-pass templatematch algorithm.
    * `frame`: The video frame that was searched, in OpenCV format.
    * `image`: The template image that was searched for, as given to
      `wait_for_match` or `detect_match`.
    """

    def __init__(
            self, timestamp, match, position, first_pass_result, frame=None,
            image=None):
        self.timestamp = timestamp
        self.match = match
        self.position = position
        self.first_pass_result = first_pass_result
        if frame is None:
            warnings.warn(
                "Creating a 'MatchResult' without specifying 'frame' is "
                "deprecated. In a future release of stb-tester the 'frame' "
                "parameter will be mandatory.",
                DeprecationWarning, stacklevel=2)
        self.frame = frame
        if image is None:
            warnings.warn(
                "Creating a 'MatchResult' without specifying 'image' is "
                "deprecated. In a future release of stb-tester the 'image' "
                "parameter will be mandatory.",
                DeprecationWarning, stacklevel=2)
            image = ""
        self.image = image

    def __str__(self):
        return (
            "MatchResult(timestamp=%s, match=%s, position=%s, "
            "first_pass_result=%s, frame=%s, image=%s)" % (
                self.timestamp,
                self.match,
                self.position,
                self.first_pass_result,
                "None" if self.frame is None else "%dx%dx%d" % (
                    self.frame.shape[1], self.frame.shape[0],
                    self.frame.shape[2]),
                _template_name(self.image)))

        
_debugstream = codecs.getwriter('utf-8')(sys.stderr)

def warn(s):
    _debugstream.write("%s: warning: %s\n" % (
        os.path.basename(sys.argv[0]), str(s)))


def debug(msg):
    """Print the given string to stderr if IM run `--verbose` was given."""
    if _debug_level > 0:
        _debugstream.write(
            "%s: %s\n" % (os.path.basename(sys.argv[0]), str(msg)))
        
def _log_image_descriptions(
        template_name, matched, position,
        first_pass_matched, first_pass_certainty, match_parameters):
    """Create html file that describes the debug images."""

    try:
        import jinja2
    except ImportError:
        warn(
            "Not generating html guide to the image-processing debug images, "
            "because python 'jinja2' module is not installed.")
        return

#     d = os.path.join("match-debug/detect_match", "%05d" % _frame_number)
    d = 'match-debug'
    template = jinja2.Template("""
        <!DOCTYPE html>
        <html lang='en'>
        <head>
        <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css" rel="stylesheet">
        <style>
            img {
                vertical-align: middle; max-width: 300px; max-height: 36px;
                padding: 1px; border: 1px solid #ccc; }
            p, li { line-height: 40px; }
        </style>
        </head>
        <body>
        <div class="container">
        <h4>
            <i>{{template_name}}</i>
            {{"matched" if matched else "didn't match"}}
        </h4>

        <p>Searching for <b>template</b> {{link("template")}}
            within <b>source</b> {{link("source")}} image.

        {% for level in levels %}

            <p>At level <b>{{level}}</b>:
            <ul>
                <li>Searching for <b>template</b> {{link("template", level)}}
                    within <b>source regions of interest</b>
                    {{link("source_with_rois", level)}}.
                <li>OpenCV <b>matchTemplate result</b>
                    {{link("source_matchtemplate", level)}}
                    with method {{match_parameters.match_method}}
                    ({{"darkest" if match_parameters.match_method ==
                            "sqdiff-normed" else "lightest"}}
                    pixel indicates position of best match).
                <li>matchTemplate result <b>above match_threshold</b>
                    {{link("source_matchtemplate_threshold", level)}}
                    of {{"%g"|format(match_parameters.match_threshold)}}
                    (white pixels indicate positions above the threshold).

            {% if (level == 0 and first_pass_matched) or level != min(levels) %}
                <li>Matched at {{position}} {{link("source_with_roi")}}
                    with certainty {{"%.4f"|format(first_pass_certainty)}}.
            {% else %}
                <li>Didn't match (best match at {{position}}
                    {{link("source_with_roi")}}
                    with certainty {{"%.4f"|format(first_pass_certainty)}}).
            {% endif %}

            </ul>

        {% endfor %}

        {% if first_pass_certainty >= match_parameters.match_threshold %}
            <p><b>Second pass (confirmation):</b>
            <ul>
                <li>Comparing <b>template</b> {{link("confirm-template_gray")}}
                    against <b>source image's region of interest</b>
                    {{link("confirm-source_roi_gray")}}.

            {% if match_parameters.confirm_method == "normed-absdiff" %}
                <li>Normalised <b>template</b>
                    {{link("confirm-template_gray_normalized")}}
                    and <b>source</b>
                    {{link("confirm-source_roi_gray_normalized")}}.
            {% endif %}

                <li><b>Absolute differences</b> {{link("confirm-absdiff")}}.
                <li>Differences <b>above confirm_threshold</b>
                    {{link("confirm-absdiff_threshold")}}
                    of {{"%.2f"|format(match_parameters.confirm_threshold)}}.
                <li>After <b>eroding</b>
                    {{link("confirm-absdiff_threshold_erode")}}
                    {{match_parameters.erode_passes}}
                    {{"time" if match_parameters.erode_passes == 1
                        else "times"}}.
                    {{"No" if matched else "Some"}}
                    differences (white pixels) remain, so the template
                    {{"does" if matched else "doesn't"}} match.
            </ul>
        {% endif %}

        </div>
        </body>
        </html>
    """)

    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(template.render(
            first_pass_certainty=first_pass_certainty,
            first_pass_matched=first_pass_matched,
            levels=list(reversed(sorted(set(
                [int(re.search(r"level(\d+)-.*", x).group(1))
                 for x in glob.glob(os.path.join(d, "level*"))])))),
            link=lambda s, level=None: (
                "<a href='{0}{1}.png'><img src='{0}{1}.png'></a>"
                .format("" if level is None else "level%d-" % level, s)),
            match_parameters=match_parameters,
            matched=matched,
            min=min,
            position=position,
            template_name=template_name,
        ))

def ddebug(s):
    """Extra verbose debug for IM developers, not end users"""
    if _debug_level > 1:
        _debugstream.write("%s: %s\n" % (os.path.basename(sys.argv[0]), str(s)))
        

if __name__ == '__main__':
    
    template_dir = os.path.join(main_dir, 'caseInfo', 'Case_pic')
    for name in os.listdir(cur_dir):
        if os.path.isdir(name) and not name.startswith('match'):
            template = os.path.join(template_dir, name)
    img_dir = os.path.join(cur_dir, os.path.basename(template))
    images = [os.path.join(img_dir,f) for f in os.listdir(img_dir)]
    
    detect_match(images[0], template)