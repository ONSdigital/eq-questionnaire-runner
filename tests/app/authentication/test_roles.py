import pytest
from werkzeug.exceptions import Forbidden

from app.authentication.roles import role_required
from tests.app.questionnaire.conftest import get_metadata


def test_role_required_unauthenticated_no_metadata(
    mock_get_metadata, mock_current_user
):
    # Given I am not authenticated and have no metadata
    mock_current_user.is_authenticated = False
    mock_get_metadata.return_value = None

    # And I have decorated a function with role_required
    wrapper = role_required("dumper")
    wrapped_func = wrapper(lambda: "not called")

    # When I call the decorated function
    # Then a Forbidden exception is raised
    with pytest.raises(Forbidden):
        wrapped_func()


def test_role_required_authenticated_no_metadata(mock_get_metadata, mock_current_user):
    # Given I am authenticated but have no metadata
    mock_current_user.is_authenticated = True
    mock_get_metadata.return_value = None

    # And I have decorated a function with role_required
    wrapper = role_required("dumper")
    wrapped_func = wrapper(lambda: "not called")

    # When I call the decorated function
    # Then a Forbidden exception is raised
    with pytest.raises(Forbidden):
        wrapped_func()


def test_role_required_authenticated_with_empty_metadata(
    mock_get_metadata, mock_current_user
):
    # Given I am authenticated but my metadata is empty
    mock_current_user.is_authenticated = True
    mock_get_metadata.return_value = {}

    # And I have decorated a function with role_required
    wrapper = role_required("dumper")
    wrapped_func = wrapper(lambda: "not called")

    # When I call the decorated function
    # Then a Forbidden exception is raised
    with pytest.raises(Forbidden):
        wrapped_func()


def test_role_required_authenticated_with_metadata_none_roles(
    mock_get_metadata, mock_current_user
):
    # Given I am authenticated but my metadata contains a
    # roles list set to None
    mock_current_user.is_authenticated = True
    mock_get_metadata.return_value = get_metadata(extra_metadata={"roles": None})

    # And I have decorated a function with role_required
    wrapper = role_required("dumper")
    wrapped_func = wrapper(lambda: "not called")

    # When I call the decorated function
    # Then a Forbidden exception is raised
    with pytest.raises(Forbidden):
        wrapped_func()


def test_role_required_authenticated_with_metadata_empty_roles(
    mock_get_metadata, mock_current_user
):
    # Given I am authenticated and my metadata contains an empty
    # roles list
    mock_current_user.is_authenticated = True
    mock_get_metadata.return_value = get_metadata(extra_metadata={"roles": []})

    # And I have decorated a function with role_required
    wrapper = role_required("dumper")
    wrapped_func = wrapper(lambda: "not called")

    # When I call the decorated function
    # Then a Forbidden exception is raised
    with pytest.raises(Forbidden):
        wrapped_func()


def test_role_required_authenticated_with_metadata_wrong_role(
    mock_get_metadata, mock_current_user
):
    # Given I am authenticated and my metadata contains a single role.
    mock_current_user.is_authenticated = True
    mock_get_metadata.return_value = get_metadata(extra_metadata={"roles": ["flusher"]})

    # And I have decorated a function with role_required, specifying a
    # role that isn't in the metadata roles list.
    wrapper = role_required("dumper")
    wrapped_func = wrapper(lambda: "not called")

    # When I call the decorated function
    # Then a Forbidden exception is raised
    with pytest.raises(Forbidden):
        wrapped_func()


def test_role_required_authenticated_with_metadata_matching_role(
    mock_get_metadata, mock_current_user
):
    # Given I am authenticated and my metadata contains a single role.
    mock_current_user.is_authenticated = True
    mock_get_metadata.return_value = get_metadata(extra_metadata={"roles": ["dumper"]})

    # And I have decorated a function with role_required, specifying a
    # role that is listed in the metadata roles list.
    wrapper = role_required("dumper")
    wrapped_func = wrapper(lambda: "single was called")

    # When I call the decorated function
    # Then the function is executed and returns a value
    assert wrapped_func() == "single was called"


def test_role_required_authenticated_with_metadata_matching_multiple_role(
    mock_get_metadata, mock_current_user
):
    # Given I am authenticated but my metadata contains multiples roles
    mock_current_user.is_authenticated = True
    mock_get_metadata.return_value = get_metadata(
        extra_metadata={"roles": ["flusher", "other", "dumper"]}
    )

    # And I have decorated a function with role_required, specifying a
    # role that is listed in the metadata roles list.
    wrapper = role_required("other")
    wrapped_func = wrapper(lambda: "other was called")

    # When I call the decorated function
    # Then the function is executed and returns a value
    assert wrapped_func() == "other was called"


