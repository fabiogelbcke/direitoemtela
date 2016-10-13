from django.test import TestCase
from videos.models import Video
from .models import VideoCategory, Category
from django.core.exceptions import ValidationError

# Create your tests here.

class VideoCategorySaveTestCase(TestCase):

    def setUp(self):
        video1 = Video(title='video1')
        video2 = Video(title='video2')
        video3 = Video(title='video3')
        video4 = Video(title='video4')
        video1.save()
        video2.save()
        video3.save()
        video4.save()
        category = Category(name='category')
        category.save()
        category2 = Category(name='category2')
        category2.save()

    def test_loads_correctly(self):
        videos = Video.objects.all()
        category = Category.objects.first()
        category2 = Category.objects.last()
        self.assertEqual(category.name, 'category')
        self.assertEqual(category2.name, 'category2')
        for counter, video in enumerate(videos):
            self.assertEqual(video.title,
                             'video' + str(counter + 1))

    def test_adds_correct_position_in_order(self):
        category = Category.objects.first()
        videos = Video.objects.all()
        for video in videos:
            vidcat = VideoCategory.objects.create_object(
                video=video,
                category=category)
        for i in range(4):
            title = 'video' + str(i + 1)
            vidcat = VideoCategory.objects.get(video__title=title)
            self.assertEqual(vidcat.position, i + 1)


    def tests_adds_correct_position_in_middle(self):
        """
        if correctly configured, as I insert a video in pos 2
        it shoud push all the videos from position 2 onwards
        to 1 position further
        """
        category = Category.objects.first()
        videos = Video.objects.all()
        for video in videos[:3]:
            vidcat = VideoCategory.objects.create_object(
                video=video,
                category=category)
        vidcat = VideoCategory.objects.create_object(
            video=videos[3],
            category=category,
            position=2)
        vidcat1 = VideoCategory.objects.get(video=videos[0])
        vidcat2 = VideoCategory.objects.get(video=videos[1])
        vidcat3 = VideoCategory.objects.get(video=videos[2])
        vidcat4 = VideoCategory.objects.get(video=videos[3])
        self.assertEqual(vidcat1.position, 1)
        self.assertEqual(vidcat2.position, 3)
        self.assertEqual(vidcat3.position, 4)
        self.assertEqual(vidcat4.position, 2)

    def tests_add_in_end_if_position_is_too_big(self):
        """
        adds in the end if position is bigger than number
        of existing lessons + 1. i.e. if there are 5
        videos and user tries to add in position 10 it
        adds to position 6
        """
        category = Category.objects.first()
        videos = Video.objects.all()
        vidcat = VideoCategory.objects.create_object(
            video=videos[1],
            category=category,
            position=100)
        vidcat = VideoCategory.objects.create_object(
            video=videos[2],
            category=category,
            position=50)
        vidcat = VideoCategory.objects.create_object(
            video=videos[0],
            category=category,
            position=200)
        vidcat1 = VideoCategory.objects.get(video=videos[0])
        vidcat2 = VideoCategory.objects.get(video=videos[1])
        vidcat3 = VideoCategory.objects.get(video=videos[2])
        self.assertEqual(vidcat1.position, 3)
        self.assertEqual(vidcat2.position, 1)
        self.assertEqual(vidcat3.position, 2)
        
    def test_doesnt_accept_negative_position(self):
        category = Category.objects.first()
        video = Video.objects.all().first()
        with self.assertRaises(ValidationError):
            vidcat = VideoCategory.objects.create_object(
                video=video,
                category=category,
                position=-3)
        
