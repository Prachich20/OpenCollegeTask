from utilities import Common


def test_result():
    data = Common().flickr(latitude=0, longitude=0, page=1)
    assert (data["pages"] > 0)


def test_invalid_latitude():
    data = Common().flickr(latitude=-1000, longitude=0, page=1)
    assert (data == "Not a valid latitude")


def test_invalid_longitude():
    data = Common().flickr(latitude=0, longitude=-1000, page=1)
    assert (data == "Not a valid longitude")
