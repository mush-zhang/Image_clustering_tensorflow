import CAM2CameraDatabaseAPIClient as cam2
from CAM2ImageArchiver.CAM2ImageArchiver import CAM2ImageArchiver

cam = cam2.camera.Camera({
    "cameraID": "5b182887751c3b00044516d6",
    "longitude": 142.369,
    "latitude": 43.7744,
    "legacy_cameraID": 30775,
    "camera_type": "non_ip",
    "source": "webcams_travel",
    "country": "JP",
    "state": "Null",
    "city": "Null",
    "is_active_image": False,
    "is_active_video": False,
    "utc_offset": 32400,
    "timezone_id": "NULL",
    "reference_logo": "webcamstravel.jpg",
    "snapshot_url": "http://images.webcams.travel/preview/1166700904.jpg"
})

archiver = CAM2ImageArchiver(image_difference_percentage=0)
cams = [cam]
archiver.archive(cams, duration=5*60*60, interval=30*60)