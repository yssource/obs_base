from __future__ import print_function, division, absolute_import

from . import base

__all__ = ("TractUnit", "PatchUnit", "FilterUnit", "VisitUnit", "SensorUnit",
           "RawUnit", "MasterCalibrationUnit", "COMMON_UNITS")


class TractUnit(base.SpatialUnit):
    number = base.IntField()
    skymap = base.PythonTypeField()
    patches = base.ReverseForeignKey()
    key = base.Tuple(number, skymap)


class PatchUnit(base.SpatialUnit):
    tract = base.ForeignKey(TractUnit, reverse="patches")
    skymap = base.Alias(tract, TractUnit.skymap)
    x = base.IntField()
    y = base.IntField()
    key = base.Tuple(tract, x, y)


class FilterUnit(base.Unit):
    name = base.StrField()
    camera = base.PythonTypeField()
    visits = base.ReverseForeignKey()
    key = base.Tuple(name, camera)


class VisitUnit(base.SpatialUnit):
    number = base.IntField()
    filter = base.ForeignKey(FilterUnit, reverse="visits")
    camera = base.Alias(filter, FilterUnit.camera)
    sensors = base.ReverseForeignKey()
    dateobs = base.DateTimeField()
    key = base.Tuple(number, camera)


class SensorUnit(base.SpatialUnit):
    number = base.IntField()
    visit = base.ForeignKey(VisitUnit, reverse="sensors")
    camera = base.Alias(visit, VisitUnit.camera)
    filter = base.Alias(visit, VisitUnit.filter)
    dateobs = base.Alias(visit, VisitUnit.dateobs)
    raw = base.ReverseForeignKey()
    key = base.Tuple(visit, number)


class RawUnit(base.Unit):
    sensor = base.ForeignKey(SensorUnit, reverse="raw")
    visit = base.Alias(sensor, SensorUnit.visit)
    camera = base.Alias(sensor, SensorUnit.camera)
    filter = base.Alias(sensor, SensorUnit.filter)
    dateobs = base.Alias(sensor, SensorUnit.dateobs)
    name = base.StrField()
    key = base.Tuple(sensor, name)


class MasterCalibrationUnit(base.Unit):
    begin = base.DateTimeField()
    end = base.DateTimeField()
    filter = base.ForeignKey(FilterUnit, reverse=None, optional=True)
    camera = base.PythonTypeField()
    key = base.Tuple(begin, end, filter, camera)


COMMON_UNITS = (TractUnit, PatchUnit, FilterUnit, VisitUnit, SensorUnit,
                RawUnit, MasterCalibrationUnit)