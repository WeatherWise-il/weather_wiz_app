import geocoder


def get_geo_location():
    g = geocoder.ip(
        "me",
    )
    if g.ok:
        return g
    else:
        return None