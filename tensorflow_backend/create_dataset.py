from keras import backend as K
K.set_image_data_format('channels_first')
from tensorflow_backend.fr_utils import *
from tensorflow_backend.inception_blocks import *
import face_recognition


# Initialize the model
# The model takes images with shape (3, 96, 96) 'channels first'
FRmodel = faceRecoModel(input_shape=(3, 96, 96))

#Showing the architecture of the model
FRmodel.summary()


# Function for resizing an image
def pre_process_image(img, image_size):
    """
    Resizes an image into given image_size (height, width, channel)

    Arguments:
    img -- original image, array
    image_size -- tuple containing width, height, channel of the image (h, w, c)

    Returns:
    img -- resized image
    """
    height, width, channels = image_size
    img = cv2.resize(img, dsize=(height, width))
    return img


# Function for identifying face locations on an image
def find_face_locations(image_path):
    """
    returns the bounding box locations of the faces, image from the path

    Arguments:
    image_path -- destination of the original image
    image_size -- tuple containing width and height of the image (h, w)

    Returns:
    (top, right, bottom, left), image -- bounding box
    if multiple faces present in the picture returns a list of tuples,
    image obtained from image_path
    """

    # Use face recognition module to detect faces
    image = face_recognition.load_image_file(image_path)

    # Test: print("Shape of the image: " + str(image.shape))

    face_locations = face_recognition.face_locations(image)
    for face_location in face_locations:
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
                                                                                                    right))
    return face_locations, image


def face_img_to_encoding(image_path, model):
    """
    returns the embedding vector of the specific image from the path

    Arguments:
    image_path -- Destination of the original image
    model -- Inception model instance in Keras

    Returns:
    embeddings -- List containing embeddings of the people in the image
    """

    # obtain the face locations and the image
    face_locations, image = find_face_locations(image_path)

    # initialize the embeddings list
    embeddings = []

    # initialize embeddings list
    for face_location in face_locations:
        # Print the location of each face in this image
        top, right, bottom, left = face_location

        # access the actual face itself
        face_image = image[top:bottom, left:right]

        # resize the cropped face image
        image_size = (96, 96, 3)
        img = pre_process_image(face_image, image_size)

        # pre-process the face image
        img = img[..., ::-1]
        img = np.around(np.transpose(img, (2, 0, 1)) / 255.0, decimals=12)
        x_train = np.array([img])
        embedding = model.predict_on_batch(x_train)
        embeddings.append(embedding)

    return embeddings

# ToDo Make a loop to read all images from data folder format them and read landmarks and then store in database

################## TEST ####################################################
# Create a initial database for identifying people
database = {}
database["Chiran"] = face_img_to_encoding("data/chiran/100chiran.jpg", FRmodel)

# Test for face_img_to_encoding
embedding = face_img_to_encoding("data/chiran/180chiran.jpg", FRmodel)
################### TEST ####################################################




