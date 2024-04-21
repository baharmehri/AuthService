from rest_framework import serializers


class BaseQueryBuilder:
    _model = None

    class QueryBuilderSerializer(serializers.Serializer):
        query = serializers.JSONField(required=False)
        page = serializers.IntegerField(required=False)
        limit = serializers.IntegerField(required=False)

        def validate_page(self, page):
            if page < 0:
                raise serializers.ValidationError("Invalid page number")
            else:
                return page

        def validate_limit(self, limit):
            if limit < 1 or limit > 100:
                raise serializers.ValidationError("Invalid limit")
            else:
                return limit

    def pagination_response(self, count, page, limit):
        return {
            'page': page,
            'limit': limit,
            'next_page': (page + 1) if count > page * limit else None,
            'total_page': int(count / limit) + 1 if count % limit > 0 else int(count / limit),
            'previous_page': page - 1 if page > 1 else None,
            'total': count
        }

    def _get_logic(self, request, just_user: bool = False):
        page = int(request.data.get("page", 1))
        limit = int(request.data.get("limit", 10))

        parsed_body = self.QueryBuilderSerializer(data=request.data)
        parsed_body.is_valid(raise_exception=True)

        query = parsed_body.validated_data.get("query", {})
        query_builder_result = self.build_query(query)
        if just_user:
            query_builder_result = query_builder_result.filter(user=request.user)
        data = query_builder_result[(page - 1) * limit: page * limit]

        count = query_builder_result.count()
        return {"data": data,
                "meta": {
                    'pagination': self.pagination_response(count, page, limit)}}

    def build_query(self, json_query):
        filters = json_query.get('filter', [])
        sort = json_query.get('sort', [])

        queryset = self._model.objects.all()

        for filter_item in filters:
            key = filter_item['key']
            value = filter_item['value']
            op = filter_item['op']

            if op == 'eq':
                queryset = queryset.filter(**{f"{key}__exact": value})
            elif op == 'neq':
                queryset = queryset.exclude(**{f"{key}__exact": value})
            elif op == 'gt':
                queryset = queryset.filter(**{f"{key}__gt": value})
            elif op == 'gte':
                queryset = queryset.filter(**{f"{key}__gte": value})
            elif op == 'lt':
                queryset = queryset.filter(**{f"{key}__lt": value})
            elif op == 'lte':
                queryset = queryset.filter(**{f"{key}__lte": value})
            elif op == 'in':
                queryset = queryset.filter(**{f"{key}__in": value})
            elif op == 'contains':
                queryset = queryset.filter(**{f"{key}__contains": value})
            elif op == 'icontains':
                queryset = queryset.filter(**{f"{key}__icontains": value})
            elif op == 'startswith':
                queryset = queryset.filter(**{f"{key}__startswith": value})
            elif op == 'endswith':
                queryset = queryset.filter(**{f"{key}__endswith": value})
            elif op == 'isnull':
                queryset = queryset.filter(**{f"{key}__isnull": value})

        for sort_item in sort:
            key = sort_item['key']
            order = sort_item['order']

            if order == 'asc':
                queryset = queryset.order_by(key)
            elif order == 'desc':
                queryset = queryset.order_by(f"-{key}")

        return queryset
