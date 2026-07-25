from mcpserver.permissions import OwnSpaceWritable


def test_own_space_writable():
    perms = OwnSpaceWritable()
    assert perms.can_write("nikinger", "nikinger") is True


def test_foreign_space_read_only():
    perms = OwnSpaceWritable()
    assert perms.can_read("nikinger", "kollege") is True
    assert perms.can_write("nikinger", "kollege") is False


def test_visible_spaces_filters_by_can_read():
    perms = OwnSpaceWritable()
    assert perms.visible_spaces("nikinger", ["nikinger", "kollege"]) == ["nikinger", "kollege"]
