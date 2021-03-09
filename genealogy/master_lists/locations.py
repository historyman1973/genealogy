def location_formats(type, address="", parish="", townorcity="", county="", country=""):

    if type == "long":
        long_location = ""
        if address:
            long_location += address

        if parish:
            if address:
                long_location += ", " + parish
            else:
                long_location += parish

        if townorcity:
            if address or parish:
                long_location += ", " + townorcity
            else:
                long_location += townorcity

        if county:
            if address or parish or townorcity:
                long_location += ", " + county
            else:
                long_location += county

        if country:
            if address or parish or townorcity or county:
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
