from datetime import datetime, timedelta

class WeekCalculationMixin:
    week_days = ['日', '月', '火', '水', '木', '金', '土']
    
    def get_week_range(self, base_date):
        """
        abse_dateを含む週の初めと終わりを返す
        """
        start_of_week = base_date - timedelta(days=(base_date.weekday()+1) % 7)
        end_of_week = start_of_week + timedelta(days=6)
        return start_of_week, end_of_week
        
    def get_week_dates(self, start_of_week):
        """
        週の開始から7日分の日付をリストで返す
        """
        return [start_of_week+timedelta(days=i) for i in range(7)]