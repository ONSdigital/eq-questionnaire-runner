import pytest

from app.authentication.user_id_generator import UserIDGenerator

ITERATIONS = 1000


def test_generate_id():
    id_generator = UserIDGenerator(ITERATIONS, "", "")
    user_id_1 = id_generator.generate_id("1234567890123456")
    user_id_2 = id_generator.generate_id("1234567890123456")
    user_id_3 = id_generator.generate_id("0000000000000000")

    assert user_id_1 == user_id_2
    assert user_id_1 != user_id_3


def test_different_salt_creates_different_user_id():
    id_generator_1 = UserIDGenerator(ITERATIONS, "", "")
    user_id_1 = id_generator_1.generate_id("1234567890123456")

    id_generator_2 = UserIDGenerator(ITERATIONS, "random", "")
    user_id_2 = id_generator_2.generate_id("1234567890123456")

    assert user_id_1 != user_id_2


def test_generate_ik():
    id_generator = UserIDGenerator(ITERATIONS, "", "")
    user_ik_1 = id_generator.generate_ik("1234567890123456")
    user_ik_2 = id_generator.generate_ik("1234567890123456")
    user_ik_3 = id_generator.generate_ik("1111111111111111")

    assert user_ik_1 == user_ik_2
    assert user_ik_1 != user_ik_3


def test_different_salt_creates_different_user_ik():
    id_generator_1 = UserIDGenerator(ITERATIONS, "", "")
    user_ik_1 = id_generator_1.generate_ik("1234567890123456")

    id_generator_2 = UserIDGenerator(ITERATIONS, "", "random")
    user_ik_2 = id_generator_2.generate_ik("1234567890123456")

    assert user_ik_1 != user_ik_2


def test_create_generator_no_user_id_salt_raises_error():
    with pytest.raises(ValueError):
        UserIDGenerator(1000, None, "")


def test_create_generator_no_user_ik_salt_raises_error():
    with pytest.raises(ValueError):
        UserIDGenerator(1000, "", None)
