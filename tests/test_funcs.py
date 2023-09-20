import pytest
from backend.core.validators import (
    OneOfTwoValidator,
    MinLenValidator,
    hex_color_validator
)
from django.core.exceptions import ValidationError


correct_words = ('Петя', 'Semen')
invalid_words = ('Петяmen', 'Петя 3', 'Se.men')
too_short_words = ('', '3', '33')


@pytest.mark.validators
@pytest.mark.parametrize('word', correct_words)
def test_one_of_two_correct(word):
    assert OneOfTwoValidator()(word) is None


@pytest.mark.validators
@pytest.mark.parametrize('word', invalid_words)
def test_one_of_two_invalid(word):
    pytest.raises(ValidationError, OneOfTwoValidator(), word)


@pytest.mark.validators
@pytest.mark.parametrize('word', correct_words)
def test_min_len_correct(word):
    assert MinLenValidator(3)(word) is None


@pytest.mark.validators
@pytest.mark.parametrize('word', too_short_words)
def test_min_len_invalid(word):
    pytest.raises(ValidationError, MinLenValidator(3), word)


@pytest.mark.validators
def test_color_correct():
    assert hex_color_validator('323') == '#332233'
    assert hex_color_validator('cBa') == '#CCBBAA'
    assert hex_color_validator('0a2B3c') == '#0A2B3C'


invalid_colors = ('3', '33', '3653', '7654321', 'bb', '44d', '33d33ff')


@pytest.mark.validators
@pytest.mark.parametrize('color', invalid_colors)
def test_color_invalid(color):
    pytest.raises(ValidationError, hex_color_validator, color)
