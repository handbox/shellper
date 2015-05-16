from jsonschema import exceptions as exc
import testtools

import shellper.validation as validation


class TestValidation(testtools.TestCase):
    def test_validation_positive(self):
        json = [
            {
                'time': '18:00',
                'date': 'yesterday',
                'summary': 'How clone git repository?'
            }
        ]
        validation.validate(json)

    def test_validation_negative(self):
        json = [
            {
                'foo_time': '18:00',
                'foo_date': 'yesterday',
                'foo_summary': 'How clone git repository?'
            }
        ]
        with testtools.ExpectedException(exc.ValidationError):
            validation.validate(json)
