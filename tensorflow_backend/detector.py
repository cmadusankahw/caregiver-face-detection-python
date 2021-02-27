# from tensorflow_backend.create_dataset import *


def recognize(image_path, database, model):
    """
    Implements face recognition by finding who is the person on the image_path image.

    Arguments:
    image_path -- path to an image
    database -- database containing image encodings along with the name of the person on the image
    model -- Inception model instance in Keras

    Returns:
    identities -- list, containing names of the predicted people on the image_path image
    """

    # ToDo Loop up to 50 images
    encodings = face_img_to_encoding(image_path, model)

    # Initialize the lists for keeping track of people in the picture
    identities = []
    unknown_encodings = []

    # Loop over person encodings in the specific image
    for encoding in encodings:

        ## Step 2: Find the closest encoding ##

        # Initializing "min_dist" to a large value, say 100
        min_dist = 100

        # Loop over the database dictionary's names and encodings.
        for (name, db_encodings) in database.items():

            for db_enc in db_encodings:

                # Compute L2 distance between the target "encoding" and the current "emb" from the database.
                dist = np.linalg.norm(encoding - db_enc)

                # If this distance is less than the min_dist, then set min_dist to dist, and identity to name.
                if dist < min_dist:
                    min_dist = dist
                    identity = name

            if min_dist > 0.8:
                print("Not in the database.")
                # Add the encoding in the database for unknown encodings
                unknown_encodings.append(encoding)

            else:
                if identity not in identities and identity != "unknown":
                    print("You're " + str(identity) + ", the distance is " + str(min_dist))
                    # Add the encoding to the known person's encoding list so that model can become more robust.
                    identities.append(identity)
                    face_encodings = database[str(identity)]
                    face_encodings.append(encoding)
                    database[str(identity)] = face_encodings

    for encoding in unknown_encodings:
        unknown = database["unknown"]
        unknown.append(encoding)
        database["unknown"] = unknown

    return identities