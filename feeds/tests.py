from uuid import UUID
from pathlib import Path

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from .models import Feed


class FeedModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.shared_instance = Feed.objects.create(
            name="Test Feed1",
            url="http://localhost:8000/library/dir1/feed.rss",
            artwork="http://localhost:8000/library/dir1/artwork.png",
            qr_code="http://localhost:8000/library/dir1/feed_qr_code.png",
            items_count=3,
        )

    def test_id_is_uuid(self):
        self.assertIsInstance(self.shared_instance.id, UUID)

    def test_name_field(self):
        self.assertEqual(self.shared_instance.name, "Test Feed1")

    def test_url_field(self):
        self.assertEqual(
            self.shared_instance.url, "http://localhost:8000/library/dir1/feed.rss"
        )

    def test_artwork_field(self):
        self.assertEqual(
            self.shared_instance.artwork,
            "http://localhost:8000/library/dir1/artwork.png",
        )

    def test_qr_code_url_field(self):
        self.assertEqual(
            self.shared_instance.qr_code,
            "http://localhost:8000/library/dir1/feed_qr_code.png",
        )

    def test_items_count_field(self):
        self.assertEqual(self.shared_instance.items_count, 3)

    def test_last_generated_field(self):
        self.assertLess(self.shared_instance.last_generated, timezone.now())

    def test_last_generated_updates_on_save(self):
        old_time = self.shared_instance.last_generated
        self.shared_instance.name = "Updated name"
        self.shared_instance.save()
        self.shared_instance.refresh_from_db()
        self.assertNotEqual(self.shared_instance.last_generated, old_time)

    def test_str_method(self):
        self.assertEqual(self.shared_instance.name, self.shared_instance.__str__())

    def test_get_absolute_url_method(self):
        self.assertEqual(
            self.shared_instance.get_absolute_url(),
            reverse(
                "feeds:feed_details", kwargs={"feed_uuid": self.shared_instance.id}
            ),
        )


class TestHomePageView(TestCase):
    """currently home page is directory_list view"""

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_template_content(self):
        response = self.client.get("/")
        self.assertContains(response, "My Folders")

    def test_correct_template_name(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "feeds/directory_list.html")

    def test_invalid_url_returns_404(self):
        response = self.client.get("/invalid_url")
        self.assertEqual(response.status_code, 404)


class TestDirectoryListView(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_available_by_name(self):
        response = self.client.get(reverse("feeds:directory_list"))
        self.assertEqual(response.status_code, 200)

    def test_context_contains_directory_data(self):
        response = self.client.get("/")
        self.assertIn("directories", response.context)

    def test_template_content(self):
        response = self.client.get("/")
        self.assertContains(response, "My Folders")

    def test_correct_template_name(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "feeds/directory_list.html")


class TestFeedDetailsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        feed_name = "test_feed"
        feed_dir = Path(settings.LIBRARY_ROOT) / feed_name
        feed_dir.mkdir(parents=True, exist_ok=True)

        cls.shared_instance = Feed.objects.create(
            name="test_feed",
            url="http://localhost:8000/library/test_feed/feed.rss",
            artwork="http://localhost:8000/library/test_feed/artwork.png",
            qr_code="http://localhost:8000/library/test_feed/feed_qr_code.png",
            items_count=3,
        )

    @classmethod
    def tearDownClass(cls):
        feed_dir = Path(settings.LIBRARY_ROOT) / "test_feed"

        if feed_dir.exists():
            feed_dir.rmdir()

        super().tearDownClass()

    def test_url_exists_at_correct_location(self):
        response = self.client.get(f"/feed/details/{self.shared_instance.id}/")
        self.assertEqual(response.status_code, 200)

    def test_view_available_by_name(self):
        response = self.client.get(
            reverse("feeds:feed_details", kwargs={"feed_uuid": self.shared_instance.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_feed_uuid(self):
        invalid_uuid = "not-a-valid-uuid"
        response = self.client.get(
            reverse("feeds:feed_details", kwargs={"feed_uuid": invalid_uuid})
        )
        self.assertEqual(response.status_code, 404)

    def test_context_contains_feed_data(self):
        response = self.client.get(
            reverse("feeds:feed_details", kwargs={"feed_uuid": self.shared_instance.id})
        )
        self.assertIn("feed", response.context)

    def test_context_contains_valid_data(self):
        response = self.client.get(
            reverse("feeds:feed_details", kwargs={"feed_uuid": self.shared_instance.id})
        )
        self.assertEqual(response.context["feed"].name, self.shared_instance.name)

    def test_template_content(self):
        response = self.client.get(
            reverse("feeds:feed_details", kwargs={"feed_uuid": self.shared_instance.id})
        )
        self.assertContains(
            response,
            f'<li class="breadcrumb-item active">{self.shared_instance.name}</li>',
        )

    def test_correct_template_name(self):
        response = self.client.get(
            reverse("feeds:feed_details", kwargs={"feed_uuid": self.shared_instance.id})
        )
        self.assertTemplateUsed(response, "feeds/feed_details.html")
