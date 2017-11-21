"""View for search results."""
from django.views.generic import ListView, TemplateView
import re  # Regular expression for search matching

from account.models import Tutor


class IndexView(TemplateView):
    """Render the search page."""

    template_name = 'search.html'
    context_object_name = 'index_context'


class ResultView(ListView):
    """View for search results."""

    template_name = 'result.html'
    model = Tutor

    def get_queryset(self):
        """Determine the list of tutors to be displayed."""
        keywords = self.request.GET['keywords']
        if 'sort' in self.request.GET:
            sort_method = self.request.GET['sort']
        else:
            sort_method = 'rating'  # Sort by rating by default
        all_tutors = Tutor.objects.all()
        filtered_tutors = []
        for tutor in all_tutors:
            # Search query in full name
            tutor_info = tutor.full_name
            # Search query in courses
            for course in tutor.courses.all():
                tutor_info += (" " + str(course))
            # Search query in tags
            for tag in tutor.tags.all():
                tutor_info += (" " + str(tag))
            # Regular expression match
            if re.search(keywords, tutor_info, re.IGNORECASE):
                filtered_tutors.append(tutor)
        if (sort_method == 'hourly_rate'):
            return sorted(filtered_tutors, key=lambda x: x.hourly_rate,
                          reverse=False)
        return sorted(filtered_tutors, key=lambda x: x.avgRating, reverse=True)

    def get_context_data(self, **kwargs):
        """Obtain search query keywords from GET request."""
        context = super(ResultView, self).get_context_data(**kwargs)
        context['keywords'] = self.request.GET['keywords']
        return context
