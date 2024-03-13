from eyepy.drawing import Image, ImageResolution


def _CAM_OK(return_code: int) -> bool:
    """
    Default camera return code checking behaviour.
    """
    return return_code == 0

from eyepy.drawing import QQVGA, QVGA, VGA, CAM1MP, CAMHD, CAM5MP
_camera_resolution: ImageResolution = ImageResolution(0, 0)

from eye import CAMInit as _CAMInit
def CAMInit(resolution: ImageResolution) -> bool:
    """
    `CUSTOM` seems to be unsupported in sim.
    """
    resolution_code = resolution._code
    return_code = _CAMInit(resolution_code)
    
    if not _CAM_OK(return_code):
        return False
    
    global _camera_resolution
    _camera_resolution = resolution
    return True

from eye import CAMRelease as _CAMRelease
def CAMRelease() -> bool:
    return_code = _CAMRelease()
    return _CAM_OK(return_code)

from eye import CAMGet as _CAMGet
def CAMGet() -> Image:
    """
    Raises a `ValueError` if the resolution is not set (in testing, segfault-ed if not set).
    """
    if _camera_resolution.PIXELS == 0:
        raise ValueError("resolution not set")
    
    raw_image = _CAMGet()
    image = Image.from_c_bytes(raw_image, gray=False, resolution=_camera_resolution)
    return image

from eye import CAMGetGray as _CAMGetGray
def CAMGetGray() -> Image:
    """
    Raises a `ValueError` if the resolution is not set (in testing, segfault-ed if not set).
    """
    if _camera_resolution.PIXELS == 0:
        raise ValueError("resolution not set")
    
    raw_image = _CAMGetGray()
    image = Image.from_c_bytes(raw_image, gray=True, resolution=_camera_resolution)
    return image
