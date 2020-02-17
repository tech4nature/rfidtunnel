from app import usb
from unittest.mock import patch


@patch('app.usb.subprocess')
def test_check_for_mount(mock_subprocess):
    mock_subprocess.run.return_value = None
    usb.check_for_mount(0)
    assert not mock_subprocess.run.assert_called_with(['sudo', 'udisksctl', 'power-off', '-b', '/dev/sda'])

    usb.check_for_mount(1)
    assert not mock_subprocess.run.assert_called_with(['sudo', 'udisksctl', 'mount', '-b', '/dev/sda'])