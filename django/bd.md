### Сложные запросы через Django ORM (annotate и aggregate)

Пример с annotate: Подсчет активности пользователей.

```python
from django.db.models import Count

top_users = User.objects.annotate(activity_count=Count('activities')).order_by('-activity_count')[:5]
```

Пример с aggregate: Подсчет общего числа заказов.

```python
from django.db.models import Sum

total_orders = Order.objects.aggregate(total=Sum('price'))
```

Пример сложного запроса с фильтрацией и аннотацией: Подсчет количества заказов по статусам.

```python
from django.db.models import Count, Q

order_statuses = Order.objects.aggregate(
pending=Count('id', filter=Q(status='pending')),
shipped=Count('id', filter=Q(status='shipped'))
)
```
