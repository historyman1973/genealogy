from genealogy import db
from ..models import Location
from flask import session


def location_formats(type, address="", parish="", district = "", townorcity="", county="", country=""):

    if type == "long":
        long_location = ""
        if address:
            long_location += address

        if parish:
            if address:
                long_location += ", " + parish
            else:
                long_location += parish

        if district:
            if address or parish:
                long_location += ", " + district
            else:
                long_location += district

        if townorcity:
            if address or parish or district:
                long_location += ", " + townorcity.upper()
            else:
                long_location += townorcity.upper()

        if county:
            if address or parish or district or townorcity:
                long_location += ", " + county
            else:
                long_location += county

        if country:
            if address or parish or district or townorcity or county:
                long_location += ", " + country
            else:
                long_location += country

        return long_location

    elif type == "short":
        short_location = ""

        if parish:
            short_location += parish

        if townorcity:
            if parish:
                short_location += ", " + townorcity
            else:
                short_location += townorcity

        if county:
            if parish or townorcity:
                short_location += ", " + county
            else:
                short_location += county

        return short_location


def add_location(form):
    address = form.location_address.data
    parish = form.location_parish.data
    district = form.location_district.data
    townorcity = form.location_townorcity.data
    county = form.location_county.data
    country = form.location_country.data
    full_location = location_formats("long", address=address, parish=parish, district=district, townorcity=townorcity,
                                     county=county, country=country)
    short_location = location_formats("short", parish=parish, townorcity=townorcity, county=county)

    new_location = Location(address=address, parish=parish, district=district, townorcity=townorcity,
                            county=county, country=country, full_location=full_location,
                            short_location=short_location)

    db.session.add(new_location)
    db.session.commit()
    db.session.flush()

    session["new_location_id"] = new_location.id

    return
