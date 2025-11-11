import logging
from pathlib import Path
from uuid import UUID

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.http import Http404

from core.utils import build_host, get_timezone_aware_datetime
from .models import Feed
from .services import (
    generate_feed,
    scan_library_for_subdirs,
    get_audio_files,
    has_audio_files,
)

logger = logging.getLogger(__name__)


def is_feed_none_or_stale(feed_metadata, directory):
    if feed_metadata is None:
        return True

    dir_modified_time = get_timezone_aware_datetime(directory.stat().st_mtime)

    return feed_metadata.last_generated < dir_modified_time


def directory_list(request):
    context = {"directories": []}
    dirs = scan_library_for_subdirs()

    for d in dirs:
        dir_feed = Feed.objects.filter(name=d.name).first()
        stale = is_feed_none_or_stale(dir_feed, d)

        if not dir_feed:
            status = "no_feed"
        elif stale:
            status = "stale"
        else:
            status = "up_to_date"

        dir_metadata = {
            "name": d.name,
            "modified_time": get_timezone_aware_datetime(d.stat().st_mtime),
            "file_count": len(get_audio_files(d)),
            "feed": dir_feed,
            "status": status,
        }
        context["directories"].append(dir_metadata)

    return render(request, "feeds/directory_list.html", context)


def create_feed(request, directory_name):
    directory = Path(settings.LIBRARY_ROOT, directory_name)

    if not directory.exists() or not directory.is_dir():
        messages.error(request, f"'{directory_name}' folder not found.")
        return redirect("/")

    if not has_audio_files(directory):
        messages.warning(request, f"No audio files found in folder: {directory.name}.")
        return redirect("/")

    feed_metadata = Feed.objects.filter(name=directory_name).first()

    if not is_feed_none_or_stale(feed_metadata, directory):
        messages.info(request, "Feed is already up to date.")
        return render(
            request, "feeds/feed_details.html", context={"feed": feed_metadata}
        )

    try:
        host_base_url = build_host(request)
        feed = generate_feed(host_base_url, directory)

    except Exception:
        logger.exception(
            "Error generating feed for folder: %s", directory.name, exc_info=True
        )
        messages.error(request, f"Error generating feed for folder: {directory.name}")
        return redirect("/")

    if feed:
        messages.success(
            request,
            f"Successfully generated/updated feed for folder: {directory_name}",
        )
        return redirect(feed.get_absolute_url())
    messages.error(request, "Error generating feed.")
    return redirect("/")


def feed_details(request, feed_uuid):
    try:
        uuid_obj = UUID(feed_uuid)
    except ValueError:
        raise Http404("Invalid feed ID.")

    feed = get_object_or_404(Feed, id=uuid_obj)
    directory = Path(settings.LIBRARY_ROOT, feed.name)
    stale = is_feed_none_or_stale(feed, directory)
    
    context = {"feed": feed, "stale": stale}
    return render(request, "feeds/feed_details.html", context)


def app_settings(request):
    return render(request, "feeds/settings.html")


def clean_up(request):
    dirs_names = [d.name for d in scan_library_for_subdirs()]
    feeds_qs = Feed.objects.all()
    orphaned_feeds = [f for f in feeds_qs if f.name not in dirs_names]

    removed_count = 0
    if request.method == "POST":
        if orphaned_feeds:
            removed_count = len(orphaned_feeds)
            for feed in orphaned_feeds:
                feed.delete()
            messages.success(
                request, f"Successfully removed {removed_count} orphaned feed{'s' if removed_count != 1 else ''}"
            )
            feeds_qs = Feed.objects.all()
            orphaned_feeds = [f for f in feeds_qs if f.name not in dirs_names]

        else:
            messages.info(request, "No orphaned feeds found.")
            
    context = {
        "feeds_count": feeds_qs.count(),
        "dirs_count": len(dirs_names),
        "orphaned_count": len(orphaned_feeds),
        "orphaned_feeds": orphaned_feeds,
        "removed_count": removed_count,
    }

    return render(request, "feeds/cleanup.html", context)
