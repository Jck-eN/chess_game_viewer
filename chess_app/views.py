from django.views.generic import ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.forms import modelformset_factory
from .models import Tournament, Game, PGN
from .forms import PgnForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sessions.middleware import SessionMiddleware
from .getdata import get_player_data


class TournamentsList(ListView):
    model = Tournament
    template_name = "../templates/tournaments.html"
    paginate_by = 10
    ordering = ['-date']


class TournamentDetails(DetailView, MultipleObjectMixin):
    model = Tournament
    template_name = "../templates/tournament.html"
    paginate_by = 1  # TODO: change this
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        object_list = Game.objects.filter(tournament_id=self.object.id).order_by("-id")
        context = super(TournamentDetails, self).get_context_data(object_list=object_list, **kwargs)
        return context


class GamesList(ListView):
    model = Game
    template_name = "../templates/index.html"
    paginate_by = 5
    ordering = ['id']


class GameDetails(DetailView):
    model = Game
    template_name = "../templates/game.html"


@user_passes_test(lambda u: u.is_superuser)
def parse_pgn(request):
    pgns = request.session.get('pgn')
    PgnFormSet = modelformset_factory(PGN, fields=('pgn',), extra=len(pgns))

    if request.method == 'POST':
        formset = PgnFormSet(request.POST)

        if formset.is_valid():
            for f in formset:
                cd = f.cleaned_data
                data = cd.get('pgn')
                get_player_data(data)
            formset.save()
            request.session['pgn'] = ""
            return redirect('/admin/chess_app/pgn')

        return render(request, 'parser.html', {'formset': formset})
    else:
        formset = PgnFormSet(queryset=PGN.objects.none(), initial=[{'pgn': x} for x in pgns])
        return render(request, 'parser.html', {'formset': formset})
