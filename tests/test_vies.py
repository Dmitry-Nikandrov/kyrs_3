from datetime import datetime
from unittest.mock import patch

from src.views import main


@patch("src.utils.datetime")
def test_main(mock_datetime):
    mock_datetime.now.return_value = datetime(2024, 12, 10, 9, 20, 55)

    assert main("None") == []


if __name__ == "__main__":
    print("Завершено успешно")
