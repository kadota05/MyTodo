from django import forms
from django.forms import ModelForm
from .models import Habit

class HabitForm(ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'target_day_per_week', 'created_at']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'target_day_per_week': forms.NumberInput(attrs={
                'type': 'range',
                'class': 'form-range',  # Bootstrap 5 のレンジ入力用クラス
                'min': '1',            # 例えば0～7の範囲で選択する場合
                'max': '7',
                'step': '1',
                'value': '4',          # デフォルト値を4に設定
                'style': 'accent-color: #888888 !important;'
            }),
            'created_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
        }
