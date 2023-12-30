###
### Author: Randall Candaso
### Course: CSc 110
### Description: This program will recieve an image containing a greenscreen
###              background along with a filler background in order to combine
###              the two, via eliminating the greenscreen.
###

def get_image_dimensions_string(file_name):
    '''
    Given the file name for a valid PPM file, this function will return the
    image dimensions as a string. For example, if the image stored in the
    file is 150 pixels wide and 100 pixels tall, this function should return
    the string '150 100'.
    file_name: A string. A PPM file name.
    '''
    image_file = open(file_name, 'r')
    image_file.readline()
    return image_file.readline().strip('\n')

def load_image_pixels(file_name):
    ''' Load the pixels from the image saved in the file named file_name.
    The pixels will be stored in a 3d list, and the 3d list will be returned.
    Each list in the outer-most list are the rows of pixels.
    Each list within each row represents and individual pixel.
    Each pixels is representd by a list of three ints, which are the RGB values of that pixel.
    '''
    pixels = []
    image_file = open(file_name, 'r')

    image_file.readline()
    image_file.readline()
    image_file.readline()

    width_height = get_image_dimensions_string(file_name)
    width_height = width_height.split(' ')
    width = int(width_height[0])
    height = int(width_height[1])

    for line in image_file:
        line = line.strip('\n ')
        rgb_row = line.split(' ')
        row = []
        for i in range(0, len(rgb_row), 3):
            pixel = [int(rgb_row[i]), int(rgb_row[i+1]), int(rgb_row[i+2])]
            row.append(pixel)
        pixels.append(row)
    return pixels, width, height

def vfx(image_a, image_b, channel, difference):
    '''
    This function takes the greenscreen pixel list and the filler image pixel
    list and determines which pixels should be added to the new image. This is
    determined by the inputted difference as well as the inputted color channel.
    :param image_a: contains a list of the greenscreen image's pixel colors
    :param image_b: contains a list of the filler image's pixel colors
    :param channel: contains the inputted color channel provided by the
                    user
    :param difference: contains the inputted channel difference provided by the
                        user
    :return:
    '''
    new_image = []
    for i in range(len(image_a)):
        for j in range(len(image_a[i])):
            red = image_a[i][j][0]
            green = image_a[i][j][1]
            blue = image_a[i][j][2]
            if channel == 'r':
                if int(green * float(difference)) < red and int(blue * float(difference)) < red:
                    replace = True
                else:
                    replace = False
            elif channel == 'g':
                if int(red * float(difference)) < green and int(blue * float(difference)) < green:
                    replace = True
                else:
                    replace = False
            else:
                if int(green * float(difference)) < blue and int(red * float(difference)) < blue:
                    replace = True
                else:
                    replace = False
            if replace == True:
                new_image.append(image_b[i][j])
            else:
                new_image.append(image_a[i][j])
    return new_image

def create_list(new_image, width):
    '''
    This function takes the newly created pixel list and converts it into
    a functional string that can be used in the .ppm file.
    :param new_image: contains the newly created image's pixel list
    :return:
    '''
    pixel_string = ''
    i = 0
    pixel_count = 1
    while i < len(new_image):
        j = 0
        while j < len(new_image[i]):
            pixel_string += str(new_image[i][j]) + ' '
            j += 1
        if i == len(new_image) - 1:
            i = len(new_image)
        if pixel_count == width:
            pixel_string += '\n'
            pixel_count = 1
        else:
            pixel_count += 1
        i += 1
    return pixel_string

def new_file(new_image, width, height, out_file):
    '''
    This function takes the new pixel list, the original width and height,
    and inserts those objects into the desired output file in their respective order.
    :param new_image: contains the newly created image's pixel list
    :param width: the original image's width
    :param height: the original image's height
    :param out_file: the desire output file the programs information is inputted into
    :return:
    '''
    file = open(out_file, 'w')
    file.write('P3\n')
    file.write(str(width) + ' ' + str(height) + '\n')
    file.write('255\n')
    file.write(str(new_image))
    file.close()

def main():
    '''
    This is the main program function that asks the user for specific inputs to
    start the program.
    :return:
    '''
    channel = input('Enter color channel\n')
    if not (channel == 'r' or channel == 'g' or channel == 'b'):
        print('Channel must be r, g, or b. Will exit.')
        exit()
    channel_difference = input('Enter color channel difference\n')
    if float(channel_difference) < 1.0 or float(channel_difference) > 10.0:
        print('Invalid channel difference. Will exit.')
        exit()
    gs_file = input('Enter greenscreen image file name\n')
    fi_file = input('Enter fill image file name\n')
    image_a, width, height = load_image_pixels(gs_file)
    image_b, width_2, height_2 = load_image_pixels(fi_file)
    if width != width_2 or height != height_2:
        print('Images not the same size. Will exit.')
        exit()
    out_file = input('Enter output file name\n')
    print('Output file written. Exiting.')
    replacement = vfx(image_a, image_b, channel, channel_difference)
    string_of_pixel = create_list(replacement, width)
    new_file(string_of_pixel, width, height, out_file)

main()
