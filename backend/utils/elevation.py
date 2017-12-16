from enum import Enum


class Elevation(Enum):
    """Enum class to restrict elevation_type values"""
    uphills = 'UPHILLS'
    downhills = 'DOWNHILLS'
    minimize = 'MINIMIZE'

