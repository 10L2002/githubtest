#usage: when you want to get 1*80=80 images of cat
#python get_image.py --query "cat" --call_count 1 --image_count 80

 
import argparse, requests, urllib.parse, os, io, imghdr

#basic model parameter
FLAGS = None

# end point
kEndPoint = '**************'

# http request header
kHeaders = { 'Ocp-Apim-Subscription-Key': '****************' } #put your subscription key

#  obtaining image URL for serach results
def GetImageUrls():
    print('Start getting %d images from offset %d' % (FLAGS.image_count, FLAGS.off_set_start ))
    image_list = []

    # because of 150 transaction limit
    for step in range(FLAGS.call_count):

        # obtaining offset 
        off_set = FLAGS.off_set_start + step * FLAGS.image_count

        # parameter for http request
        params = urllib.parse.urlencode({
            'count': FLAGS.image_count,
            'offset': off_set,
            'imageType':'Photo',
            'q': FLAGS.query,
        })
#            'mkt': 'ja-JP',

        # calling bing API 
        res = requests.get(kEndPoint, headers=kHeaders, params=params)

        if step == 0:
            print('Total Estimated Mathes: %s' % res.json()['totalEstimatedMatches'])
        vals = res.json()['value']

        print('Get %d images from offset %d' % (len(vals), off_set))

        # store image URL for serach results
        for j in range(len(vals)):
            image_list.append(vals[j]["contentUrl"])

    return image_list

#  obtaining images and save
def fetch_images(image_list):
    print('total images:%d' % len(image_list))
    for i in range(len(image_list)):

        #  (print progress in each 100 transaction)
        if i % 100 == 0:
            print('Start getting and saving each image:%d' % i)
        try:
            # (obtaining images)
            response = requests.get(image_list[i], timeout=5 )

        # (when error happens)
        except requests.exceptions.RequestException:
            print('%d:Error occurs :%s' % (i, image_list[i]))
            continue

        # filtering by image type
        with io.BytesIO(response.content) as fh:
            image_type = imghdr.what(fh)
            if imghdr.what(fh) != 'jpeg' and imghdr.what(fh) != 'png':
                print('Not saved file type:%s' % imghdr.what(fh))
                continue

        # save images
            with open('{}/image.{}.{}'.format(FLAGS.output_path, str(i), imghdr.what(fh)), 'wb') as f:
                f.write(response.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--image_count',
        type=int,
        default=100,
        help='collection number of image files per api call.'
  )
    parser.add_argument(
        '--call_count',
        type=int,
        default=2,
        help='number of api calls.'
  )
    parser.add_argument(
        '--off_set_start',
        type=int,
        default=0,
        help='offset start.'
  )
    parser.add_argument(
        '--output_path',
        type=str,
        default='', #put name of saving directory 
        help='image files output directry.'
  )
    parser.add_argument(
        '--query',
        type=str,
        default='cat',
        help='search query.'
  )

    
    FLAGS, unparsed = parser.parse_known_args()
    fetch_images(GetImageUrls())
