from attack_info_manager import AttackInfoManager


def assert_list_lengths(a, length):
    assert len(a.get_lons()) == length
    assert len(a.get_lats()) == length
    assert len(a.get_colors()) == length
    assert len(a.get_sizes()) == length


def test_new_instance():
    a = AttackInfoManager(5, 500, 50)
    assert_list_lengths(a, 5)


def test_one_update():
    a = AttackInfoManager(5, 500, 50)
    # list(*) to create a copy not a reference
    lons = list(a.get_lons())
    lats = list(a.get_lats())
    colors = list(a.get_colors())
    sizes = list(a.get_sizes())
    a.update()
    assert_list_lengths(a, 10)
    assert lons == a.get_lons()[:5]
    assert lats == a.get_lats()[:5]
    assert colors == a.get_colors()[:5]

    for index in range(5):
        assert sizes[index] == a.get_sizes()[index] + 50


def test_nine_updates():
    a = AttackInfoManager(5, 500, 50)
    # list(*) to create a copy not a reference
    lons = list(a.get_lons())
    lats = list(a.get_lats())
    colors = list(a.get_colors())
    sizes = list(a.get_sizes())
    for count in range(9):
        a.update()
    assert_list_lengths(a, 50)
    assert lons == a.get_lons()[:5]
    assert lats == a.get_lats()[:5]
    assert colors == a.get_colors()[:5]

    for index in range(5):
        assert a.get_sizes()[index] == 50


def test_ten_updates():
    a = AttackInfoManager(5, 500, 50)
    # list(*) to create a copy not a reference
    lons = list(a.get_lons())
    lats = list(a.get_lats())
    colors = list(a.get_colors())
    sizes = list(a.get_sizes())
    for count in range(10):
        a.update()
    assert_list_lengths(a, 50)
    assert lons != a.get_lons()[:5]
    assert lats != a.get_lats()[:5]
    # colors may match depending on protocols
    #assert colors != a.get_colors()[:5]

    for index in range(5):
        assert a.get_sizes()[index] == 50


def test_100_updates():
    a = AttackInfoManager(5, 500, 50)

    for count in range(10):
        a.update()

    for count in range(90):
        assert_list_lengths(a, 50)