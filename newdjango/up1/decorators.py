from django.shortcuts import redirect

def anonymous_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Проверяем роль пользователя
            if hasattr(request.user, 'role') and request.user.role.name == 'Менеджер':
                return redirect('admin_panel')  # менеджер — на админку
            else:
                return redirect('home')  # обычный пользователь — на главную
        return view_func(request, *args, **kwargs)
    return _wrapped_view
