import os
import unittest

from main import LOCAL_FRONTEND_ORIGINS, get_allowed_origins


class CorsConfigTests(unittest.TestCase):
    def test_local_origins_present_when_env_missing(self) -> None:
        original = os.environ.pop("FIELD_SHIFT_CORS_ORIGINS", None)
        try:
            self.assertEqual(get_allowed_origins(), LOCAL_FRONTEND_ORIGINS)
        finally:
            if original is not None:
                os.environ["FIELD_SHIFT_CORS_ORIGINS"] = original

    def test_env_origins_are_parsed_and_deduplicated(self) -> None:
        original = os.environ.get("FIELD_SHIFT_CORS_ORIGINS")
        os.environ["FIELD_SHIFT_CORS_ORIGINS"] = (
            " https://xo5u.github.io , https://xo5u.github.io ,https://field-shift.example.com "
        )
        try:
            self.assertEqual(
                get_allowed_origins(),
                [
                    "http://localhost:5173",
                    "http://127.0.0.1:5173",
                    "https://xo5u.github.io",
                    "https://field-shift.example.com",
                ],
            )
        finally:
            if original is None:
                os.environ.pop("FIELD_SHIFT_CORS_ORIGINS", None)
            else:
                os.environ["FIELD_SHIFT_CORS_ORIGINS"] = original


if __name__ == "__main__":
    unittest.main()
