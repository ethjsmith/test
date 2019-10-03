with picamera.PiCamera() as camera:
            camera.resolution = (1024,768)
            camera.start_preview()
            time.sleep(1)
            camera.capture('/static/pic.jpg')
