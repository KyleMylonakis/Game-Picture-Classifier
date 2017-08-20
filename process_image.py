###############################################################
# Script to automate image processcing
# iheight and iwidth control the desired output resolution
###############################################################


from scipy import ndimage as ndim
import scipy
import sys
import os
import imghdr


# Get the current working directory
os.environ["PATH"] += os.pathsep + os.getcwd()

if not os.path.exists(os.getcwd() + '/game_images/processed_images/'):
    print('Making Processed Image Directory')
    os.makedirs('game_images/processed_images/')

# Label the directory with all the raw images
raw_dir = os.getcwd() + '/game_images/raw_images'

# Select desired output resolution
iheight = 576
iwidth = 1024


# Walk over all subdirectories in the raw database
for root, dirs, files in os.walk(raw_dir):
    #print(root)
    for item in files:
        try:
            # Figure out which game the image comes from
            current_game = []
            for ii in range(len(root)):
                if not (root[-(ii+1)] == ('\\' or '/')):
                    current_game.append(root[-ii -1])
                else:
                    break
            current_game.reverse()
            current_game = ''.join(current_game)

            #print(os.getcwd() + '/game_images/processed_images/' + current_game)

            # Create a folder for the current game's processed images
            if not os.path.exists(os.getcwd() + '/game_images/processed_images/' + current_game ):
                os.makedirs('game_images/processed_images/' + current_game)

            #print(current_game)

            # Process the images
            img_p = ndim.imread(os.path.join(root, item))
            img_p = scipy.misc.imresize(img_p, (iheight, iwidth))
            img_p = scipy.misc.toimage(img_p)
            # Need to save with a file extension specified
            img_p.save(os.getcwd() + '/game_images/processed_images/' + current_game + '/' + item + '.png')
            print('Successfully Processed ' + current_game + ' Image ' + item)

        except:
            #print(item + " is not an image.")
            pass
            
