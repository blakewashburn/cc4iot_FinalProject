import json
import boto3
import urllib

def lambda_handler(event, context):
    
    # Setup AWS clients
    rekogClient = boto3.client("rekognition")
    s3Client = boto3.client("s3")
    iotClient = boto3.client("iot-data")
    
    # Grab original image of face to match captured images against
    originalImage = s3Client.get_object(Bucket = "imagecollectionbucket", Key = "originalImage.png")
    
    # Get the captured Image from the camera
    inputImageBucket = event['Records'][0]['s3']['bucket']['name']
    inputImageKey = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    inputImage = s3Client.get_object(Bucket = inputImageBucket, Key = inputImageKey)
    
    # Get bytestream of images
    originalImageContect = originalImage["Body"].read()
    inputImageContent = inputImage["Body"].read()
    
    # Invoke rekognition function to compare inputImage and originalImage
    # Only return faces if 80 percent confidence is achieved
    matchedFaces = client.compare_faces(SimilarityThreshold = 80,
                                  SourceImage={'Bytes': inputImageContent},
                                  TargetImage={'Bytes': originalImageContent})
    
    
    # Check for a matched face
    for faceMatch in matchedFaces['FaceMatches']:
        if faceMatch != NULL:
            # Publish face match message to IoT Core 
            iotClient.publish(topic='iotTopic', qos=1, payload=json.dumps({"message":"Face Match Found!"}))
            

    return {
        'statusCode': 200,
        'body': json.dumps('Completed Function Successfully')
    }