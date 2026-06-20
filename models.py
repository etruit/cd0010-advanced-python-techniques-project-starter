"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.
"""
import math

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown), and whether it's
    marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, pdes, name=None, diameter=float('nan'),
                 hazardous=False):
        """Create a new `NearEarthObject`.

        :param pdes: The primary designation of the NEO.
        :param name: The IAU name of the NEO.
        :param diameter: The diameter of the NEO in kilometers.
        :param hazardous: A flag indicating if the NEO is potentially
        hazardous.
        """
        self.designation = str(pdes)
        self.name = str(name) if name else None
        try:
            diameter = float(diameter)
        except (TypeError, ValueError):
            diameter = float('nan')
        self.diameter = float('nan') if math.isnan(diameter) else diameter
        self.hazardous = bool(hazardous)

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return (
            f"{self.designation} ({self.name})"
            if self.name
            else self.designation
        )

    def __str__(self):
        """Return `str(self)`."""
        return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} " \
               f"km and is " \
               f"{'potentially hazardous'
                  if self.hazardous else 'not potentially hazardous'}."

    def __repr__(self):
        """Return a machine-readable representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, " \
               f"name={self.name!r}, diameter={self.diameter:.3f}, " \
               f"hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach
    to Earth, such as the date and time (in UTC) of closest approach, the
    nominal approach distance in astronomical units, and the relative approach
    velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, des, cd, dist, v_rel):
        """Create a new `CloseApproach`.

        :param des: The primary designation of the NEO making the close
        approach.
        :param cd: The close approach date and time (in UTC).
        :param dist: The nominal approach distance in astronomical units.
        :param v_rel: The relative approach velocity in kilometers per second.
        """
        self._designation = des
        self.time = cd_to_datetime(cd)
        self.distance = float(dist)
        self.velocity = float(v_rel)

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this close approach's time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default
        representation includes seconds - significant figures that don't
        exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return f"At {self.time_str}, '{self._designation}' approaches Earth " \
               f"at a distance of {self.distance:.2f} au and a velocity " \
               f"of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return a machine-readable representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, " \
               f"distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
