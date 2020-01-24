from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index, name='index'),
    path('createuser', views.createuser),
    path('login', views.login),
    path('success', views.dashboard),
    path('logout', views.logout),
    path('wishes/new', views.createwish),
    path('wish/success', views.addwish),
    path('wishes/remove/<int:id>', views.removewish),
    path('wishes/edit/<int:id>', views.editwish),
    path('wish/update/<int:id>', views.updatewish),
    path('wishes/granted/<int:id>', views.grantwish),
    path('wishes/stats', views.viewstats),
]
