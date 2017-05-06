import cv2
import numpy
from skimage.measure import compare_ssim as ssim
from ScreenShotTaker import ScreenShotTaker

"""
These maps map image pixels for checking data. They are of the form:
position_name : position
Where the position is in (y, x, y+h, x+w) form
"""
image_data_positions = {
    'menu_tester': (26, 2, 60, 40)
}

image_data_constants = {
    'menu_tester': cv2.imread(r'data/menu_tester.jpg')
}

PICKER_INDEX_FIRST = 288
PICKER_INDEX_DIFF = 28


class IcyTowerImageData:
    picker_image = cv2.imread(r'data\picker.jpeg')

    def __init__(self, image):
        self.menu_tester = IcyTowerImageData.get_image_part(image, image_data_positions['menu_tester'])
        err = 1 - ssim(cv2.cvtColor(self.menu_tester, cv2.COLOR_BGR2GRAY),
                       cv2.cvtColor(image_data_constants['menu_tester'], cv2.COLOR_BGR2GRAY))
        self.is_menu = err < 0.1
        if self.is_menu:
            self.picker_index = self.get_picker_index(image)

    @staticmethod
    def get_image_part(image, coordinates):
        """
        Gets a rectangle inside an image
        :param image: The big image.
        :param coordinates: The coordinates of the desired rectangle in the form (y, x, y+h, x+w).
        :return: The image part.
        """
        return image[coordinates[0]: coordinates[2], coordinates[1]: coordinates[3]]

    @staticmethod
    def get_picker_index(image):
        """
        Gets a rectangle inside an image
        :param image: The big image.
        :param coordinates: The coordinates of the desired rectangle in the form (y, x, y+h, x+w).
        :return: The image part.
        """
        mask = 255 - IcyTowerImageData.picker_image
        x = cv2.matchTemplate(image, IcyTowerImageData.picker_image, cv2.TM_SQDIFF, mask=mask)
        _, _, min_loc, _ = cv2.minMaxLoc(x)
        picker_y = min_loc[1]
        # The index of the picker is 316 for the first option, and 316 + 28*i for the rest.
        return int((picker_y - PICKER_INDEX_FIRST + PICKER_INDEX_DIFF / 2) / PICKER_INDEX_DIFF)



def main():
    import time
    counter = 0
    while True:
        counter += 1
        image = ScreenShotTaker.get_window_screen_shot('Icy Tower v1.3.1')
        image_data = IcyTowerImageData(image)
        print(image_data.is_menu)
        print(image_data.picker_index)
        # cv2.imwrite('data/aa_%d.jpeg' % counter, image_data.menu_tester)
        time.sleep(2)

if __name__ == "__main__":
    main()
