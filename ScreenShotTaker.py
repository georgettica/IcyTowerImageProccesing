import numpy
import pyscreenshot
import win32gui


class ScreenShotTaker:
    def __init__(self):
        pass

    @staticmethod
    def screen_shot_coordinates(coordinates):
        """
        Screen shots coordinates
        :param coordinates: In form of (y, x, y+h, x+w). If none - takes a screen shot of all screen.
        :return: The image of the window.
        """
        if coordinates:
            im = pyscreenshot.grab(bbox=coordinates)
        else:
            im = pyscreenshot.grab()
        im2 = numpy.array(im)
        im2 = im2[..., ::-1]
        return im2

    @staticmethod
    def get_window(window_title):
        """
        :param window_title: The title of the window.
        :return: The handle of the window. 0 if fails.
        """
        return win32gui.FindWindow(None, window_title)

    @staticmethod
    def get_window_coordinates(window_handle):
        """
        :param window_handle: The handle of the window.
        :return: The coordinates of the window in the form of (y, x, y+h, x+w). None if the window was not found.
        """
        if window_handle == 0:
            return None
        rect = win32gui.GetWindowRect(window_handle)
        return rect

    @staticmethod
    def get_window_screen_shot(window_title):
        """
        :param window_title: The title of the window.
        :return: The image of the window.
        """
        window_handle = ScreenShotTaker.get_window(window_title)
        window_coordinates = ScreenShotTaker.get_window_coordinates(window_handle)
        window_screen_shot = ScreenShotTaker.screen_shot_coordinates(window_coordinates)
        return window_screen_shot


def main():
    im = ScreenShotTaker.get_window_screen_shot('Icy Tower v1.3.1')
    import cv2
    cv2.imwrite("Test.jpg", im)


if __name__ == "__main__":
    main()