def test_role_required_wrapped_with_positional_arguments(
    mock_get_metadata, mock_current_user
):
    # Given I am authenticated and my metadata contains roles
    mock_current_user.is_authenticated = True
    mock_get_metadata.return_value = get_metadata(
        extra_metadata={"roles": ["flusher", "other", "dumper"]}
    )

    # And I have decorated a function that takes multiple positional arguments
    # with role_required, specifying a role that is listed in the metadata
    # roles list.
    wrapper = role_required("other")
    wrapped_func = wrapper(lambda arg1, arg2, arg3: [arg1, arg2, arg3])

    # When I call the decorated function with arguments
    # Then the function is executed and returns the arguments supplied
    assert wrapped_func(1, 2, 3) == [1, 2, 3]


def test_role_required_wrapped_with_keyword_arguments(
    mock_get_metadata, mock_current_user
):
    # Given I am authenticated and my metadata contains roles
    mock_current_user.is_authenticated = True
    mock_get_metadata.return_value = get_metadata(
        extra_metadata={"roles": ["flusher", "other", "dumper"]}
    )

    # And I have decorated a function that takes multiple positional arguments
    # with role_required, specifying a role that is listed in the metadata
    # roles list.
    wrapper = role_required("other")
    wrapped_func = wrapper(lambda arg1=None, arg2=None: [arg1, arg2])

    # When I call the decorated function with arguments
    # Then the function is executed and returns the arguments supplied
    assert wrapped_func(arg1="y", arg2="z") == ["y", "z"]


def test_role_required_wrapped_with_positional_and_keyword_arguments(
    mock_get_metadata, mock_current_user
):
    # Given I am authenticated and my metadata contains roles
    mock_current_user.is_authenticated = True
    mock_get_metadata.return_value = get_metadata(
        extra_metadata={"roles": ["flusher", "other", "dumper"]}
    )

    # And I have decorated a function that takes multiple positional arguments
    # with role_required, specifying a role that is listed in the metadata
    # roles list.
    wrapper = role_required("other")
    wrapped_func = wrapper(lambda arg1, arg2=None: [arg1, arg2])

    # When I call the decorated function with both positional and keyword arguments
    # Then the function is executed and returns the arguments supplied
    assert wrapped_func("i", arg2=2) == ["i", 2]


def test_role_required_unauthenticated_wrapped_with_arguments(
    mock_get_metadata, mock_current_user
):
    # Given I am not authenticated
    mock_current_user.is_authenticated = False
    mock_get_metadata.return_value = {}

    # And I have decorated a function that takes multiple arguments
    wrapper = role_required("other")
    wrapped_func = wrapper(lambda arg1, arg2, arg3: [arg1, arg2, arg3])

    # When I call the decorated function with arguments
    # Then a Forbidden exception is raised
    with pytest.raises(Forbidden):
        wrapped_func("a", "b", "c")


def test_role_required_unauthenticated_wrapped_with_keyword_arguments(
    mock_get_metadata, mock_current_user
):
    # Given I am not authenticated
    mock_current_user.is_authenticated = False
    mock_get_metadata.return_value = get_metadata(
        extra_metadata={"roles": ["flusher", "other", "dumper"]}
    )

    # And I have decorated a function that takes multiple positional arguments
    # with role_required, specifying a role that is listed in the metadata
    # roles list.
    wrapper = role_required("other")
    wrapped_func = wrapper(lambda arg1=None, arg2=None: [arg1, arg2])

    # When I call the decorated function with keyword arguments
    # Then a Forbidden exception is raised
    with pytest.raises(Forbidden):
        wrapped_func(arg1="y", arg2="z")


def test_role_required_unauthenticated_wrapped_with_positional_and_keyword_arguments(
    mock_get_metadata, mock_current_user
):
    # Given I am not authenticated
    mock_current_user.is_authenticated = False
    mock_get_metadata.return_value = get_metadata(
        extra_metadata={"roles": ["flusher", "other", "dumper"]}
    )

    # And I have decorated a function that takes multiple positional arguments
    # with role_required, specifying a role that is listed in the metadata
    # roles list.
    wrapper = role_required("other")
    wrapped_func = wrapper(lambda arg1, arg2=None: [arg1, arg2])

    # When I call the decorated function with keyword arguments
    # Then a Forbidden exception is raised
    with pytest.raises(Forbidden):
        wrapped_func("p", arg2=9)
